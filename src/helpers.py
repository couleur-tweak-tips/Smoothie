
from platform import architecture, system
from getpass import getpass
from sys import exit

def checkOS ():
    from platform import architecture, system
    if architecture()[0] != '64bit':
        print('This script is only compatible with 64bit systems.')
        exit(1)

    if system() not in ['Linux', 'Windows']:
        # If hasn't returned yet then throw
        print(f'Unsupported OS "{system()}"')
        exit(1)

isLinux = system() == 'Linux'
isWin = system() == 'Windows'

def pause():
    getpass('Press enter to continue..')

# Bool aliases
yes = ['True','true','yes','y','1']
no = ['False','false','no','n','0','null','',None]
