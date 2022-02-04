from vapoursynth import core
import vapoursynth as vs
from os import path # To split file extension
from configparser import ConfigParser
import havsfunc # aka Interframe2

conf = ConfigParser()
conf.read(config_filepath)

# Bool aliases
yes = ('True','true','yes','y','1')
no = ('False','false','no','n','0')

if path.splitext(input_video)[1] == '.avi':
    video = core.avisource.AVISource(f"{input_video}")
    video = core.fmtc.matrix(clip=video, mat="601", col_fam=vs.YUV, bits=16)
    video = core.fmtc.frameblending(clip=video, css="420")
    video = core.fmtc.bitdepth(clip=video, bits=8)
else:
    video = core.ffms2.Source(source=f"{input_video}", cache=False)

if float(conf['timescale']['in']) != 1: # Input timescale, done before interpolation
    video = core.std.AssumeFPS(video, fpsnum=(video.fps * (1 / conf['timescale']['in'])))

if str(conf['interpolation']['enabled']).lower() in yes: # Interpolation using Interframe2 (uses SVP-Flow, which is what blur uses)

    video = havsfunc.InterFrame(
        video,
        GPU=True,
        NewNum=int(conf['interpolation']['fps']),
        Preset=str(conf['interpolation']['speed']),
        Tuning=str(conf['interpolation']['tuning']),
        OverrideAlgo=int(conf['interpolation']['algorithm']))

if float(conf['timescale']['out']) != 1: # Output timescale, done after interpolation
    video = core.std.AssumeFPS(video, fpsnum=video.fps * float(conf['timescale']['out']))

if str(conf['misc']['deduplication']).lower() in yes:
    def FillDrops(clip, thresh=0.1):
        if not isinstance(clip, vs.VideoNode):
            raise ValueError('This is not a clip')

        differences = core.std.PlaneStats(clip, clip[0] + clip)

        super = core.mv.Super(clip)
        forward_vectors = core.mv.Analyse(super, isb=False)
        backwards_vectors = core.mv.Analyse(super, isb=True)
        filldrops = core.mv.FlowInter(clip, super, mvbw=backwards_vectors, mvfw=forward_vectors, ml=1)
        
        def selectFunc(n, f):
            if f.props['PlaneStatsDiff'] < thresh:
                return filldrops
            else:
                return clip

        fixed = core.std.FrameEval(clip, selectFunc, prop_src=differences)
        return fixed
    video = FillDrops(video, thresh=0.001)


frame_gap = int(video.fps / int(conf['frameblending']['fps']))
blended_frames = int(frame_gap * int(conf['frameblending']['intensity']))
if blended_frames > 0:
    if blended_frames % 2 == 0:
        blended_frames += 1
    weights = [1 / blended_frames] * blended_frames 
    video = core.frameblender.FrameBlend(video, weights, True)
video = havsfunc.ChangeFPS(video, int(conf['frameblending']['fps']))
video.set_output()
