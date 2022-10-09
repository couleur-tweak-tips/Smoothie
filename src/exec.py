from sys import argv, exit
from os import path, system, listdir
from helpers import *
from bar import * # Progress bar
from glob import glob as resolve
from random import choice # Randomize smoothie's flavor
from subprocess import run, Popen
from yaml import safe_load

if isWin:
    import tkinter as tk
    from tkinter import filedialog # Pick a file
    from win32gui import GetForegroundWindow, SetWindowPos # Move terminal to top left
    from win32con import HWND_TOPMOST # Make window stay on top
    hwnd = GetForegroundWindow()

def voidargs(args):
    if args.dir:
        scriptDir = path.dirname(argv[0])
        if isWin:
            Popen(f'explorer {scriptDir}')
            exit(0)
        elif isLinux:
            print(scriptDir)
            exit(0)

    if args.recipe:
        recipe = path.abspath(path.join(path.dirname(argv[0]), "settings/recipe.yaml"))
        if path.exists(recipe) == False:
            print(f"Looking for recipe path {recipe}")
            print("recipe (config) path does not exist (are you messing with files?), exitting..")
            pause()
            exit(1)
        if isWin:
            Popen(path.abspath(recipe), shell=True)
            exit(0)
        elif isLinux:
            print('What code editor would you like to open your recipe with? (e.g nano, vim, code)')
            print(f'This file is located at {recipe}')
            editor = input('Editor:')
            Popen(f'{path.abspath(editor)} {path.abspath(recipe)}', shell=True)
            exit(0)

