ver='0.7.1'
from sys import argv
from os import path
from helpers import *
from glob import glob as resolve
from random import choice # Randomize smoothie's flavor
from subprocess import run, Popen, PIPE
from yaml import safe_load
from json import loads
import constants
from typing import Any, Iterable
import colors
from re import match

if constants.ISWIN: # File dialog, file opener
	import tkinter as tk
	from tkinter import filedialog # Pick a file
	from win32gui import GetForegroundWindow, SetWindowPos # Move terminal to top left
	from win32con import HWND_TOPMOST # Make window stay on top
	hwnd = GetForegroundWindow()

def parse_ez_enc_args(args) -> str:
	
	def next_in(i: Iterable, idx: int, default: Any = '') -> Any:
		try:
			return i[idx + 1]
		except IndexError:
			return default

	args = args.strip().casefold().split(' ') 

	for i, word in enumerate(args):
		word = word.lower()
		if word == "avc": word = "h264"
		if word == "hevc": word = "h265"

		if 'x26' in word: # x265 or x264
			args[i] = constants.ENC_PRESETS['h26' + word[3]]['cpu'] #+ ' -c:a copy'
			
		elif (std := word) in constants.ENC_PRESETS: # valid standard
			if (enc := next_in(args, i)) in constants.ENC_PRESETS[std]: # valid encoder
				args[i] = constants.ENC_PRESETS[std][enc] #+ ' -c:a copy'
				args.pop(i + 1)
		#print(f"tf is {i} and {word}")
		if word.lower() in ('upscale', '4k'):
			args.insert(i, '-vf scale=-2:2160:flags=neighbor')
   
			if not match(r".* -vf| -lavfi| -filter_complex| -pix_fmt.*", args[0]):
				args[i] += ' -pix_fmt yuv420p10le'
			args.pop(i + 1)
	
	print(args)
	if not match(r"\-acodec|\-c:a|\-codec:a|\-an", ' '.join(args)):
		print("adding audio")
		args.append(' -c:a copy')

	return ' '.join(args)

def voidargs(args) -> None:
	if args.dir:
		scriptDir = path.dirname(argv[0])
		if constants.ISWIN:
			Popen(f'explorer {scriptDir}')
			exitSm(0, args)
		elif constants.ISLINUX:
			print(scriptDir)
			exitSm(0, args)

	if args.recipe:
		recipe = path.join(constants.SMDIR, constants.DEFAULT_RECIPE)
		if path.exists(recipe) == False:
			print(f"Looking for recipe path {recipe}")
			print("recipe (config) path does not exist (are you messing with files?), exitting..")
			exitSm(1, args)
		if constants.ISWIN:
			Popen(path.abspath(recipe), shell=True)
			exitSm(0, args)
		elif constants.ISLINUX:
			print('What code editor would you like to open your recipe with? (e.g nano, vim, code)')
			print(f'This file is located at {recipe}')
			editor = input('Editor:')
			Popen(f'{path.abspath(editor)} {path.abspath(recipe)}', shell=True)
			exitSm(0, args)

