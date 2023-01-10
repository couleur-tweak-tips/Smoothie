# This file is what contains the VapourSynth code used in vitamix.vpy

import vapoursynth as vs
from vapoursynth import core
from os import path
from sys import path as envpath
if path.dirname(__file__) not in envpath: # Not by default
	envpath.append(path.dirname(__file__)) 
from helpers import *
from plugins import filldrops, weighting, havsfunc, adjust
from ast import literal_eval
import logging
logging.basicConfig(level=logging.DEBUG)
import constants

"""
Parses the absolute path mask and it's extension
"""

def Masking(clip: vs.VideoNode,
            original: vs.VideoNode,
            maskFn: str,
            maskDir: str):

	maskPath = maskFn
	if not path.splitext(maskFn)[1]:
		for ext in constants.IMAGE_EXTS:
			if path.exists(file := path.join(maskDir, maskFn + ext)):
				maskPath = file
				break

	rmask = core.ffms2.Source(maskPath)
	featherMask = rmask.std.Minimum().std.BoxBlur(vradius=6, hradius=6, vpasses=2,hpasses = 2)

	return core.std.MaskedMerge(clipa=clip, clipb=original, mask=featherMask, first_plane=True)
	# region debug
	# print(logging.debug(maskPath))
	# print(logging.debug(clip.format))
	# print(logging.debug(original.format))
	# print(logging.debug(featherMask.format))
	#video = core.std.MaskedMerge(
	#	clipa=original,
	#	clipb=video,
	#	mask=rmask.std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.BoxBlur(vradius = 6,vpasses = 2,hradius 	= 6, hpasses = 2),
	#	first_plane=True
	#)
	#endregion


def parse_weights(orig) -> tuple:

    if not orig:
        raise ValueError('no weights given')

    if isinstance(orig, list):
        return 'divide', {'weights': orig}

    else:
        orig = orig.replace(' ', '')
        orig = orig.split('|')
        func_name = orig[0]

        if not hasattr(weighting, func_name):
            raise ValueError(f'Invalid weighting function: "{func_name}"')

        if len(orig) == 1:
            return func_name, {}

        else:
            params = {}
            for pair in orig[1].split(';'):
                param, value = pair.split('=')
                if param in ('std','std_dev','stddev'):
                    param = 'std_dev'
                # custom func is a string that literal_eval can't parse
                if not (func_name == 'custom' and param == 'func'):
                    try:
                        value = literal_eval(value)
                    except ValueError as v:
                        raise ValueError(f'weighting: invalid value "{value}" '
                                         f'for parameter "{param}"') from v

                params[param] = value

            return func_name, {**params}




def average(clip: vs.VideoNode, weights: list[float], divisor: float  | None = None):
    
    def get_offset_clip(offset: int) -> vs.VideoNode:
        if offset > 0:
            return clip[0] * offset + clip[:-offset]
        elif offset < 0:
            return clip[-offset:] + clip[-1] * (-offset)
        else:
            return clip

    diameter = len(weights)
    radius = diameter // 2

    if divisor is None:
        divisor = sum(weights)

    assert diameter % 2 == 1, "You need an odd number of weights"

    clips = [get_offset_clip(offset) for offset in range(-radius, radius + 1)]

    expr = ""
    # expr_vars = "xyzabcdefghijklmnopqrstuvw"
    expr_vars = []
    for i in range(0, 1024): expr_vars += [f"src{i}"]
    
    for var, weight in zip(expr_vars[:diameter], weights):
        expr += f"{var} {weight} * "

    expr += "+ " * (diameter - 1)
    expr += f"{divisor} /" if divisor != 1 else ""

    clip = core.akarin.Expr(clips, expr)

    return clip





