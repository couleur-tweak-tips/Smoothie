from dearpygui.dearpygui import get_value, set_value
from confparse import interpolation, frame_blending, misc, timescale, flowblur, encoding
from yaml import safe_load, safe_dump
from values import recipe, config_values, elements_values
from subprocess import run
from pathlib import Path
from tkinter.messagebox import showinfo

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


class config:
    def write():
        config = recipe.format(**config_values(get_value))
        with open(fr"{get_scoop_dir()}\apps\smoothie\current\Smoothie\settings\recipe.yaml", 'w') as f:
            f.write(safe_dump(safe_load(config), sort_keys=False))
        showinfo('Recipe Made!', 'Your recipe has been made!')