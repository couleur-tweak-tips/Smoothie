from os import environ, path
from urllib.request import urlretrieve 
Temp=environ["TEMP"]
Folder=f'{environ["APPDATA"]}\Smoothie'

# Vapoursynth Scripts
if path.exists(f'{Folder}/Resample.vpy') is False:
    urlretrieve("https://raw.githubusercontent.com/Aetopia/Smoothie/master/Scripts/Resample.vpy", f'{Folder}/Resample.vpy')

if path.exists(f'{Folder}/Interpolate.vpy') is False:
    urlretrieve("https://raw.githubusercontent.com/Aetopia/Smoothie/master/Scripts/Interpolate.vpy", f'{Folder}/Interpolate.vpy')

# Resample
    
def Resample(Video, Intensity, FPS):
    Resample = open(Temp+"/Render.vpy", "w+")
    Intensity=float(Intensity)
    Script=f""" 
from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
video = core.ffms2.Source(source=r"{Video}", cache=False)
frame_gap = int(video.fps / 60)
blended_frames = int(frame_gap * {Intensity})
if blended_frames > 0:
	if blended_frames % 2 == 0:
		blended_frames += 1
	weights = [1 / blended_frames] * blended_frames
	video = core.frameblender.FrameBlend(video, weights, True)
video = haf.ChangeFPS(video, {FPS})
video.set_output()
"""
    Resample.write(Script)
    Resample.close()
    
    VSPipeArgs=f'-a Video="{Video}" -a Intensity="{Intensity}" -a FPS="{FPS}" "{Folder}/Resample.vpy"'
    return VSPipeArgs

# Interpolate
def Interpolate(Video, InterpolateFPS, Preset, Tuning, Algorithm, Program, ResampleFPS, Intensity):
    Interpolate = open(Temp+"/Render.vpy", "w+")
    Script=f"""
from vapoursynth import core
import vapoursynth as vs
import havsfunc as haf
Program="{Program}".lower()
video = core.ffms2.Source(source=r'{Video}', cache=False)
if Program == 'svp':
	video = haf.InterFrame(video, GPU=True, NewNum={InterpolateFPS}, Preset={Preset}, Tuning={Tuning}, OverrideAlgo={Algorithm})
elif Program == 'rife':
	from vsrife import RIFE
	video = core.resize.Bicubic(video, format=vs.RGBS)
	while video.fps < {InterpolateFPS}:
		video = RIFE(video)
	video = core.resize.Bicubic(video, format=vs.YUV420P8, matrix_s="709")
frame_gap = int(video.fps / 60)
blended_frames = int(frame_gap * {Intensity})
if blended_frames > 0:
	if blended_frames % 2 == 0:
		blended_frames += 1
	weights = [1 / blended_frames] * blended_frames
	video = core.frameblender.FrameBlend(video, weights, True)
video = haf.ChangeFPS(video, {ResampleFPS})
video.set_output()
""" 
    Interpolate.write(Script)
    Interpolate.close() 

    VSPipeArgs=f'-a Video="{Video}" -a InterpolateFPS="{InterpolateFPS}" -a Preset="{Preset}" -a Tuning="{Tuning}" -a Algorithm="{Algorithm}" -a Program="{Program}" -a ResampleFPS="{ResampleFPS}" -a Intensity="{Intensity}" "{Folder}/Interpolate.vpy"'
    return VSPipeArgs  
