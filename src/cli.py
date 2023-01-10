from argparse import ArgumentParser
from constants import SRCDIR
from os import path
from sys import argv
parser = ArgumentParser()
add_arg = parser.add_argument

add_arg("-input", "-i",   
        help=" specify input video path(s)",
        action="store",
        nargs="+",
        metavar='PATH',
        type=str)

add_arg("-output", "-o",
        help=" specify output video path",
        action="store",
        nargs="+",
        metavar='PATH',
        type=str)

# open stuff 
add_arg("-dir",
        help=" opens the directory where Smoothie resides",
        action="store_true")

add_arg("-recipe", "-rc",
        help=" opens default recipe.ini",
        action="store_true")
 
# overrides/behavior 
add_arg("-peek", "-p",
        help=" Render a specific frame (outputs an image)",
        action="store",
        nargs=1,
        metavar='752',
        type=int)

add_arg("-stripaudio", "-an",
        help=" Doesn't output audio track",
        action="store_true")

add_arg("-config", "-c",
        help=" specify override config file",
        action="store",
        nargs=1, 
        metavar='PATH',
        type=str)

add_arg("-userecipe", "-ur",
        help=" specify override config file",
        action="store",
        nargs=1,
        metavar='PATH',
        type=str)

add_arg("-encargs", "-enc",
        help=" specify override ffmpeg encoding arguments",
        action="store",
        type=str)

add_arg("-verbose", "-v",
        help=" increase output verbosity",
        action="store_true")

add_arg("-veryverbose", "-vv",
        help=" increase output verbosity",
        action="store_true")

add_arg("-outdir", "-outd",
        help=" save all output to current directory",
        nargs='?',
        const='')

add_arg("-vpy",
        help=" use another VS script",
        action="store",
        nargs=1,
        metavar='PATH',
        type=str)

add_arg("-cui",
        help=" Make terminal stay on top moved on top left",
        action="store_true")

add_arg("-tonull", "-tn",
        help=" Redirect VS' Y4M output to NULL (for debugging)",
        action="store_true")

add_arg("-tompv",
        help=" Redirect VS' Y4M output to MPV (for viewing)",
        action="store_true")

add_arg("-override", "-overide","-ov",
        help=" Override a recipe value e.g: category;key;value",
        action="store",
        nargs="+",
        metavar='PATH',
        type=str)

# Cutting related
add_arg("-json",
        help=" JSON string to pass data",
        action="store",
        metavar='{0:23,1:34}',
        type=str)

add_arg("-padding",
        help = " Cut but keep same amount of delay (NLE script)",
        action="store_true")

add_arg("-trim",
        help=" Cut parts of the clip you don't want",
        action="store_true")

add_arg("-split",
        help=" Split your cut segments into multiple files",
        action="store_true")

add_arg("-rerun", '-!!',
        help=" Split your cut segments into multiple files",
        action="store_true")

lastargs = path.join(SRCDIR, 'lastargs.txt')

with open(lastargs, "r+", encoding="UTF-8") as f:
        if len(argv) == 2 and argv[1] in ["-!!", "-rerun"]:
                args = parser.parse_args(f.read().splitlines())
                
        else:
                f.truncate(0)
                f.write("\n".join(argv[1:]))
                args = parser.parse_args()


