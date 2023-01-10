
from os import path
from sys import argv, path as importpath
importpath.append(path.dirname(__file__))
from subprocess import run
import time

import execute # Returns a dict containing the recipe, and a long vspipe {config} | ffmpeg command
from bar import Bar
from cli import args
from helpers import *
import colors
import constants


if constants.ISWIN: # File dialog, file opener
	from lib import win32lib

init = time.time()

check_os()
commands = execute.buildcmd(args) # This builds every commands that will then be ran

for cmd in commands:
    
    # Used in verbose mode or when Smoothie/what it uses crashes
    context = f"""
VSPipe command:\n{cmd['vs']}

FFmpeg command:\n{cmd['ff']}

Arguments passed to Smoothie:\n
{' '.join(argv)}
    """
    
    command = (cmd['vs'] + ' | ' + cmd['ff'])
    
    if args.verbose:
        
        print(context)
        
        try:
            a = run(command, shell=True)
            
        except KeyboardInterrupt:
            exit()
            
    else: # (try to) display the progress bar
        
        if probe(cmd['path'])['duration'] == '':
            
            colors.printc(f"@LREDCould not determine duration of @WHITE{path.basename(cmd['path'])}. @REDNot displaying progress bar")
            
            try:
                a = run(command, shell=True)
            except KeyboardInterrupt:
                exit()
            if a.returncode >= 1: log = [" "]
            
            
        else:
            
            try:
                log = Bar(cmd)
            except KeyboardInterrupt:
                exit()
                
        if (log): # Only returns logs if it throws
            if args.cui and constants.ISWIN:
                params = getWinParams(recipe=cmd['recipe']['console params'], debug=True)
                win32lib.setSMWndParams(**params)
            colors.printc("Oops! $LRED@WHITESmoothie crashed&RESET@LRED, here's a bunch of info you can look into and share to help us debug:")
            print(context)
            for error in log:
                if error == "\n": continue
                print(error.replace("\n",""))
            exitSm(1, args)



done = time.time()
elapsed = done-init
if elapsed >= 60:
    term = f"{round(elapsed/60, 2)} minutes"
else:
    term = f"{round(elapsed, 2)} seconds"
    
colors.printc(f"\033[2K@LBLUESmoothie&RESET: Finished rendering @LBLUE{len(commands)}&RESET videos in @LBLUE{term}&RESET")