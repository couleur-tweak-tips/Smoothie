from getpass import getpass
from sys import exit, stdin
from subprocess import run, PIPE
from re import search
from platform import architecture, system as ossystem
from os import system, environ

global isWT
isWT = environ.get('WT_PROFILE_ID') != None # This environemnt variable spawns with WT

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
yes = ['True','true','yes','y','1',1]
no = ['False','false','no','n','0',0,'null','',None]

def get_sec(time_str):
    if type(time_str) is list: time_str = time_str[0]
    if type(time_str) is str:
        if '.' in time_str: time_str = time_str.split('.')[0]
        if search('[a-zA-Z]', time_str) is not None:
            raise Exception(f'Timecode to trim contains a letter: {time_str}')
    # god bless https://stackoverflow.com/a/6402934
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(time_str).split(':'))))