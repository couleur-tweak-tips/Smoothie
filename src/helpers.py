from getpass import getpass
from sys import exit
from re import search
import platform
from os import environ
import json
import subprocess as sp

def exitSm(errorlevel, args) -> None: # Do not "instantly" close the terminal
	if args.cui:
		none = input("Press enter to exit")
	exit(errorlevel)

global isWT
isWT = environ.get('WT_PROFILE_ID') != None # This environemnt variable spawns with WT

def probe(file_path: str) -> dict:

    cmd = ("ffprobe",
           "-v", "error",
           "-of", "json",
           "-show_format",
           "-show_streams",
           file_path)

    data = json.loads(sp.check_output(cmd))
    
    if 'duration' not in data['format'].keys():
        data['format']['duration'] = ""

    # common values
    data.update({
        'stream':	data['streams'][0],
        'fps':		round(eval(data['streams'][0]['avg_frame_rate'])),
        'duration':	data['format']['duration'],
        'res':	(data['streams'][0]['width'], data['streams'][0]['height']),
        'codec':	data['streams'][0]['codec_name']
    })

    data.pop('streams') # we only need the first stream

    return data
    
def fps(file_path:str) -> int:
    r_frame_rate = probe(file_path)[1]['streams'][0]['r_frame_rate']
    return round(eval(r_frame_rate))
    
def setWTprogress(value:int,color:str=None): # Modified from https://github.com/oxygen-dioxide/wtprogress
    if(color!=None):
        color={"green":1,"g":1,"red":2,"r":2,"yellow":4,"y":4}[color]
    else:
        color="1"
    value=int(value)
    print("\x1b]9;4;{};{}\x1b\\".format(color,value),end="",flush=True)
    
def check_os():
    if platform.architecture()[0] != '64bit':
        raise OSError('Smoothie is only compatible with 64bit systems.')

    if platform.system() not in ('Linux', 'Windows'):
        raise OSError(f'Unsupported OS "{platform.system()}"')


def pause():
    getpass('Press enter to continue..')

# Bool aliases
yes = ['True','true','yes','y','1', True]
no = ['False','false','no','n','0','null','','none',None, False]

def get_sec(timecode):
    if type(timecode) is str:
        if '.' in timecode:
            spare = float("0." + timecode.split('.')[1])
            timecode = timecode.split('.')[0]
        if ';' in timecode:
            timecode = timecode.replace(';','.')
    elif isinstance(timecode, (float, int)):
        return timecode
    if type(timecode) is list: timecode = timecode[0]
    if type(timecode) is str:
        if search('[a-zA-Z]', timecode) is not None:
            raise Exception(f'Timecode to trim contains a letter: {timecode}')
    if 'spare' not in locals(): spare = 0
    # god bless https://stackoverflow.com/a/6402934
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(timecode).split(':')))) + spare


eol = end = reset = '\33[0m'

class style:
    bold      = '\33[1m' 
    italic    = '\33[3m' 
    url       = '\33[4m'
    blink     = '\33[5m' 
    altblink  = '\33[6m' 
    selected  = '\33[7m'
    invisible = '\33[8m'
    strike    = '\33[9m'

class foreground:
    rgb     = lambda r,g,b: f'\33[38;2;({r};{g};{b})m'
    black   = '\33[30m'
    red     = '\33[31m'
    green   = '\33[32m'
    yellow  = '\33[33m'
    blue    = '\33[34m'
    violet  = '\33[35m'
    beige   = '\33[36m'
    white   = '\33[37m'
    grey    = '\33[90m'
    lred    = '\33[91m'
    lgreen  = '\33[92m'
    lyellow = '\33[93m'
    lblue   = '\33[94m'
    lviolet = '\33[95m'
    lbeige  = '\33[96m'
    lwhite  = '\33[97m' 

class background:
    rgb     = lambda r,g,b: f'\33[48;2;({r};{g};{b})m'
    black   = '\33[40m'
    red     = '\33[41m'
    green   = '\33[42m'
    yellow  = '\33[43m'
    blue    = '\33[44m'
    violet  = '\33[45m'
    beige   = '\33[46m'
    white   = '\33[47m'
    grey    = '\33[100m'
    lred    = '\33[101m'
    lgreen  = '\33[102m'
    lyellow = '\33[103m'
    lblue   = '\33[104m'
    lviolet = '\33[105m'
    lbeige  = '\33[106m'
    lwhite  = '\33[107m' 

# Aliases
fg = foreground
bg = background   
st = style
