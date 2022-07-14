from platform import system
from ui import start
from os import _exit, path
from sys import path as sys_path
sys_path.append(path.dirname((__file__)))
if system() == 'Windows':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(2)

# Ensure that the script is running in the path is present in.


def main():
    try:
        start()
    except KeyboardInterrupt:
        _exit(0)

if __name__ == '__main__':
    main()
