from helpers import *
from os import path, system, listdir
from glob import glob as resolve
from random import choice # Randomize smoothie's flavor
from configparser import ConfigParser
from subprocess import run
from sys import argv, exit

def voidargs(args):
    if args.dir:
        scriptDir = path.dirname(argv[0])
        if isWin:
            run(f'explorer {scriptDir}')
            exit(0)
        elif isLinux:
            print(scriptDir)
            exit(0)

    if args.recipe:
        recipe = path.abspath(path.join(path.dirname(argv[0]), "settings/recipe.ini"))
        if path.exists(recipe) == False:
            print("recipe (config) path does not exist (are you messing with files?), exitting..")
            pause()
            exit(1)
        if isWin:
            run(path.abspath(recipe), shell=True)
            exit(0)
        elif isLinux:
            print('What code editor would you like to open your recipe with? (e.g nano, vim, code)')
            print(f'This file is located at {recipe}')
            editor = input('Editor:')
            run(f'{path.abspath(editor)} {path.abspath(recipe)}', shell=True)

def runvpy(parser):
    args = parser.parse_args()
    
    if args.input in [no, None]:
        parser.print_help() # If the user does not pass any args, just redirect to -h (Help)
        exit(0)

    if isWin and not args.verbose:
        import win32gui
        import win32con
        hwnd = win32gui.GetForegroundWindow()
        win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,1000,200,0)
    
    # This is done in order to be "directory agnostic"
    # Just read it as, if I'm in a folder called src, do cd ..
    parent, dir = path.split( path.split(path.abspath(argv[0]))[0] )
    if dir == 'src':
        step = path.join(parent, path.basename(argv[0]))
        if args.verbose: print(f'Stepping down from {argv[0]} to {step}')
        argv[0] = step
        
    voidargs(args)

    conf = ConfigParser()
    
    if args.config:
        config_filepath = path.abspath(args.config)
        conf.read(config_filepath)
    else:
        config_filepath = path.abspath(path.join(path.dirname(argv[0]), "settings/recipe.ini"))
        conf.read(config_filepath)
        
    mask_directory = path.abspath(path.join(path.dirname(argv[0]), "masks"))
    if not path.exists(mask_directory):
        print(f"mask folder does not exist, exitting (looked for {mask_directory})")
        pause(); exit()


    if not path.exists(config_filepath):
        print(f"config path does not exist, exitting (looked for {config_filepath})")
        pause(); exit()
    if args.verbose:
        print(f"VERBOSE: using config file: {config_filepath}")

    round = 0
    for video in args.input:

        if not args.verbose:
            system('cls' if isWin else 'clear') # cls on windows, clear on anything else 

        if '*' in video: # If filepath contains wildcard, resolve them
            for file in resolve(video):
                if path.isfile(file):
                    args.input.append(file)
            continue
        elif not path.exists(video):
            print(f"Filepath {video} does not exist, skipping..")
            continue

        if path.isdir(video):
            for file in listdir(video):
                file = path.join(video, file)
                if path.isfile(file):
                    args.input.append(file)
            continue

        video = path.expandvars(
            path.abspath(video)
            )
        
        if isWin:
            round += 1
            title = "Smoothie - " + path.basename(video)
            if len(args.input) > 1:
                title = f'[{round}/{len(args.input)}] ' + title
            system(f"title {title}")

        
        flavors = [
            'Berry','Cherry','Cranberry','Coconut','Kiwi','Avocado','Durian','Lemon','Lime','Fig','Mirabelle',
            'Peach','Apricot','Grape','Melon','Papaya','Banana','Apple','Pear','Orange','Mango','Plum','Pitaya'
        ] if str(conf['misc']['flavors']) in [yes,'fruits'] else ['Smoothie']

        if args.curdir:
            outdir = path.abspath(path.curdir)
        elif conf['misc']['folder'] in no:
            outdir = path.abspath(path.dirname(video))
        else:
            outdir = conf['misc']['folder']
            

        if args.peek:
            ext = '.png'
        elif conf['misc']['container'] in no:
            ext = path.splitext(video)[1]
        else:
            ext = conf['misc']['container']
        
        filename = path.splitext(path.basename(video))[0]

        out = path.join(outdir, f'{filename} - {choice(flavors)}{ext}')

        count=2
        while path.exists(out):
            out = path.join(outdir, f'{filename} - {choice(flavors)} ({count}){ext}')
            count+=1
        
        if args.output:
            if ((type(args.input) is list) and (len(args.input) == 1)):
                out = args.output[0]
                       
        if isWin:
            vspipe = path.join(path.dirname(path.dirname(argv[0])),'VapourSynth','VSPipe.exe')
        elif isLinux:
            vspipe = 'vspipe'
                    
        if args.vpy:
            if path.dirname(args.vpy[0]) in no:
                vpy = path.join( path.dirname(argv[0]), (args.vpy[0]) )
            else:
                vpy = path.abspath(args.vpy[0])
        else: vpy = path.abspath(path.join(path.dirname(argv[0]),'vitamix.vpy'))

        command = [ # This is the master command, it gets appended some extra output args later down
        f'{vspipe} "{vpy}" --arg input_video="{path.abspath(video)}" --arg mask_directory="{mask_directory}" --arg config_filepath="{config_filepath}" -y - ',
        f'{conf["encoding"]["process"]} -hide_banner -loglevel error -stats -i - ',
        ]
        
        map = '-map 0:v -map 1:a?' if isWin else '-map 0:v -map 1:a\?' # Mapping the audio's file, Linux needs an escape character

        if args.peek:
            frame = int(args.peek[0]) # Extracting the frame passed from the singular array
            command[0] += f'--start {frame} --end {frame}'
            command[1] += f' "{out}"' # No need to specify audio map, simple image output
        elif args.trim:
            command[0] += f'--arg trim="{args.trim}"'
            command[1] += f'{conf["encoding"]["args"]} "{out}"'
        else:
            # Adds as input the video to get it's audio tracks and gets encoding arguments from the config file
            command[1] += f'-i "{path.abspath(video)}" {map} {conf["encoding"]["args"]} "{out}"'

        if args.verbose:
            command[0] += ' --arg verbose=True'
            for cmd in command: print(f"{cmd}\n")
            print(f"Queuing video: {video}, vspipe is {vspipe}")
            
        exitcode = run((command[0] + '|' + command[1]), shell=True).returncode
        if exitcode != 0 and not args.verbose:
            print(f"Something went wrong with {video}")
            pause() ; exit(1)

    system(f"title [{round}/{len(args.input)}] Smoothie - Finished! (EOF)")