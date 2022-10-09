import vapoursynth as vs
from vapoursynth import core

# From current directory
from os import path
from sys import path as envpath
if path.dirname(__file__) not in envpath: # Not by default
    envpath.append(path.dirname(__file__)) 
from helpers import *
from plugins import filldrops, weighting, havsfunc, adjust

from ast import literal_eval
import logging
logging.basicConfig(level=logging.INFO)

try:
    global conf
    conf = eval(config)
except NameError:
    raise vs.Error("Failed to load recipe (was it declared with VSPipe?)")
except SyntaxError:
    raise Exception(f"Failed to parse passed the JSON recipe: \n\n{config}")
    
def verb(msg):
    if conf['misc']['verbose'] == True:
        print(logging.debug(f' {msg}'))

    
if path.splitext(input_video)[1] == '.avi':
    video = core.avisource.AVISource(input_video)
    video = core.fmtc.matrix(clip=video, mat="709", col_fam=vs.YUV, bits=16)
        # If you're gonna bother working with .AVI you're probably using 709 anyways
        # (let me know of one valid case to use this container as input)
    video = core.fmtc.resampling(clip=video, css="420")
    video = core.fmtc.bitdepth(clip=video, bits=8)
else:
    video = core.ffms2.Source(source=input_video, cache=False)
    
if 'start' and 'end' in conf['TEMP'].keys():
        
    fps = round(eval(str(video.fps))) # Converts str '1000000/3571' to int 280
    start, end = conf['TEMP']['start'], conf['TEMP']['end']
    
    verb(f'Trimming {start} to {end} with fps {fps}')
    video = core.std.Trim(video, start, end)
    verb(f'Finished cutting trim from {start} to {end}')

if float(conf['timescale']['in']) != 1: # Input timescale, done before interpolation
    video = core.std.AssumeFPS(video, fpsnum=(video.fps * (1 / float(conf['timescale']['in']))))

if str(conf['interpolation']['enabled']).lower() in yes: # Interpolation using Interframe2 (uses SVP-Flow, which is also what blur uses)
     useGPU = (conf['interpolation']['use gpu']) in yes
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
    from plugins import filldrops
    video = filldrops.FillDrops(
        video,
        thresh = float((conf['misc']['dedupthreshold']))
    )

if str(conf['frame blending']['enabled']).lower() in yes:

    from plugins import weighting
    repartition = conf['frame blending']['weighting']
    if type(repartition) is str:
        partition = repartition.lower()

    frame_gap = int(video.fps / int(conf['frame blending']['fps']))
    blended_frames = int(frame_gap * float(conf['frame blending']['intensity']))
    if blended_frames > 0:
        if blended_frames % 2 == 0:  # If number is not odd (requires odd number of frames)
            blended_frames += 1
    
    if type(repartition) is str:
        repartition = conf['frame blending']['weighting'].split(';')[0]
        adv = conf['frame blending']['weighting'].split(';')[1:]
        argcount = len(adv)
    else:
        repartition = conf['frame blending']['weighting']

    args = {'frames': blended_frames}

    # shout out yandere dev for the inspiration 
    if repartition in ['gaussian','gauss','gaussiansym','gausssym','gaussian_sym']:
        if argcount >= 1:
            args['standard_deviation'] = int(adv[0])
        if argcount >= 2:
            args['bound'] = literal_eval(adv[1].strip())
        if repartition in ['gaussian','gauss']:
            weights = weighting.gaussian(**args)
        else:
            weights = weighting.gaussiansym(**args)
    elif repartition == 'custom':
        args['func'] = adv[0]
        if argcount >= 2:
            args['bound'] = literal_eval(adv[1].strip())
        weights = weighting.custom(**args)
    elif repartition == 'pyramid':
        if argcount >= 1:
            if adv[0] in yes:
                args['reverse'] = True
        weights = weighting.pyramid(**args)
    elif type(repartition) is list:
        weights = weighting.divide(frames=blended_frames, weights=repartition)
    elif repartition[0] == '[':
        weights = literal_eval(repartition.strip())
    else:
        if not hasattr(weighting, repartition):
            raise ValueError(f'Weighting {repartition} does not exist')
        else:
            weights = eval(f'weighting.{repartition}(frames={blended_frames})')
    
    #verb(f"Weights: {weights}")
    video = core.frameblender.FrameBlend(video, weights)
    video = havsfunc.ChangeFPS(video, int(conf['frame blending']['fps']))

if conf['flowblur']['enabled'] not in no:
    if conf['flowblur']['amount'] not in no:
        original = video # Makes an un-smeared copy to use for the mask later    
        s = core.mv.Super(video, 16, 16, rfilter=3)
        bv = core.mv.Analyse(s, isb=True, blksize=16, plevel=2, dct=5)
        fv = core.mv.Analyse(s, blksize=16, plevel=2, dct=5)
        video = core.mv.FlowBlur(video, s, bv, fv, blur=(conf['flowblur']['amount']))
    if conf['flowblur']['mask'].lower() not in no:
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
        rmask = core.ffms2.Source(mask)
        video = core.std.MaskedMerge(
           clipa=original,
           clipb=video,
           mask=rmask.std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.BoxBlur(vradius = 6,vpasses = 2,hradius = 6,hpasses = 2),
           first_plane=True
           )
        # verb(f'Using mask {mask}')
        # filtered = video.std.Expr(expr=['x 0 -','',''])
        # GW = core.ffms2.Source(mask, cache=False)
        # BW = GW.resize.Bicubic(video.width,video.height, matrix_s='709',format=vs.GRAY8)
        # BW = BW.std.Levels( min_in=0, max_in=235, gamma =0.05, min_out=0, max_out=255)
        # video = havsfunc.Overlay(original, filtered, mask=BW)

video.set_output()
