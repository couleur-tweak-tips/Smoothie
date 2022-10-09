from getpass import getpass
from json import loads
from sys import exit
from subprocess import run, PIPE
from re import search
from platform import architecture, system as ossystem
from os import environ
from math import floor

global isWT
isWT = environ.get('WT_PROFILE_ID') != None # This environemnt variable spawns with WT

def probe(file_path:str):
    
    command_array = ["ffprobe",
                 "-v", "quiet",
                 "-print_format", "json",
                 "-show_format",
                 "-show_streams",
                 file_path]
    result = run(command_array, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return [
        result.returncode,
        loads(result.stdout),
        result.stderr]
    
def fps(file_path:str):
    r_frame_rate = probe(file_path)[1]['streams'][0]['r_frame_rate']
    return round(eval(r_frame_rate))
    
def setWTprogress(value:int,color:str=None): # Modified from https://github.com/oxygen-dioxide/wtprogress
    if(color!=None):
        color={"green":1,"g":1,"red":2,"r":2,"yellow":4,"y":4}[color]
    else:
        color="1"
    value=int(value)
    print("\x1b]9;4;{};{}\x1b\\".format(color,value),end="",flush=True)
    
def checkOS ():
    if architecture()[0] != '64bit':
        print('This script is only compatible with 64bit systems.')
        exit(1)

    if ossystem() not in ['Linux', 'Windows']:
        # If hasn't returned yet then throw
        print(f'Unsupported OS "{ossystem()}"')
        exit(1)

global isLinux, isWin
isLinux = ossystem() == 'Linux'
isWin = ossystem() == 'Windows'

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