from argparse import ArgumentParser
from sys import argv, exit
from os import path, system#, getcwd
from configparser import ConfigParser
import subprocess
from subprocess import run, PIPE, Popen
from random import choice # Randomize smoothie's flavor
import platform # Get OS (detect win/linux)

if platform.architecture()[0] != '64bit':
    print('This script is only compatible with 64bit systems.')
    exit(1)

isLinux=platform.system() == 'Linux' 
isWin=platform.system() == 'Windows' 
if not isWin and not isLinux:
    print(f'Unsupported OS "{platform.system()}"')
    exit(1)

def pause(text):
    none = input(text)

# Bool aliases
yes = ['True','true','yes','y','1']
no = ['False','false','no','n','0','null','',None]

parser = ArgumentParser()
parser.add_argument("-peek",    "-p",    help="render a specific frame (outputs an image)", action="store", nargs=1, metavar='752',       type=int)
parser.add_argument("-trim",    "-t",    help="Trim out the frames you don't want to use",  action="store", nargs=1, metavar='0:23,1:34', type=str)
parser.add_argument("-dir",              help="opens the directory where Smoothie resides", action="store_true"                                   )
parser.add_argument("-recipe",  "-rc",   help="opens default recipe.ini",                   action="store_true"                                   )
parser.add_argument("--config", "-c",    help="specify override config file",               action="store", nargs=1, metavar='PATH',      type=str)
parser.add_argument("--encoding","-enc", help="specify override ffmpeg encoding arguments", action="store",                               type=str)
parser.add_argument("-verbose", "-v",    help="increase output verbosity",                  action="store_true"                                   )
parser.add_argument("-curdir",  "-cd",   help="save all output to current directory",       action="store_true",                                  )
parser.add_argument("-input",   "-i",    help="specify input video path(s)",                action="store", nargs="+", metavar='PATH',    type=str)
parser.add_argument("-output",   "-o",    help="specify output video path(s)",              action="store", nargs="+", metavar='PATH',    type=str)
parser.add_argument("-vpy",              help="specify a VapourSynth script",               action="store", nargs=1, metavar='PATH',      type=str)
args = parser.parse_args()

if args.dir:
    scriptDir = path.dirname(__file__)
    if isWin:
        run(f'explorer {scriptDir}')
        exit(0)
    elif isLinux:
        print(scriptDir)
        exit(0)
    
if args.recipe:

    recipe = path.abspath(path.join(path.dirname(__file__), "settings/recipe.ini"))

    if path.exists(recipe) == False:
        print("config path does not exist (are you messing with files?), exitting..")
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


conf = ConfigParser()

if args.config:
    config_filepath = path.abspath(args.config[0])
    conf.read(config_filepath)
else:
    config_filepath = path.abspath(path.join(path.dirname(__file__), "settings/recipe.ini"))
    conf.read(config_filepath)

if path.exists(config_filepath) in [False,None]:
    print("config path does not exist, exitting")
    run('powershell -NoLogo')
elif args.verbose:
    print(f"VERBOSE: using config file: {config_filepath}")

if args.input in [no, None]:
    parser.parse_args('-h'.split()) # If the user does not pass any args, just redirect to -h (Help)

round = 0 # Reset the round counter

for video in args.input: # Loops through every single video

    if not args.verbose:
        if isWin:
            clear = 'cls'
        elif isLinux:      
            clear = 'clear'
        run(clear, shell =  True)  

    round += 1

    title = "Smoothie - " + path.basename(video)

    if len(args.input) > 1:
        title = f'[{round}/{len(args.input)}] ' + title

    if isWin:
        system(f"title {title}")

    # Suffix

    if str(conf['misc']['flavors']) in [yes,'fruits']:
        flavors = [
            'Berry','Cherry','Cranberry','Coconut','Kiwi','Avocado','Durian','Lemon','Lime','Fig','Mirabelle',
            'Peach','Apricot','Grape','Melon','Papaya','Banana','Apple','Pear','Orange','Mango','Plum','Pitaya'
        ]
    else:
        flavors = ['Smoothie']

    # Extension

    if args.peek:
        ext = '.png'
    elif conf['misc']['container'] in no:
        ext = path.splitext(video)[1]
    else:
        ext = conf['misc']['container']

    filename = path.basename(path.splitext(video)[0])

    # Directory

    if args.curdir:
        outdir = path.abspath(path.curdir)
    elif conf['misc']['folder'] in no:
        outdir = path.dirname(video)
    else:
        outdir = conf['misc']['folder']

    out = path.join(outdir, filename + f' - {choice(flavors)}{ext}')

    count=2
    while path.exists(out):
        out = path.join(outdir, f'{filename} - {choice(flavors)} ({count}){ext}')
        count+=1
    
    if args.output:
        if ((type(args.input) is list) and (len(args.input) == 1)):
            out = args.output[0]

    # VapourSynth
    if isWin:
        vspipe = path.join(path.dirname((path.dirname(__file__))),'VapourSynth','VSPipe.exe')

    elif isLinux:
        vspipe = 'vspipe'

    if args.vpy:

        if path.dirname(args.vpy[0]) in no:
            
            vpy = path.join( path.dirname(__file__), (args.vpy[0]) )
        else:
            vpy = path.abspath(args.vpy[0])
    else:
        vpy = path.abspath(path.join(path.dirname(__file__),'blender.vpy'))
    
    command = [ # This is the master command, it gets appended some extra output args later down
    f'{vspipe} "{vpy}" --arg input_video="{path.abspath(video)}" --arg config_filepath="{config_filepath}" -c y4m - ',
    f'{conf["encoding"]["process"]} -hide_banner -loglevel error -stats -i - ',
    ]

    if isWin:
        map = '-map 0:v -map 1:a?'
    elif isLinux:
        map = '-map 0:v -map 1:a\?'

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
        print(f"Queuing video: {video}")

    #if run(' '.join(command),shell=True).returncode != 0:
    #    print(f"Something went wrong with {video}, press any key to un-pause")
    #    system('pause>nul')
 
    #run(command[1], stdin = Popen(command[0], stdout = PIPE).stdout)
    #ps = subprocess.Popen((command[0]), stdout=subprocess.PIPE)
    #output = subprocess.check_output((command[1]), stdin=ps.stdout)
    #ps.wait()
    exitcode = run((command[0] + '|' + command[1]), shell=True).returncode
    if exitcode != 0:
        print(f"Something went wrong with {video}, press any key to un-pause")
        if isWin: system('pause>nul')
        exit(1)
 
    system(f"title [{round}/{len(args.input)}] Smoothie - Finished! (EOF)")