def buildcmd(args) -> list: # Builds up a command from all recipe
	
	voidargs(args) # All args that result in not continuing the script
	
	def verb(message):
		if args.verbose:
			print("VERBOSE: " + message)
	
	if args.userecipe:
		config_filepath = path.expandvars(path.abspath(args.userecipe))
	else:
		config_filepath = path.join(constants.SMDIR, constants.DEFAULT_RECIPE) # ../recipe.yaml
	
	rc = {}
	if not path.exists(config_filepath):
		print(f"Config filepath {config_filepath} does not exist")
		exitSm(1, args)
	else:
		verb(f"RECIPE: {config_filepath}")
		with open(config_filepath, 'r') as file:
			rc = safe_load(file)
	
	rc['encoding']['args'] = parse_ez_enc_args(rc['encoding']['args'])

	if args.verbose or rc['misc']['verbose'] in yes: # Making sure they're both turned on
		rc['misc']['verbose'] = True
		args.verbose = True

	if args.cui and rc['misc']['stay on top'] in yes:
		SetWindowPos(hwnd,HWND_TOPMOST,0,0,1000,60,0) # Move and resize terminal to the top left of the screen


	if args.override:
		for override in args.override:
			print("Using override(s):", override)
			category, key, value = override.split(';')
			rc[category][key] = value

	for effect in ['frame blending', 'interpolation', 'flowblur']:
		if rc[effect]['enabled'] not in no and rc[effect]['enabled'] not in yes:
			print(f"Effect {effect} has wrong true/false value: {rc[effect]['enabled']}")
			exitSm(1, args)

	if not path.exists(constants.MASKDIR):
		print(f"Masks directory not found (expected at {constants.MASKDIR}")
		exitSm(1, args)
	else: verb(f"smDir: {constants.SMDIR}")
	
 	# args.input is -i, the normal way of passing files via CLI/Send To
	# -cui means the user did not use the CLI, but a send to/start menu shortcut (both startmenu & sendto are "sm -cui -i ")
	if not args.input and not args.cui and not args.json: # if args.json then input paths are passed in the json string
		colors.printc(f"@LBLUESmoothie \33[38;5;244m{ver}&RESET, add the \33[38;5;244m-h&RESET arg for more info on the CLI\nor go to @LBLUE&URLhttps://github.com/couleur-tweak-tips/Smoothie/wiki&RESET")
		#parser.print_help() # If the user does not pass any args, just redirect to-h (Help)
		exitSm(0, args)
	elif constants.ISWIN and not args.input and args.cui and not args.json:
		root = tk.Tk()
		none = root.withdraw() # Redirected to none to get supressed from stdout
		root.iconbitmap(path.dirname(argv[0]) + '/sm.ico')
		
		returned = filedialog.askopenfilenames(
			title="Select video(s) to queue to Smoothie",
			filetypes= (("Video files", "*.mp4 *.mkv *.webm *.avi"),("All files", "*.*"))
		)
		if returned in no: exitSm(1, args)
		else:
			args.input = returned

	elif args.input and not args.json: input_info = args.input
	elif args.json:
		input_info = list(loads(args.json.replace("'",'"')))
	else:
		print("Could not resolve input selection")
		exitSm(1, args)

	#input_info = {}
	videos = list() # This will end up containing paths, and trimming points if given
	if args.trim and type(input_info[0]) == dict: # Then it is an array of not unique single filenames with start and fin points
		# It'll need to be properly restructured into dicts with one video in each with 'timecodes' containing all of the same video's cuts
		timecodes = dict() # Unique timecodes will be appended
		for cut in input_info:
			if cut['path'] not in timecodes.keys(): # Then create timecodes["D:\video\blabla.mp4"]
				timecodes[(cut['path'])] = dict()
				timecodes[(cut['path'])]['timecodes'] = list()
			timecodes[(cut['path'])]['timecodes'].append({ # Only append the start and fin, filename unneeded
				"start": cut["start"],
				"fin": cut["fin"]
			})
		for filepath in timecodes.keys(): # Restructure it into videos
			videos.append({
				"path": filepath,
				"timecodes": timecodes[filepath]['timecodes']
			})
	elif args.input:
		videos = list()
		for vid in input_info:
			videos.append({
				"path": vid
			})

	if rc['misc']['verbose']:
		print(
f"""
INPUT_INFO (what was received from args):
{input_info}

VIDEOS (what Smoothie made out of -json):
{videos}
""")

	#region oldtrim
		# print("INPUT_INFO (what was received from args):")
		# print(	input_info)
		# print("")
		# print("VIDEOS (what Smoothie made out of -json):")
		# print(	videos)
	# for vid in input_info:
	# 	if type(vid) == str:
	# 		videos.append({
	# 			"path": vid
	# 		})
	# 	if args.trim and type(vid) == dict:
	# 		timecodes = dict()
	# 		for cut in vid:
			# timecodes = list()
			# for cut in vid:
			# 	timecodes.append({
			# 		"start": cut["start"]
			# 		"fin": cut["fin"]
			# 	})
			# 	videos.append({
			# 		"path":		cut['filename'],
			# 		"timecodes" : timecodes
			# 	})
		
	# if not args.json:
	# 	verb("we do be parsing input as input string")
	# 	for filepath in input_info: # It's an object because it can either be a simple path string of a dict containing trimming points
	# 		verb("parsing input as string")
	# 		videos.append({"path": filepath})

	# elif args.padding or args.trim:
	# 	verb("We either padding or trimming my g")

	# 	if 'filename' in input_info[0].keys():
	# 		print("y1");exit()
	# 		for cut in input_info:
	# 			videos.append({
	# 				"path":		cut['filename'],
	# 				"start":	cut['start'],
	# 				"fin":		cut['fin']
	# 			})
	# 	else:
	# 		videos.append ({
	# 			"path": args.input[0], # First because it's a list per default only one is allowed anyways
	# 			"timecodes": args.json
	# 		})
 
	# elif args.split:
	# 	verb("We splittin in here")
	# 	for timecode in input_info:
	# 		videos.append ({
	# 			"path":		args.input[0],
	# 			"start":	timecode['start'],
	# 			"fin":		timecode['fin']
	# 		})
	# else:
	# 	print("If you pass -json you must also pass -split, -trim or -padding")
	# 	exitSm(1, args)
	#endregion
	
	EncArgs = rc['encoding']['args']
	if EncArgs in no:
		print("You did not specify any encoding arguments, using the default but slow 'H264 CPU' preset")
		rc['encoding']['args'] = "H264 CPU" # Modifying it on the fly when recipe has been loaded into the ram
	elif EncArgs == "H264 GPU":
		print("H264 CPU encodes your video in x264, 'H264 GPU' does not mean anything, replace GPU by NVENC (for NVIDIA cards), AMF (for AMD cards), and QuickSync (for Intel iGPUs/cards)")
	parsedArgs = EncArgs.split(' ')
	enc, std = False, False
	for arg in parsedArgs: # No maidens nor cases
		if arg in ['NV','NVENC','NVIDIA']: 		enc = 'NVENC'
		if arg in ['AMD','AMF']:				enc = 'AMF'
		if arg in ['Intel','QuickSync','QSV']:	enc = 'QuickSync'
		if arg == 'CPU':						enc = 'CPU'
		if arg == 'x264':						enc = 'CPU'; std = 'H264'
		if arg == 'x265':						enc = 'CPU'; std = 'H265'

		if arg in ['H264','H.264','AVC']:		std = 'H264'
		if arg in ['HEVC','H.265','HEVC']: 		std = 'H265'

	if enc and std:
		rc['encoding']['args'] = constants.ENC_PRESETS[std.lower()][enc.lower()] # This makes use of the EncPresets dictionary declared above
		if 'Upscale' in parsedArgs or '4K' in parsedArgs: rc['encoding']['args'] += ' -vf zscale=3840:2160:f=point'
		verb(f"EncArgs: {rc['encoding']['args']}")
	# Uncomment this block if you don't want custom encoding arguments
 	#else:
	#	print(f"Failed to parse arguments: {rc['encoding']['args']}")
	#	exitSm(1, args)

	iterations = 0
	commands = list()
	for video in videos:

		rc['runtime'] = {}
 			# Everything in here is passed to VapourSynth, not rewritten back to the recipe (nothing gets)
			# It gets reset at each command since trimming points may be different
		if args.json:
			rc['runtime'].update(video) # Merges them
			if args.split: rc['runtime']['cut type']		= "split"
			elif args.padding: rc['runtime']['cut type']	= "padding"
			elif args.trim: rc['runtime']['cut type']		= "trim"
		else:
			rc['runtime']['cut type']						= False
		filepath = video['path']
	
		if not path.exists(filepath):
			print(f"{filepath} does not exist, skipping")
			continue

		iterations += 1
		title = f"Smoothie {ver} - " + path.basename(filepath)
		if len(videos) > 1:
			title = f'[{iterations}/{len(videos)}] ' + title
		if args.padding:	title += " (Padding)"
		if args.trim:		title += " (Trimming)"
		if args.split:		title += " (Splitting)"

		if not args.json:

			if rc['misc']['suffix'] == 'fruits':
				USE_FRUITS = True
				suffix = choice(constants.FRUITS)
			elif rc['misc']['suffix'] == 'detailed':
				suffix = ''
				if rc['interpolation']['enabled'] in yes:
					suffix += f"{rc['interpolation']['fps']}fps"
				if rc['frame blending']['enabled'] in yes:
					suffix += f" ({rc['frame blending']['fps']}, {float(rc['frame blending']['intensity'])}"
				if rc['flowblur']['enabled'] in yes:
					suffix += f", bf@{rc['flowblur']['amount']}"
				if "(" in suffix: suffix += ")"
				suffix += ' '
			else:
				suffix = rc['misc']['suffix']
	
		else: suffix = 'SM'
		

		if args.outdir or args.outdir == '': # Works both as a str and a switch
		
			if args.outdir == '': # User simply specified the argument, but didn't give a value, so it defaults to current working directory
				verb("Setting output to cwd")
				outdir = path.abspath(path.curdir) 
		
			else: # Else if speccified use what the user provided
				outdir = path.abspath(args.outdir)
		
		elif rc['misc']['folder'] in no: # If no specified output directory in config, use also the input directory as output 
			outdir = path.abspath(path.dirname(filepath))
		else: # Else finally use conf
			outdir = rc['misc']['folder']

		if args.peek:
			ext = '.png'
		elif rc['misc']['container'] in no:
			ext = path.splitext(filepath)[1]
		else:
			cont = rc['misc']['container']
			ext = cont if cont.startswith('.') else f'.{cont}'

		filename = path.splitext(path.basename(filepath))[0] # get 'video' out of D:/video.mp4
		if rc['misc']['prefix']:
			filename = f'{rc["misc"]["prefix"]}{filename}'

		if args.output:
			if len(args.input) > 1:
				print("Only a single input is supported when selecting an output file")
				exitSm(1, args)
			out = args.output[0]
		elif not args.output:
			out = path.join(outdir, f'{filename} ~ {suffix}{ext}')
			count=2 # Start at "output file (2).mp4", like when copying files on Windows
			while path.exists(out):
				out = path.join(outdir, f'{filename} ~ {suffix}({count}){ext}')
				count+=1

		# Go from
		# /Smoothie/src/main.py
		# To
		# /VapourSynth/VSPipe.exe
		if constants.ISWIN:
			vspipe = path.join(path.dirname(constants.SMDIR),'VapourSynth\\VSPipe.exe')
		elif constants.ISLINUX:
			vspipe = constants.VSPIPE_PATH_LINUX

		if args.vpy:
			if path.dirname(args.vpy[0]) == '': # assumes its in in /src/
				vpy = path.join(constants.SRCDIR, args.vpy[0] )
			else:
				vpy = path.abspath(args.vpy[0])
		else: vpy = path.abspath(path.join(constants.SRCDIR, constants.DEFAULT_VPY_NAME))

		if args.verbose: # Propagate verbosity to VapourSynth
			rc['misc']['verbose'] = True

		rc['runtime']['smDir'] = constants.SMDIR

		cmd = { # This is the master command that will be appended upon
			"vs": f'"{vspipe}" "{vpy}" --arg input_video="{path.abspath(filepath)}" -y - --arg rc="{rc}"',
			"ff": f'{rc["encoding"]["process"]} -hide_banner -loglevel error -stats -stats_period 0.15 -i - ',
			"title": title,
			"path": filepath,
			"recipe": rc
		}

		audio_map = '-map 0:v -map 1:a?' if constants.ISWIN else '-map 0:v -map 1:a\?'
			# This puts the audio's file on the audio-less output file, Linux needs an escape character

		if args.peek:
			frame = int(args.peek[0]) # Extracting the frame passed from the singular array
			cmd['vs'] += f'--start {frame} --end {frame}'
			cmd['ff'] += f' "{out}"' # No need to specify audio map, simple image output
		elif args.tonull:
			cmd['ff'] += f' -f null NUL'
		elif args.tompv:
			cmd['ff'] = rc['misc']['mpv bin'] + ' -' # Overwrite it 😋
		elif not args.json or args.padding:
			
			cmd['ff'] += f'-i "{path.abspath(filepath)}" {audio_map} {rc["encoding"]["args"]} "{out}"'
				# Inputs original video to take it's audio, VapourSynth does not take/return any
			
			for audioarg in ('-c:a','-an','-codec:audio'): # Then copy audio, it defaults to aac
				if audioarg not in rc["encoding"]["args"]:
					cmd['ff'] += " -c:a copy"
					break
		elif args.json:
			cmd['ff'] += f' {rc["encoding"]["args"]} "{out}"'


		if 'ffmpeg' in cmd['ff']:
			# This will force the output video's color range to be Full
			range_proc = run(f'ffprobe -v error -show_entries stream=color_range -of default=noprint_wrappers=1:nokey=1 "{video}"', stdout=PIPE, stderr=PIPE, universal_newlines=True)
			if range_proc.stdout == 'pc\n':
				if '-vf ' in cmd['ff']:
					cmd['ff'] = cmd['ff'].replace('-vf ','-vf scale=in_range=full:out_range=limited,') # Very clever video filters appending
				else:
					cmd['ff'] += ' -vf scale=in_range=full:out_range=full '

		commands.append(cmd) # Command ended building
	return commands # buildcmd