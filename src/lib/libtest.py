from win32lib import *
from time import sleep
from getpass import getpass
from os import system


def main():
    [print(i) for i in filedialog()]
    getpass("\nPress Enter to continue...")
    set_sm_debug()
    system('cls')
    while True:
        print("Window is now on top.", end="\r")
        sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()