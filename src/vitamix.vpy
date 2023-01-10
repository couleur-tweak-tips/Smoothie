import vapoursynth as vs
from vapoursynth import core
from math import floor

from os import path
from sys import path as envpath
if path.dirname(__file__) not in envpath: # Not by default
	envpath.append(path.dirname(__file__)) # From script directory
from helpers import *
from smoothing import Smoothing

from ast import literal_eval
import logging
logging.basicConfig(level=logging.DEBUG)

import json

try:
	rc = literal_eval(rc)#.decode('utf-8'))

except NameError:
	raise vs.Error("Failed to load recipe (not declared with VSPipe --arg?)")
except SyntaxError:
	raise Exception(f"Failed to parse the passed JSON recipe: \n\n{rc}")

def verb(msg):
	if rc['misc']['verbose'] == True:
		print(logging.debug(f' {msg}'))

rt = rc['runtime']
	
clip = core.lsmas.LWLibavSource(source=input_video, cache=1, prefer_hw=3)

clip = Smoothing(clip, rc)

fps = float(clip.fps) # It is of "fraction type" per default

def toframes(timecode):
	return floor(get_sec(timecode)*fps)

verb(f"OG clip length: {clip.num_frames}")
blackClip = core.std.BlankClip(clip, length=clip.num_frames)

match rt['cut type']:
    
	case "trim":
		for i in range(len(tc := rt['timecodes'])):
      
			s, e = tc[i]['start'], tc[i]['fin']
			if e == 'EOF':
				e = clip.num_frames-1
			verb(f"Index #{i}: from {s} to {e}")
			s, e = toframes(s), toframes(e)

			if i == 0:  
				toadd = clip[s:e]
			else:
				if e == 'EOF':
					toadd += clip[s:]
				else:
					toadd += clip[s:e]

		clip = toadd

	case "padding":
		Mappings = ""
		for i in range(len(tc := rt['timecodes'])):
		
			dStart, dEnd = tc[i]['start'], tc[i]['fin']
			verb(f"Keeping clip #{i} from {dStart} to {dEnd}")
	
			s = round(toframes(tc[i]['start']) - (0.1 * fps))
			e = round(toframes(tc[i]['fin']) + (0.1 * fps))
	
			Mappings += f"[{max(s-1, 0)} {min(e, clip.num_frames)-1}] "
		verb(f"Mappings: {Mappings}")
		clip = core.remap.ReplaceFramesSimple(blackClip, clip, mappings=Mappings.rstrip(' '))
  
  
	case "split":
			s, e = toframes(rt['start']), toframes(rt['fin'])
			clip = core.std.Trim(clip, s, e)

clip.set_output()
