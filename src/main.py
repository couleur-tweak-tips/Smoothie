
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
	from win32gui import GetForegroundWindow, SetWindowPos # Move terminal to top left
	from win32con import HWND_TOPMOST # Make window stay on top
	hwnd = GetForegroundWindow()

init = time.time()

check_os()
commands = execute.buildcmd(args) # This builds every commands that will then be ran

for cmd in commands:
    
    context = f"""
VS: {cmd['vs']}

FF: {cmd['ff']}

ARGS: {' '.join(argv)}
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
            if args.cui: win32lib.set_sm_debug
            colors.printc("Oops! $LRED@WHITESmoothie crashed&RESET@LRED, here's a bunch of info you can share to help us debug:")
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