import argparse
import sys
import subprocess
sys.path.insert(0, 'scripts')
from config import ConfigExist
from render import Render

ConfigExist()

Parser=argparse.ArgumentParser(prog="Smoothie",
usage="""
smoothie -resample Video1.mp4 Video2.mp4 Video3.mp4
smoothie -interpolate Video1.mp4 Video2.mp4 Video3.mp4""")

Parser.add_argument('-resample',action="store",
help="Resample single or multiple videos at once.",
nargs='*',
metavar=("<Videos>"))

Parser.add_argument('-interpolate',action="store",
help="Interpolate and resample single or multiple videos at once.",
nargs='*',
metavar=("<Videos>"))

Parser.add_argument('-edit',action="store_true",help="Edit Smoothie's config file.")

Arguments=Parser.parse_args()

if Arguments.resample is not None:
    Render(Arguments.resample, "resample")
elif Arguments.interpolate is not None:
    Render(Arguments.interpolate, "interpolate")
elif Arguments.edit is True:
    subprocess.Popen(['start',f'{CWD}/Smoothie-Config.ini'],shell=True)     