def Smoothing (video, rc):

	def verb(msg):
		if rc['misc']['verbose'] == True:
			print(logging.debug(f' {msg}'))



	if float(ts := rc['timescale']['in']) != 1: # Input timescale, done before interpolation

		video = core.std.AssumeFPS(video, fpsnum=(video.fps * (1 / float(ts))))


	if str((pi := rc['pre interp'])['enabled']) in yes:

		# if path.isfile(pi['ffdata']): # then the user specified the absolute DLL path
		# 	rifelib = pi['ffdata']
		# else: # guess it
		# 	rifelib = path.join(pi['ffdata'], "pkgs/rife-ncnn-vs/vapoursynth64/RIFE.dll")

		# if not path.exists(rifelib):
		# 	raise FileNotFoundError(f"Model directory not found: [{rifelib}]")

		# try:
		# 	core.std.LoadPlugin(path.abspath(pi['rife lib']))
		# except:
		# 	raise vs.Error("Failed to load RIFE plugin lib")

		cMatrix = '709'
			
		try:
			m = video.get_frame(0).props._Matrix
		
			if m == 0:		cMatrix = 'rgb'
			elif m == 4:	cMatrix = 'fcc'
			elif m == 5:	cMatrix = '470bg'
			elif m == 6:	cMatrix = '170m'
			elif m == 7:	cMatrix = '240m'
			elif m == 8:	cMatrix = 'ycgco'
			elif m == 9:	cMatrix = '2020ncl'
			elif m == 10:	cMatrix = '2020cl'
			elif m == 12:	cMatrix = 'chromancl'
			elif m == 13:	cMatrix = 'chromacl'
			elif m == 14:	cMatrix = 'ictcp'

		except:
			cMatrix = '709'

		colRange = 'limited'

		try:
			if video.get_frame(0).props._ColorRange == 0: colRange = 'full'
		except:
			colRange = 'limited'

		if video.format.color_family == vs.YUV:
			video = core.resize.Bicubic(clip=video, format=vs.RGBS, matrix_in_s=cMatrix, range_s=colRange)

		if video.format.color_family == vs.RGB:
			video = core.resize.Bicubic(
				clip=video,
				format=vs.RGBS
			)

		if path.exists(pi['model']):
			if path.isfile(pi['model']):
				raise NotADirectoryError("You need to specify the model's directory, not file")
			model_path = pi['model']
		else:
			model_path = f"{rc['runtime']['smDir']}/models/{pi['model']}"
			
		if not path.exists(model_path):
			raise FileNotFoundError(f"Model directory not found: [{model_path}]")

		if 'mask' in pi.keys():
			if pi['mask'] not in no:
				original = video
				verb(original)

		video = core.rife.RIFE(
			video,
			multiplier=str(pi['factor']).strip('x'),
			model_path=model_path,
			gpu_id=0, gpu_thread=1, tta=False, uhd=False, sc=True
			)

		if 'mask' in pi.keys():
			if pi['mask'] not in no:
				video = Masking(
					clip=video,
					original=original,
					maskDir=constants.MASKDIR,
					maskFn=rc['flowblur']['mask']
				)
    
		video = vs.core.resize.Bicubic(video, format=vs.YUV420P8, matrix_s=cMatrix)
		#verb("the fuck is" + cMatrix)


	if str((ip := rc['interpolation'])['enabled']).lower() in yes:

		if float(video.fps) > ip['fps']:
			raise ValueError("Input FPS greater than specified interpolation FPS")

		if 'mask' in ip.keys():
			if ip['mask'] not in no:
				original = video
        
		useGPU = (ip['use gpu']) in yes

		if str(ip['fps']).endswith('x'): # if multiplier support
			interp_fps = int(video.fps * int((ip['fps']).replace('x','')))
		else:
			interp_fps = int(ip['fps'])

		video = havsfunc.InterFrame(
			video,
			GPU=useGPU,
			NewNum=interp_fps,
			Preset=str(ip['speed']),
			Tuning=str(ip['tuning']),
			OverrideAlgo=int(ip['algorithm'])
		)
		if ip['mask'] not in no:
			video = Masking(
				clip=video,
				original=original,
				maskFn=ip['mask'],
				maskDir= constants.MASKDIR
            )
		

	if float(rc['timescale']['out']) != 1: # Output timescale, done after interpolation
 
		video = core.std.AssumeFPS(video, fpsnum=int(video.fps * float(rc['timescale']['out'])))



	if rc['misc']['dedupthreshold'] not in no:
		video = filldrops.FillDrops(
			video,
			thresh = float((rc['misc']['dedupthreshold']))
		)



	if str(rc['frame blending']['enabled']).lower() in yes:

		# repartition = rc['frame blending']['weighting']

		# if type(repartition) is str:
		# 	partition = repartition.lower()

		frame_gap = int(video.fps / int(rc['frame blending']['fps']))
		blended_frames = int(frame_gap * float(rc['frame blending']['intensity']))

		if blended_frames > 0:
			if blended_frames % 2 == 0: # If number is not odd (requires odd number of frames)
				blended_frames += 1
		
		#region oldweights
		# if type(repartition) is str:
		# 	repartition = rc['frame blending']['weighting'].split(';')[0]
		# 	adv = rc['frame blending']['weighting'].split(';')[1:]
		# 	argcount = len(adv)
		# else:
		# 	repartition = rc['frame blending']['weighting']
		#
		# args = {'frames': blended_frames}
		#
		# # shout out yandere dev for the inspiration 
		# if repartition in ['gaussian','gauss','gaussiansym','gausssym','gaussian_sym']:
		# 	if argcount >= 1:
		# 		args['standard_deviation'] = int(adv[0])
		# 	if argcount >= 2:
		# 		args['bound'] = literal_eval(adv[1].strip())
		# 	if repartition in ['gaussian','gauss']:
		# 		weights = weighting.gaussian(**args)
		# 	else:
		# 		weights = weighting.gaussiansym(**args)
		#
		# elif repartition == 'custom':
		# 	args['func'] = adv[0]
		# 	if argcount >= 2:
		# 		args['bound'] = literal_eval(adv[1].strip())
		# 	weights = weighting.custom(**args)
		#
		# elif repartition == 'pyramid':
		# 	if argcount >= 1:
		# 		if adv[0] in yes:
		# 			args['reverse'] = True
		# 	weights = weighting.pyramid(**args)
		#
		# elif type(repartition) is list:
		# 	weights = weighting.divide(frames=blended_frames, weights=repartition)
		#
		# elif repartition[0] == '[':
		# 	weights = literal_eval(repartition.strip())
		#
		# else:
		# 	if not hasattr(weighting, repartition):
		# 		raise ValueError(f'Weighting {repartition} does not exist')
		# 	else:
		# 		weights = eval(f'weighting.{repartition}(frames={blended_frames})')
		#
		#verb(f"Weights: {weights}")
		#endregion
  
		func, args = parse_weights(rc['frame blending']['weighting'])
  
		verb(f"WEIGHTING: {func}")
		if args != {}:
			verb(f"PARAMS: {args}")
        
		weights = getattr(weighting, func)(blended_frames, **args)
		wa = len(weights)
		verb(f"Weights: {wa}")
		# if len(weights) >= 26:
		# 	verb(f"weights provided: {wa}, using legacy frameblender (tops at 128)")
		# 	video = core.frameblender.FrameBlend(clip=video, weights=weights)
		# elif len(weights) >= 26 and len(weights) <= 31: # Because why not.
		# 	verb(f"weights provided: {wa}, using averageframes (tops at 31)")
		# 	video = core.std.AverageFrames(clip=video, weights=weights)
		# else:
		# 	verb(f"weights provided: {wa}, using fast expr (tops at 25)")
		# 	video = average(clip=video, weights=weights)

		# video = core.frameblender.FrameBlend(clip=video, weights=weights)
		video = average(clip=video, weights=weights)
		video = havsfunc.ChangeFPS(video, int(rc['frame blending']['fps']))

		if 'mask' in ip.keys():
			if ip['mask'] not in no:
				video = Masking(
					clip=video,
					original=original,
					maskDir=constants.MASKDIR,
					maskFn=ip['mask']
				)


	if (flb := rc['flowblur'])['enabled'] not in no:
          
		if rc['flowblur']['amount'] not in no: # If it was 0 or none there there wouldn't be any blurring to do anyways
      
			if 'mask' in flb.keys():
				if flb['mask'] not in no:
						original = video

      
			s = core.mv.Super(video, 16, 16, rfilter=3)
			bv = core.mv.Analyse(s, isb=True, blksize=16, plevel=2, dct=5)
			fv = core.mv.Analyse(s, blksize=16, plevel=2, dct=5)
			video = core.mv.FlowBlur(video, s, bv, fv, blur=(rc['flowblur']['amount']))
   
			if 'mask' in flb.keys():
				if rc['flowblur']['mask'] not in no:
					video = Masking(
						clip=video,
						original=video,
						maskDir=constants.MASKDIR,
						maskFn=rc['flowblur']['mask']
					)
    
				#region oldmask
				# mask = rc['flowblur']['mask']
				# maskDir = constants.MASKDIR
				# verb(f'Mixing in {maskDir} and {mask}..')
	
				# if not path.exists(mask): # Then user specified a relative path, and needs to be verified

				# 	if '.' in mask: # Then the user specified a file extension
				# 		mask = path.join(maskDir, mask)

				# 	else: # Then the user did not specify any image extension and it needs to loop through common exts
				# 		for extension in ['png','jpg','jpeg']:
				# 			if not path.exists(mask):
				# 				mask = path.join(maskDir, f'{mask}.{extension}')

				# 			else:
				# 				continue # Loops until it ends if it found valid mask path
							
				# if not path.exists(mask): # Then even if we did some checks to convert to absolute path it still does not exists
				# 	raise vs.Error(f"The Mask filepath you provided does not exist: {mask}")

				# rmask = core.ffms2.Source(mask)
				# print(logging.debug(mask))
				# print(logging.debug(video.format))
				# print(logging.debug(original.format))
				# print(logging.debug(rmask.format))

				# video = core.std.MaskedMerge(
				# 	clipa=original,
				# 	clipb=video,
				# 	mask=rmask.std.Minimum().std.Minimum().std.Minimum().std.Minimum().std.BoxBlur(vradius = 6,vpasses = 2,hradius 	= 6,hpasses = 2),
				# 	first_plane=True
				# )
				# verb(f'Using mask {mask}')
				# filtered = video.std.Expr(expr=['x 0 -','',''])
				# GW = core.ffms2.Source(mask, cache=False)
				# BW = GW.resize.Bicubic(video.width,video.height, matrix_s='709',format=vs.GRAY8)
				# BW = BW.std.Levels( min_in=0, max_in=235, gamma =0.05, min_out=0, max_out=255)
				# video = havsfunc.Overlay(original, filtered, mask=BW)
				#endregion
	return video