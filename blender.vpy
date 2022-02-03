from configparser import ConfigParser
from vapoursynth import core
import vapoursynth as vs
import havsfunc

Recipe = ConfigParser()
Recipe.read(Config)
Video = core.ffms2.Source(source=Input, cache=False)

if bool(Interpolate):
	Video = havsfunc.InterFrame(Video, GPU=True, 
	NewNum=int(Recipe['interpolation']['fps']), 
	Preset=str(Recipe['interpolation']['speed']),
	Tuning=str(Recipe['interpolation']['tuning']), 
	OverrideAlgo=int(Recipe['interpolation']['algorithm']))
		
frame_gap = int(Video.fps / 60)
blended_frames = int(frame_gap * float(Recipe['frameblending']['intensity']))
if blended_frames > 0:
	if blended_frames % 2 == 0:
		blended_frames += 1
	weights = [1 / blended_frames] * blended_frames
	Video = core.frameblender.FrameBlend(Video, weights, True)
Video = havsfunc.ChangeFPS(Video, int(Recipe['frameblending']['fps']))
Video.set_output()