def runvpy(parser):
    
    args = parser.parse_args()

    voidargs(args)

    if args.override:
        for override in args.override:
            category, key, value = override.split(';').split(';')
            conf[category][key] = value

    if args.input in [no, None] and not args.cui:
        if args.trim:
            if 'filename' in args.trim[0]:
                videos = loads(args.trim[0])
        else:
            print("Smoothie 0.7, add the -h arg for more info on the CLI\nor go to https://github.com/couleur-tweak-tips/Smoothie/wiki")
            #parser.print_help() # If the user does not pass any args, just redirect to -h (Help)
            exit(0)
    elif isWin and args.input in [no, None] and args.cui:
        root = tk.Tk()
        none = root.withdraw()
        root.iconbitmap(path.dirname(argv[0]) + '/src/sm.ico')
        
        file_path = filedialog.askopenfilenames(
            
            title="Select video(s) to queue to Smoothie",
            filetypes= (("Video files", "*.mp4 *.mkv *.webm *.avi"),
                        ("All files", "*.*"))
        )
        if file_path in [None,'']: exit(1)
        if not args.input: args.input = []
        for vid in file_path: args.input.append(vid)
    else:
        videos = args.input
    
    if args.config: config_filepath = path.abspath(args.config)
    else: config_filepath = path.abspath(path.join(path.dirname(path.dirname(argv[0])), "settings/recipe.yaml"))

    with open(config_filepath, 'r') as file:
        conf = safe_load(file)

    if args.cui and conf['misc']['stay on top'] in yes:
        SetWindowPos(hwnd,HWND_TOPMOST,0,0,1000,60,0)

    if not args.input and not args.trim:
        print("Failed to gather input videos")
        exit(1)     

        
    mask_directory = path.abspath(path.join(path.dirname(path.dirname(argv[0])), "masks"))
    if not path.exists(mask_directory):
        print(f"mask folder does not exist, exitting (looked for {mask_directory})")
        pause(); exit()


    if not path.exists(config_filepath):
        print(f"config path does not exist, exitting (looked for {config_filepath})")
        pause(); exit()
    if args.verbose:
        print(f"VERBOSE: using config file: {config_filepath}")
        
        
    EncPresets = { # Same setup as TweakList's Get-EncArgs
        'H264': {
            'NVENC' :       "-c:v h264_nvenc -preset p7 -rc vbr -b:v 250M -cq 18",
            'AMF' :         "-c:v h264_amf -quality quality -qp_i 12 -qp_p 12 -qp_b 12",
            'QuickSync' :   "-c:v h264_qsv -preset veryslow -global_quality:v 15",
            'CPU' :         "-c:v libx264 -preset slower -x264-params aq-mode=3 -crf 15 -pix_fmt yuv420p10le"
        },
        'H265' : {
            'NVENC' :       "-c:v hevc_nvenc -preset p7 -rc vbr -b:v 250M -cq 18",
            'AMF' :         "-c:v hevc_amf -quality quality -qp_i 16 -qp_p 18 -qp_b 20",
            'QuickSync' :   "-c:v hevc_qsv -preset veryslow -global_quality:v 18",
            'CPU' :         "-c:v libx265 -preset slow -x265-params aq-mode=3 -crf 18 -pix_fmt yuv420p10le"
        }
    }
    passedArgs = conf['encoding']['args'].split(' ') # Make an array that contains what the user passed

    enc, std = False, False
    for arg in passedArgs: # No maidens nor cases
        if arg in ['NV','NVENC','NVIDIA']: enc = 'NVENC'
        if arg in ['AMD','AMF']:           enc = 'AMF'
        if arg in ['Intel','QuickSync','QSV']:   enc = 'QuickSync'
        if arg == 'CPU':                   enc = 'CPU'
        if arg == 'x264':                  enc = 'CPU'; std = 'H264'
        if arg == 'x265':                  enc = 'CPU'; std = 'H265'
        if arg in ['H264','H.264','AVC']:  std = 'H264'
        if arg in ['HEVC','H.265','HEVC']: std = 'H265'

    if enc and std:
        conf['encoding']['args'] = EncPresets[std][enc] # This makes use of the EncPresets dictionary declared above
        if 'Upscale' in passedArgs or '4K' in passedArgs: conf['encoding']['args'] += ' -vf zscale=3840:2160:f=point'
    
    for i in videos: # This loop ONLY converts all paths to literal, the actual for loop that does all the process is later down
        i =- 1
        video = videos[i]
        if type(video) is not str: video = video['filename']
        if '*' in video: # If filepath contains wildcard, resolve them
            for file in resolve(video):
                if path.isfile(file):
                    args.input.append(file)
            continue
        elif not path.exists(video):
            print(f"Filepath {video} does not exist, skipping..")
            args.input.remove(video)
            continue

        elif path.isdir(video):
            for file in listdir(video):
                file = path.join(video, file)
                if path.isfile(file):
                    args.input.append(file)
            continue
        
    if not args.input and not args.trim:
        print("Failed to gather input videos")
        pause()
        exit(1)
    
    # if args.trimmer:
        
    #     commands = []

    #     for video in args.input:
    #         if isWin: system(f'title Smoothie Trimmer - {path.basename(video)}')
    #         print("Give a timestamp to trim from your clips from/to, you can specify multiple parts, example:")
    #         print("23 to 1:34, 1:50 to 2:04, 3:47 to 1:04:01")
    #         config_dir = path.join(path.dirname(argv[0]),'mpv')
    #         proc = Popen(f'mpv --config-dir="{config_dir}" --really-quiet -vf fps=120 "{path.abspath(video)}"')
            
    #         trims = str(input('Timecode(s): ').strip().replace('to', ';').replace(' ','').split(','))
            
    #         while 'to' not in trims and ';' not in trims:
    #             print("Please give time codes separated by ; or ' to '")
    #             trims = input('Timecode(s): ').strip().replace('to', ';').replace(' ','').split(',')[0]
            
    #         for trim in trims:
    #             start, end = trim.split(';')
    #             commands += [f'sm -i "{video}" -frametrim {get_sec(start)},{get_sec(end)}']
    #         proc.kill()
            
    #     for cmd in commands:
    #         print(cmd)
    #         returncode = run(cmd).returncode
    #         if returncode != 0:
    #             raise Exception(f'Failed to trim video with command {cmd}')

    #     exit(0)
    
    conf['TEMP'] = {}

    iterations = 0
    for i in range(len(videos)): # Second loop, now that videos have been expanded
        #i =- 1
        video = videos[i]
        if type(video) is dict: 
            trims = video
            video = video['filename']
        else:
            trims = {}

        video = path.expandvars(
            path.abspath(video)
        )
        
        if isWin:
            iterations += 1
            title = "Smoothie - " + path.basename(video)
            if len(videos) > 1:
                title = f'[{iterations}/{len(videos)}] ' + title
            system(f"title {title}")
        
        if conf['misc']['suffix'] == 'fruits':
            suffix = choice([
            'Berry','Cherry','Cranberry','Coconut','Kiwi','Avocado','Durian','Lemon','Lime','Fig','Mirabelle',
            'Peach','Apricot','Grape','Melon','Papaya','Banana','Apple','Pear','Orange','Mango','Plum','Pitaya'
        ])
        elif conf['misc']['suffix'] == 'detailed':
            suffix = ''
            if conf['interpolation']['enabled']:
                suffix += f"{conf['interpolation']['fps']}fps"
            if conf['frame blending']['enabled']:
                suffix += f" ({conf['frame blending']['fps']}, {float(conf['frame blending']['intensity'])}"
            if conf['flowblur']['enabled']:
                suffix += f", bf@{conf['flowblur']['amount']}"
            if "(" in suffix: suffix += ")"
            suffix += ' '
            

        if args.outdir:
            if args.outdir == '': # User simply specified the argument, but didn't give a value, so it defaults to current working directory
                outdir = path.abspath(path.curdir)
            else: # Else if speccified use what the user provided
                outdir = path.abspath(args.outdir)
        elif conf['misc']['folder'] in no: # If no specified output directory in config, use also the input directory as output 
            outdir = path.abspath(path.dirname(video))
        else: # Else finally use conf
            outdir = conf['misc']['folder']
            
        if args.peek:
            ext = '.png'
        elif conf['misc']['container'] in no:
            ext = path.splitext(video)[1]
        else:
            cont = conf['misc']['container']
            ext = cont if cont.startswith('.') else f'.{cont}'
        
        filename = path.splitext(path.basename(video))[0]
        if conf['misc']['prefix']:
            filename = f'{conf["misc"]["prefix"]}{filename}'

        if args.output and len(videos) == 1:
            out = args.output
        elif not args.output:
            out = path.join(outdir, f'{filename} ~ {suffix}{ext}')

            count=2
            while path.exists(out):
                out = path.join(outdir, f'{filename} ~ {suffix}({count}){ext}')
                count+=1
                               
        if isWin:
            vspipe = path.join(path.dirname(path.dirname(path.dirname(argv[0]))),'VapourSynth','VSPipe.exe')
        elif isLinux:
            vspipe = 'vspipe'
                    
        if args.vpy:
            if path.dirname(args.vpy[0]) in no:
                vpy = path.join( path.dirname(argv[0]), (args.vpy[0]) )
            else:
                vpy = path.abspath(args.vpy[0])
        else: vpy = path.abspath(path.join(path.dirname(argv[0]),'vitamix.vpy'))

        if args.verbose:
            conf['misc']['verbose'] = True

        command = [ # This is the master command, it gets appended some extra output args later down
        f'"{vspipe}" "{vpy}" --arg input_video="{path.abspath(video)}" --arg mask_directory="{mask_directory}" -y - ',
        f'{conf["encoding"]["process"]} -hide_banner -loglevel error -stats -stats_period 0.15 -i - ',
        ]
        
        map = '-map 0:v -map 1:a?' if isWin else '-map 0:v -map 1:a\?' # This puts the audio's file on the audio-less output file, Linux needs an escape character
        
        if args.peek:
            frame = int(args.peek[0]) # Extracting the frame passed from the singular array
            command[0] += f'--arg config="{conf}" --start {frame} --end {frame}'
            command[1] += f' "{out}"' # No need to specify audio map, simple image output
        elif args.tonull:
            command[0] += f'--arg config="{conf}"'
            command[1] += f' -f null NUL'
        elif args.tompv:
            a = conf['misc']['mpv bin']
            conf['misc']['verbose'] = True
            command[0] += f' --arg config="{conf}"'
            command[1] = conf['misc']['mpv bin'] + ' -'
        
        elif 'start' in trims.keys() and 'fin' in trims.keys(): # If they're both in here
            s, e = trims['start'], trims['fin']        
            if s>e:
                print(f"Trimming point {s} to {e} on video {video} is invalid: end before start??")
                continue
            elif e==s:
                print(f"Trimming point {s} to {e} on video {video} is invalid start and end are the same??")
                continue
            
            conf['TEMP']['start'] = s
            conf['TEMP']['end'] = e
            command[0] += f' --arg config="{conf}"'
            command[1] += f'{conf["encoding"]["args"]} "{out}"' # No audio since it's desynced and cba
        elif 'start' in trims.keys() or 'fin' in trims.keys(): # If only one is present
            print(trims)
            raise Exception('Incomplete trimming timecodes (need both start and end to do da trimming')
        else:
            command[0] += f' --arg config="{conf}"'

            # Adds as input the video to get it's audio tracks and gets encoding arguments from the config file
            command[1] += f'-i "{path.abspath(video)}" {map} {conf["encoding"]["args"]} "{out}"'

        if 'ffmpeg' in command[1]:
            # This will force the output video's color range to be Full
            range_proc = run(f'ffprobe -v error -show_entries stream=color_range -of default=noprint_wrappers=1:nokey=1 "{video}"', stdout=PIPE, stderr=PIPE, universal_newlines=True)
            if range_proc.stdout == 'pc\n':
                if '-vf ' in command[1]:
                    command[1] = command[1].replace('-vf ','-vf scale=in_range=full:out_range=limited,') # Very clever video filters appending
                else:
                    command[1] += ' -vf scale=in_range=full:out_range=full '

        if args.verbose:
            for cmd in command: print(f"{cmd}\n")
            print(f"Queuing video: {video}, vspipe is {vspipe}")
            try: a = run((command[0] + '|' + command[1]), shell=True)
            except KeyboardInterrupt:
                exit()
        else:
            log = Bar(command, video)
            if (log):
                if args.cui: SetWindowPos(hwnd,HWND_TOPMOST,0,0,1000,720,0)
                print(' '.join(command))
                print("")
                print(conf)
                print(''.join(log))
                print("VapourSynth and/or FFmpeg failed, here's a bunch of info you can share to help us debug")
                pause();exit(1)
        # Don't join these two if statements together, the one at the top is in the loop, while the bottom is when it's finished, notice the tab difference
    
    if not args.verbose:
        if args.cui:
            system(f"title [{iterations}/{len(videos)}] Smoothie - Finished! (EOF)")
        elif len(videos) > 1:
            print(f"\033[u\033[0J✅ Finished rendering {len(videos)} videos", end='\r')
        else:
            print(f"\033[u\033[?25h", end='\r')

    if conf['misc']['ding after'] <= len(videos):
        ding = r"C:\Windows\Media\ding.wav" # Modify that linux users :yum:
        ffplay = 'ffplay'
        if path.exists(r"C:\Windows\Media\ding.wav"):
            _ = subprocess.run(f'"{ffplay}" "{ding}" -volume 20 -autoexit -showmode 0 -loglevel quiet', shell=True)