from time import sleep
from getpass import getpass
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import win32lib
from win32lib import *

def main():
    [print(i) for i in win32lib.openFileDialog()]
    getpass("\nPress Enter to continue...")
    win32lib.setSmTop(False)
    os.system('cls')
    print("Window is now on top.", end="\r")
    getpass("\r")
    os.system('cls')
    win32lib.setSmDebug(True)
    print("Debug Mode!", end="\r")
    getpass("\r")
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()