from tkinter.filedialog import askopenfile, askopenfiles
from dearpygui.dearpygui import *
from confparse import interpolation, frame_blending, misc, timescale, flowblur, encoding
from webbrowser import open_new_tab
from os import path
from yaml import safe_load, safe_dump
from values import recipe, config_values, elements_values
from subprocess import run
from pathlib import Path
from tkinter.messagebox import askyesno, showinfo
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
        disable_item('save')
        with open(f"{path.dirname(__file__)}/../../settings/recipe.yaml", 'w') as f:
            f.write(recipe.format(**config_values(get_value)))
        showMessage('Your recipe has been made!', timeout=2000)
        enable_item('save')
    def load():
        recipe = askopenfile()
        if recipe != None:
            init(recipe.name)

class info:
    def about():
        disable_item('about')
        showinfo('About', '''Smoothie GUI made using:

1. DearPyGUI 
2. PyYaml    

Made by Aetopia.''')
        enable_item('about')
    
    def help():
        open_new_tab('https://github.com/couleur-tweak-tips/Smoothie/wiki')

class sm:
    def select_videos():
        videos = askopenfiles()
        if videos != '':
            videos = [f'"{video.name}"' for video in videos]
            configure_item('videos', items=videos, default_value=videos[0])
    
    def clear_queue():
        widgets.disable_all()
        option = askyesno('Warning', 'Are you sure you want to clear the queue?')
        if option:
            configure_item('videos', items=[], default_value=None)
        widgets.enable_all()
            
class widgets:
    def disable_all():
        items = get_all_items()
        for item in items:
            try:
                disable_item(item)
            except SystemError:
                pass
    
    def enable_all():
        items = get_all_items()
        for item in items:
            try:
                enable_item(item)
            except SystemError:
                pass