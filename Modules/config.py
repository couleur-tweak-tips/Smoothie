import configparser
from encoder import GetEncoder
from os import environ, path, mkdir
Folder=f'{environ["APPDATA"]}/Smoothie'

if path.exists(Folder) is False:
  mkdir(Folder)

def ConfigExist():
  if path.exists(f'{Folder}/Smoothie-Config.ini') is False:
    ConfigCreate()

def ConfigCreate():
    SmoothieConfig = configparser.ConfigParser()
    EncoderSettings=GetEncoder()
    # Video
    SmoothieConfig['interpolation'] = {
    'fps': '480',
    'speed': 'medium',
    'tuning': 'weak',
    'algorithm': '23'
    }

    SmoothieConfig['resampling'] = {
      'fps': '60', 
      'intensity': '1'
      }   

    # Rendering
    SmoothieConfig['rendering'] = {
    "process": 'ffmpeg.exe',
    "arguments": '-loglevel error -hide_banner -stats'+f' {EncoderSettings[0]} '+'{Input}'+f' {EncoderSettings[1]} '+'{Output}' } 

    # Create Config File
    with open(f'{Folder}/Smoothie-Config.ini', 'w') as configfile:
        SmoothieConfig.write(configfile)

def ConfigRead(Option):
  SmoothieConfig = configparser.ConfigParser()
  SmoothieConfig.read(f'{Folder}/Smoothie-Config.ini')

  Process=SmoothieConfig['rendering']['process']
  Arguments=SmoothieConfig['rendering']['arguments']

  if Option == "resample":
    FPS=SmoothieConfig['resampling']['fps']

    Intensity=SmoothieConfig['resampling']['intensity']

    return (Process, Arguments, Intensity, FPS)
     
  elif Option == "interpolate":   
    InterpolateFPS=SmoothieConfig['interpolation']['fps']

    Speed=SmoothieConfig['interpolation']['speed']

    Tuning=SmoothieConfig['interpolation']['tuning']

    Algorithm=SmoothieConfig['interpolation']['algorithm']

    ResampleFPS=SmoothieConfig['resampling']['fps']

    Intensity=SmoothieConfig['resampling']['intensity']

    return (Process, Arguments, 
    InterpolateFPS, Speed, Tuning, Algorithm, 
    ResampleFPS, Intensity)

  

    



