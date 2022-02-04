from sys import argv # parse args
from os import path # split file extension
from configparser import ConfigParser
from yaml import load,FullLoader # parse the config
from subprocess import run # Run vs
#from random import choice # Randomize the smoothie's flavor))

if len(argv) == 1:
    print('''
using Smoothie from the command line:

sm "D:\Video\input1.mp4" "D:\Video\input2.mp4" ...
    Simply give in the path of the videos you wish to queue to smoothie

sm config.extension "D:\Video\input1.mp4" "D:\Video\input2.mp4" ...
    You can also make the first argument be your custom config file's name, it'll look for it in the settings folder
    ''')
    exit(0)

def ensure(file, desc):
    if path.exists(file) == False:
        print(f"{desc} file not found: {file}")
        exit(1)

if path.splitext(argv[1])[1] == '.ini':
    recipe=path.abspath(argv[1])
    queue=argv[2:]
else:    
    recipe=f'{path.abspath(path.dirname(argv[0]))}/settings/recipe.ini'
    queue=argv[1:]

conf=ConfigParser()
conf.read(recipe)

for video in list(queue):
    """
    if ['conf']['misc']['random flavors'] == True:
        flavors = ('Strawberry','Blueberry','Raspberry','Blackberry',
        'Cherry', 'Cranberry','Coconut','Peach','Apricot',
        'Dragonfruit','Grapefruit', 'Melon','Papaya',
        'Watermelon','Banana','Pineapple','Apple','Kiwi')
    else:
        flavors = ('Smoothie')
    """ 
    filename, ext = path.splitext(video)

    if conf['misc']['folder'].lower() in ['null','','none','no','n']:
        outdir = path.abspath(path.split(video)[0])
    else:
        outdir = path.abspath(conf['misc']['folder'])

    out = f'{outdir}/{filename} - Smoothie.{conf["misc"]["container"]}'
   
    print(f'> Video: {path.abspath(video)}\n')
    command = [ # Split in two for readability/
        f'vspipe -c y4m -a input_video="{path.abspath(video)}" -a config_filepath="{recipe}" "{path.join(path.dirname(argv[0]))}/blender.vpy" -',
        f'ffmpeg -y -hide_banner -loglevel warning -stats -i - {conf["encoding"]["args"]} "{out}"'
    ]
    run(f'{command[0]} | {command[1]}',shell=True)        
