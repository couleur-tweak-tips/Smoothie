from os import path
import sys
sys.path.append(path.curdir)
import vapoursynth as vs
from vapoursynth import core
from configparser import ConfigParser
import havsfunc
from re import search


# Bool aliases
yes = ['True','true','yes','y','1', True]
no = ['False','false','no','n','0','null','',None, False]


def defined(var):
    # variable to test must be provided as a string
    # e.g testing the variable var would need to be defined('var'), not defined(var)
    try:
        eval(var)
    except NameError:
        return False
    else:
        return True
    
def verb(msg):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    if defined('verbose') == True:
        print(logging.debug(f' {msg}'))

global conf
conf = eval(config)
verb(f"what is {conf['encoding']['args']}")

verb('Starting indexing..')
if path.splitext(input_video)[1] == '.avi':
    video = core.avisource.AVISource(input_video)
    video = core.fmtc.matrix(clip=video, mat="709", col_fam=vs.YUV, bits=16)
    # If you're gonna bother working with .AVI you're probably using 709 anyways
    # (let me know of one valid case to use this container as input)
    video = core.fmtc.resampling(clip=video, css="420")
    video = core.fmtc.bitdepth(clip=video, bits=8)
else:
    video = core.ffms2.Source(source=input_video, cache=False)

if '__TEMP' in conf.keys():

    # if type(trim) is bytes: # Convert bytestring to array to string T_T
    #     trim = eval(''.join(map(chr, trim)))[0]
        
    fps = round(eval(str(video.fps))) # Converts str '1000000/3571' to int 280
    # start, end = trim.split(',')
    # verb(f"what is {start}, {end} and {fps}")
    #def get_sec(time_str):
    #    if type(time_str) is list: time_str = time_str[0]
    #    if type(time_str) is str:
    #        if '.' in time_str: time_str = time_str.split('.')[0]
    #        if search('[a-zA-Z]', time_str) is not None:
    #            raise Exception(f'Timecode to trim contains a letter: {time_str}')
    #    # god bless https://stackoverflow.com/a/6402934
    #    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(time_str).split(':'))))
    start, end = conf['__TEMP']['start'], conf['__TEMP']['end']
    verb(f'Trimming {start} to {end} with fps {fps}')
    video = core.std.Trim(video, start, end)
    verb(f'Finished cutting trim from {start} to {end}')
    
if float(conf['timescale']['in']) != 1: # Input timescale, done before interpolation
    video = core.std.AssumeFPS(video, fpsnum=(video.fps * (1 / float(conf['timescale']['in']))))

if str(conf['interpolation']['enabled']).lower() in yes: # Interpolation using Interframe2 (uses SVP-Flow, which is also what blur uses)
     useGPU = (conf['interpolation']['gpu']) in yes
     if str(conf['interpolation']['fps']).endswith('x'): # if  multiplier support
         interp_fps = int(video.fps * int((conf['interpolation']['fps']).replace('x','')))   
     else:
         interp_fps = int(conf['interpolation']['fps'])
     video = havsfunc.InterFrame(
         video,
         GPU=useGPU,
         NewNum=interp_fps,
         Preset=str(conf['interpolation']['speed']),
         Tuning=str(conf['interpolation']['tuning']),
         OverrideAlgo=int(conf['interpolation']['algorithm'])
     )
    
if float(conf['timescale']['out']) != 1: # Output timescale, done after interpolation
    video = core.std.AssumeFPS(video, fpsnum=(video.fps * float(conf['timescale']['out'])))

if conf['misc']['dedupthreshold'] not in no:
    import filldrops
    video = filldrops.FillDrops(
        video,
        thresh = float((conf['misc']['dedupthreshold']))
    )

if str(conf['frame blending']['enabled']).lower() in yes:

    import weighting
    repartition = conf['frame blending']['weighting']

    frame_gap = int(video.fps / int(conf['frame blending']['fps']))
    blended_frames = int(frame_gap * float(conf['frame blending']['intensity']))
    if blended_frames > 0:
        if blended_frames % 2 == 0:  # If number is not odd (requires odd number of frames)
            blended_frames += 1

    if ',' in repartition or type(repartition) is list: # , means it's a list (aka array)
        weights = repartition
    elif repartition in ['gauss','gaussSym','gaussian','gaussianSym'] and ';' in repartition:
        rep, dev, bound = repartition.Split(';')
        weights = eval(f'weighting.{repartition}(frames={blended_frames}, standard_deviation={dev}, bound={eval(bound)})')
    else:
        weights = eval(f'weighting.{repartition}({blended_frames})')
    verb(f"Weights: {weights}")
    video = core.frameblender.FrameBlend(video, weights)
    video = havsfunc.ChangeFPS(video, int(conf['frame blending']['fps']))
    
    if conf['flowblur']['enabled'] not in no:
                
        if conf['flowblur']['amount'] not in no:
            original = video # Makes an un-smeared copy to use for the mask later    
            s = core.mv.Super(video, 16, 16, rfilter=3)
            bv = core.mv.Analyse(s, isb=True, blksize=16, plevel=2, dct=5)
            fv = core.mv.Analyse(s, blksize=16, plevel=2, dct=5)
            video = core.mv.FlowBlur(video, s, bv, fv, blur=(conf['flowblur']['amount']))

        if conf['flowblur']['mask'] not in no:
            mask = conf['flowblur']['mask']
            if type(mask_directory) is bytes:
                mask_directory = ''.join(map(chr, mask_directory))
            verb(f'Mixing in {mask_directory} and {mask}..')
            if not path.exists(mask): # Then user specified a relative path, and needs to be verified
                if '.' in mask: # Then the user specified a file extension
                    mask = path.join(mask_directory, mask)
                else: # Then the user did not specify any image extension and it needs to loop through common exts
                    for extension in ['png','jpg','jpeg']:
                        if not path.exists(mask):
                            mask = path.join(mask_directory, f'{mask}.{extension}')
                        else:
                            continue # Loops until it ends if it found valid mask path
            if not path.exists(mask): # Then even if we did some checks to convert to absolute path it still does not exists
                raise vs.Error(f"The Mask filepath you provided does not exist: {mask}")

            #rmask = core.imwri.Read(mask)
            #video = core.std.MaskedMerge(
            #    clipa=original,
            #    clipb=video,
            #    mask=rmask.std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.BoxBlur(vradius = 6,vpasses = 2,hradius = 6,hpasses = 2),
            #    first_plane=True
            #    )

            verb(f'Using mask {mask}')
            filtered = video.std.Expr(expr=['x 0 -','',''])
            GW = core.ffms2.Source(mask, cache=False)
            BW = GW.resize.Bicubic(video.width,video.height, matrix_s='709',format=vs.GRAY8)
            BW = BW.std.Levels( min_in=0, max_in=235, gamma =0.05, min_out=0, max_out=255)
            video = havsfunc.Overlay(original, filtered, mask=BW)

video.set_output()
