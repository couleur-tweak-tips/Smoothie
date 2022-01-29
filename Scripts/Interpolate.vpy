# Interpolate

from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
Program=Program.lower()
video = core.ffms2.Source(source=Video, cache=False)
if Program == 'svp':
	video = haf.InterFrame(video, GPU=True, NewNum=int(InterpolateFPS), Preset=str(Preset), Tuning=str(Tuning), OverrideAlgo=int(Algorithm))
elif Program == 'rife':
	from vsrife import RIFE
	video = core.resize.Bicubic(video, format=vs.RGBS)
	while video.fps < int(InterpolateFPS):
		video = RIFE(video)
	video = core.resize.Bicubic(video, format=vs.YUV420P8, matrix_s="709")
frame_gap = int(video.fps / 60)
blended_frames = int(frame_gap * float(Intensity))
if blended_frames > 0:
	if blended_frames % 2 == 0:
		blended_frames += 1
	weights = [1 / blended_frames] * blended_frames
	video = core.frameblender.FrameBlend(video, weights, True)
video = haf.ChangeFPS(video, int(ResampleFPS))
video.set_output()