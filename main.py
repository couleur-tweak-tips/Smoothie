# Modules
from argparse import ArgumentParser
from pathlib import Path
import platform
from os import path, system
from sys import argv
from subprocess import run
from configparser import ConfigParser

# CLI Arguments
Parser=ArgumentParser(usage="",add_help=False)
Parser.add_argument('-resample', '-r', action="store", nargs="*")
Parser.add_argument('-interpolate', '-i', action="store", nargs="*")
Arguments=Parser.parse_args()

# Functions
def Render(Videos, Recipe=f"{path.abspath(path.split(argv[0])[0])}/settings/recipe.ini", Interpolate=False, Prefix="Resampled"):
    Program=ConfigParser()
    Program.read(Recipe)
    Queue=len(Videos)
    for Video in Videos:
        Queue-=1
        if Queue != 0:
            if platform.system() == "Windows":
                system(f"title Smoothie - Videos Queued: {Queue}")
            else:
                print(f"Videos Queued: {Queue}\n")    
        else:
            if platform.system() == "Windows":
                system(f"title Smoothie")                       
        VideoPath, VideoFile=path.split(path.abspath(Video))[0],path.split(path.abspath(Video))[1]
        Command=f'vspipe -c y4m -a Input="{path.abspath(Video)}" -a Interpolate="{Interpolate}" -a Config="{Recipe}" "{path.abspath("Vapoursynth.vpy")}" - | {Program["rendering"]["process"]} -y -loglevel error -hide_banner -stats -i - {Program["rendering"]["arguments"]} "{VideoPath}/{Prefix} {VideoFile}"'
        print(f"Video: {Video}\n")
        run(Command,shell=True)
        print("")

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
        Render(Arguments.interpolate, Interpolate=True)         
