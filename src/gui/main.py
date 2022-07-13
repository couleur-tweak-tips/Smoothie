from os import _exit, path
from sys import path as sys_path
from ctypes import windll
sys_path.append(path.dirname((__file__)))
from ui import start
windll.shcore.SetProcessDpiAwareness(2)

# Ensure that the script is running in the path is present in.
if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        _exit(0)