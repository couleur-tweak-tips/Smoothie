# Provides bindings to lib.dll

from ctypes import CDLL, c_char_p
from os.path import dirname

# Absolute paths are required to load the dll file.
dll = CDLL(f"{dirname(__file__)}/lib.dll")


def openFileDialog(title: str = "Open", filters: str = "All Files (*.*)|*.*", dir: str = ".") -> list[str]:
    # Title -> Title of the file dialog.
    # Filters -> Files (*.ext1, *.ext2, ...)|*.ext1;*.ext2;...
    # Directory -> Set the directory to open the file dialog in.

    ofd = dll.openFileDialog
    ofd.restype = c_char_p
    ofd.argtypes = [c_char_p, c_char_p, c_char_p]
    return ofd(title.encode(), filters.encode(), dir.encode()).decode().splitlines()


def setWinOnTop():
    # Puts any foreground window on top of all other windows.
    dll.setWinOnTop()