from time import sleep
from getpass import getpass
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

def main():
    [print(i) for i in openFileDialog()]
    getpass("\nPress Enter to continue...")
    setWinOnTop()
    os.system('cls')
    while True:
        print("Window is now on top.", end="\r")
        sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()