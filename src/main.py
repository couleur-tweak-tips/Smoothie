from os import path
from sys import path as importpath
importpath.append(path.dirname(__file__))
import exec
import helpers
helpers.checkOS()

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-peek",    "-p",   help=" Render a specific frame (outputs an image)",     action="store",       nargs=1, metavar='752',      type=int)
parser.add_argument("-trim", "-ft",     help=" Trim out the frames you don't want to render",   action="store",       nargs=1, metavar='0:23,1:34'         )
parser.add_argument("-dir",             help=" opens the directory where Smoothie resides",     action="store_true"                                        )
parser.add_argument("-recipe",  "-rc",  help=" opens default recipe.ini",                       action="store_true"                                        )
parser.add_argument("-config",  "-c",   help=" specify override config file",                   action="store",       nargs=1, metavar='PATH',     type=str)
parser.add_argument("-encargs", "-enc", help=" specify override ffmpeg encoding arguments",     action="store",                                    type=str)
parser.add_argument("-verbose", "-v",   help=" increase output verbosity",                      action="store_true"                                        )
parser.add_argument("-outdir",  "-outd",help=" save all output to current directory",           nargs='?', const=''                                        )
parser.add_argument("-input",   "-i",   help=" specify input video path(s)",                    action="store",       nargs="+", metavar='PATH',   type=str)
parser.add_argument("-output",  "-o",   help=" specify output video path(s)",                   action="store",       nargs="+", metavar='PATH',   type=str)
parser.add_argument("-vpy",             help=" specify a VapourSynth script",                   action="store",       nargs=1, metavar='PATH',     type=str)
parser.add_argument("-cui",             help=" Make terminal stay on top moved on top left",    action="store_true",                                       )
parser.add_argument("-tonull",          help=" Redirect VS' Y4M output to NULL (for debugging)",action="store_true",                                       )
parser.add_argument("-tompv",           help=" Redirect VS' Y4M output to MPV  (for debugging)",action="store_true",                                       )
parser.add_argument("-override", "-ov", help=" Override a recipe value e.g: category;key;value",action="store",       nargs="+", metavar='PATH',   type=str)


exec.runvpy(parser)