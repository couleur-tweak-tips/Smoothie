import exec
import helpers
helpers.checkOS()

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-peek",     "-p",    help="render a specific frame (outputs an image)", action="store", nargs=1, metavar='752',       type=int)
parser.add_argument("-trim",     "-t",    help="Trim out the frames you don't want to use",  action="store", nargs=1, metavar='0:23,1:34', type=str)
parser.add_argument("-dir",               help="opens the directory where Smoothie resides", action="store_true"                                   )
parser.add_argument("-recipe",   "-rc",   help="opens default recipe.ini",                   action="store_true"                                   )
parser.add_argument("--config",  "-c",    help="specify override config file",               action="store", nargs=1, metavar='PATH',      type=str)
parser.add_argument("--encoding", "-enc", help="specify override ffmpeg encoding arguments", action="store",                               type=str)
parser.add_argument("-verbose",  "-v",    help="increase output verbosity",                  action="store_true"                                   )
parser.add_argument("-curdir",   "-cd",   help="save all output to current directory",       action="store_true",                                  )
parser.add_argument("-input",    "-i",    help="specify input video path(s)",                action="store", nargs="+", metavar='PATH',    type=str)
parser.add_argument("-output",    "-o",   help="specify output video path(s)",               action="store", nargs="+", metavar='PATH',    type=str)
parser.add_argument("-vpy",               help="specify a VapourSynth script",               action="store", nargs=1, metavar='PATH',      type=str)

exec.runvpy(parser)