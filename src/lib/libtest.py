from win32lib import *
from time import sleep
from getpass import getpass
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))


def main():
    [print(i) for i in openFileDialog()]
    getpass("\nPress Enter to continue...")
    setSMWndParams(False, True, 200, 20)
    os.system('cls')
    print("Window is now on top.", end="\r")
    getpass("\r")
    os.system('cls')
    setSMWndParams(False, True, 1000, 720)
    print("Debug Mode!", end="\r")
    getpass("\r")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
