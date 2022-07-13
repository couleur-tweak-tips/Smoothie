from os import _exit, path
from sys import path as sys_path
from sys import exit
from ctypes import windll
sys_path.append(path.dirname((__file__)))
from ui import start
windll.shcore.SetProcessDpiAwareness(2)

# Ensure that the script is running in the path is present in.
def main():
    try:
        start()
        exit(0)
    except KeyboardInterrupt:
        _exit(0)