from tkinter.filedialog import askopenfile
from dearpygui.dearpygui import get_value, set_value
from confparse import interpolation, frame_blending, misc, timescale, flowblur, encoding
from webbrowser import open_new_tab
from os import path
from yaml import safe_load, safe_dump
from values import recipe, config_values, elements_values
from subprocess import run
from pathlib import Path
from tkinter.messagebox import showinfo
import tkinter as tk
from tkinter import messagebox as msgb

def get_scoop_dir():
    return str(Path(run('scoop.cmd which scoop',
                        capture_output=True, shell=True).stdout.decode('utf-8').strip().lower())
               .expanduser())\
        .replace(r'\apps\scoop\current\bin\scoop.ps1', '')


def init(recipe: str):
    """
    Initialize the GUI with the given recipe.
    """
    recipe = safe_load(open(recipe))
    for key, value in elements_values(interpolation(recipe),
                                      frame_blending(recipe),
                                      flowblur(recipe),
                                      misc(recipe),
                                      encoding(recipe),
                                      timescale(recipe)).items():
        set_value(key, value)


def showMessage(message, type='info', timeout=2500):

    root = tk.Tk()
    root.withdraw()
    try:
        root.after(timeout, root.destroy)
        if type == 'info':
            msgb.showinfo('Info', message, master=root)
        elif type == 'warning':
            msgb.showwarning('Warning', message, master=root)
        elif type == 'error':
            msgb.showerror('Error', message, master=root)
    except:
        pass

class config:
    def write():
        config = recipe.format(**config_values(get_value))
        with open(f"{path.dirname(__file__)}/../../settings/recipe.yaml", 'w') as f:
            f.write(safe_dump(safe_load(config), sort_keys=False))
        showMessage('Your recipe has been made!', timeout=2000)
    def load():
        recipe = askopenfile()
        if recipe != None:
            init(recipe.name)

class info:
    def about():
        showinfo('About', '''Smoothie GUI made using:

1. DearPyGUI 
2. PyYaml    

Made by Aetopia.''')
    
    def help():
        open_new_tab('https://github.com/couleur-tweak-tips/Smoothie/wiki')