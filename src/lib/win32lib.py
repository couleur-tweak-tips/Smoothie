# Provides bindings to lib.dll

from ctypes import CDLL, c_char_p
from os.path import dirname

# Absolute paths are required to load the dll file.
dll = CDLL(f"{dirname(__file__)}/lib.dll")


def filedialog(title: str = "Open", filters: str = "", dir: str = "") -> list[str]:
    # Title -> Title of the file dialog.
    # Filters -> Files (*.ext1, *.ext2, ...)|*.ext1;*.ext2;...
    # Directory -> Set the directory to open the file dialog in.

    fd = dll.filedialog
    fd.restype = c_char_p
    fd.argtypes = [c_char_p, c_char_p, c_char_p]
    return fd(title.encode(), filters.encode(), dir.encode()).decode('UTF-8').splitlines()


def set_sm_on_top():
    # Puts the Smoothie Window on top of all other windows.
    dll.setSMOnTop()

def set_sm_debug():
    # Puts the Smoothie Window on top of all other windows.
    dll.setSMDebug()
