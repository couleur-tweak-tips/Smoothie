# Modules
from argparse import ArgumentParser
from pathlib import Path
from platform import system
from os import path
from sys import argv
from subprocess import Popen, PIPE, STDOUT
from configparser import ConfigParser

# CLI Arguments
Parser=ArgumentParser(usage="",add_help=False)
Parser.add_argument('-resample', '-r', action="store", nargs="*")
Parser.add_argument('-interpolate', '-i', action="store", nargs="*")
Arguments=Parser.parse_args()

# Functions
def Render(Videos, Recipe=f"{path.abspath(path.split(argv[0])[0])}/settings/recipe.ini", Interpolate=False, Prefix="Resampled"):
    Config=ConfigParser()
    Config.read(Recipe)
    Queue=len(Videos)
    for Video in Videos:

        Queue-=1
        if Queue != 0:
            if system() == "Windows":
                import ctypes
                ctypes.windll.kernel32.SetConsoleTitleW(f"Smoothie - Videos Queued: {Queue} | Rendering: {path.split(Video)[1]}")
            else:
                print(f"Videos Queued: {Queue}")    
        else:
            if system() == "Windows":
                import ctypes
                ctypes.windll.kernel32.SetConsoleTitleW(f"Smoothie - Rendering: {path.split(Video)[1]}")    

        VideoPath, VideoFile = path.split(path.abspath(Video))[0],path.split(path.abspath(Video))[1]
        VSPipe = f'vspipe -c y4m -a Input="{path.abspath(Video)}" -a Interpolate="{Interpolate}" -a Config="{Recipe}" "{path.abspath(path.split(argv[0])[0])}/vs.vpy" -' 
        FFmpeg = f'ffmpeg -y -loglevel error -hide_banner -stats -i - {Config["rendering"]["arguments"]} "{VideoPath}/{Prefix} - {VideoFile}"'
        Command=f'{VSPipe} | {FFmpeg}'
        print(f"\n> Video: {path.split(Video)[1]}")
        Process = Popen(Command, shell=True, encoding='utf-8', stdout=PIPE, stderr=STDOUT)

        # Output
        FullOutput=""
        while True:
            Output = Process.stdout.readline()
            FullOutput+=Output
            if Output == '' or Process.poll() is not None:
                break
            if Output:
                try:
                    print(f"> Time: {Output.strip().split('=')[5].split(' ')[0]} | Speed: x{Output.strip().split('=')[7].split(' ')[0].replace('x','')}", end='\r',flush=True)
                except:
                    pass 
        print("")           
        Process.communicate()
        if Process.returncode == 1:
            print(FullOutput)
            exit()


# Arguments Parsing
if Arguments.resample is not None:
    if Path(Arguments.resample[0]).suffix == '.ini':
        Render(Arguments.resample[1::], Recipe=path.abspath(Arguments.resample[0]))
    else:
        Render(Arguments.resample)    

elif Arguments.interpolate is not None:
    if Path(Arguments.interpolate[0]).suffix == '.ini':
        Render(Arguments.interpolate[1::], 
        Recipe=path.abspath(Arguments.interpolate[0]), 
        Interpolate=True,Prefix="Interpolated")
    else:
        Render(Arguments.interpolate, Interpolate=True, Prefix="Interpolated")