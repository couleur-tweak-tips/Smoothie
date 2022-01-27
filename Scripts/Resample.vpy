# Resample Script

from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
video = core.ffms2.Source(source=Video, cache=False)
frame_gap = int(video.fps / 60)
blended_frames = int(frame_gap * float(Intensity))
print(blended_frames)
if blended_frames > 0:
	if blended_frames % 2 == 0:
		blended_frames += 1
	weights = [1 / blended_frames] * blended_frames
	video = core.frameblender.FrameBlend(video, weights, True)
video = haf.ChangeFPS(video, int(FPS))
video.set_output()
