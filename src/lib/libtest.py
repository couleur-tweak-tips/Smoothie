from win32lib import *
from time import sleep
from getpass import getpass
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))


def main():
    [print(i) for i in openFileDialog()]
    getpass("\nPress Enter to continue...")
    os.system('cls')
    
    # Warning! Exceeding the buffer size will make conhost.exe crash!
    for i in range(5):
        setSMWndParams(False, True, 185, 20, i)
        print("Window is now on top.", end="\r")
        sleep(1)
    getpass("\r")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
