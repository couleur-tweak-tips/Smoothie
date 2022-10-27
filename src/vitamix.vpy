import vapoursynth as vs
from vapoursynth import core

from os import path
from sys import path as envpath
if path.dirname(__file__) not in envpath: # Not by default
	envpath.append(path.dirname(__file__)) # From script directory
from helpers import *
from smoothing import Smoothing

from ast import literal_eval
import logging
logging.basicConfig(level=logging.DEBUG)

try:
	global conf
	rc = literal_eval(rc)
except NameError:
	raise vs.Error("Failed to load recipe (not declared with VSPipe --arg?)")
except SyntaxError:
	raise Exception(f"Failed to parse the passed JSON recipe: \n\n{rc}")

def verb(msg):
	if rc['misc']['verbose'] == True:
		print(logging.debug(f' {msg}'))

rt = rc['runtime']
	
if path.splitext(input_video)[1] == '.avi':
	clip = core.avisource.AVISource(input_video)
	clip = core.fmtc.matrix(clip=clip, mat="709", col_fam=vs.YUV, bits=16)
		# If you're gonna bother working with .AVI you're probably using 709 anyways
		# (let me know of one valid case to use this container as input)
	clip = core.fmtc.resampling(clip=clip, css="420")
	clip = core.fmtc.bitdepth(clip=clip, bits=8)
else:
	clip = core.ffms2.Source(source=input_video, cache=False)

fps = int(clip.fps) # It is of "fraction type" per default

def toframes(timecode):
	return round(get_sec(timecode)*60)

if rt['cut type'] in (False, 'split'): # Then there's no cutting/already been handled

	rc['timecodes'] = (1,2) # So the loop does not throw
 
	if ct := rt['cut type'] == 'split':
		s, e = ct['start'], ct['fin']
		clip = core.std.Trim(clip, s, e)
else:
	for i in range(len(tc := rt['timecodes'])):
		s, e = tc[i]['start'], tc[i]['fin']
		if e == 'EOF': e = clip.num_frames-1

		if len(range(e, clip.num_frames-1)) < 1*fps: # If it's less than one second off the end
			logging.info("End of clip was 1 second off the end, joining to EOF")
			e = clip.num_frames-1 # Then remove the end trim, thus rendering till the end of the clip
		verb(f"Trimming from {round(s/fps, 2)} to {round(e/fps, 2)}")
		out = core.std.BlankClip(clip[0])
		if 'toadd' in locals():
			toadd += clip[s:e]
		else:
			toadd = clip[s:e]
	clip = toadd


clip = Smoothing(clip, rc)

# This is what I used for padding, cancelled for now
# if rc['runtime']['type']: # If you're doing trimming
# 	out += toadd
# 	if not rt['timecodes'][i] == rt['timecodes'][i]: # it's not the last
# 		length = (toframes(rt['timecodes'][i+1]['start']) - e) * rc['frame blending']['fps'] // int(clip.fps)
# 		out += core.std.BlankClip(clip[0], length=(length))
# 		logging.debug(f"ERR:{(get_sec(rt['timecodes'][i+1]['start']) - out.num_frames/(rc['frame blending']['fps']))}")
# else:
# 	out = toadd 

clip.set_output()
