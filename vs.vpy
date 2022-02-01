from configparser import ConfigParser
from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf

Recipe = ConfigParser()
Recipe.read(Config)
Video = core.ffms2.Source(source=Input, cache=False)

if bool(Interpolate):
	if Recipe['interpolation']['program'].lower() == 'svp':
		Video = haf.InterFrame(Video, GPU=True, 
		NewNum=int(Recipe['interpolation']['fps']), 
		Preset=str(Recipe['interpolation']['speed']),
		Tuning=str(Recipe['interpolation']['tuning']), 
		OverrideAlgo=int(Recipe['interpolation']['algorithm']))
		
	elif Recipe['interpolation']['program'].lower() == 'rife':
		Video = core.resize.Bicubic(Video, format=vs.RGBS)
		
		while Video.fps < int(Recipe['interpolation']['fps']):
			Video = core.rife.RIFE(Video)
			
		Video = core.resize.Bicubic(Video, format=vs.YUV420P8, matrix_s="709")
	
frame_gap = int(Video.fps / 60)
blended_frames = int(frame_gap * float(Recipe['resampling']['intensity']))
if blended_frames > 0:
	if blended_frames % 2 == 0:
		blended_frames += 1
	weights = [1 / blended_frames] * blended_frames
	Video = core.frameblender.FrameBlend(Video, weights, True)
Video = haf.ChangeFPS(Video, int(Recipe['resampling']['fps']))
Video.set_output()