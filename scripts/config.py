import configparser
from encoder import GetEncoder 
from os import path
from sys import argv
File=f"{path.split(argv[0])[0]}/Smoothie-Config.ini"

def ConfigExist():
  if path.exists(File) is False:
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
    with open(File, 'w') as configfile:
        SmoothieConfig.write(configfile)

def ConfigRead(Option):
  SmoothieConfig = configparser.ConfigParser()
  SmoothieConfig.read(File)

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

"""  
  elif Option == "interpolate":
    FPS=SmoothieConfig['interpolation']['fps']

    Speed=SmoothieConfig['interpolation']['speed']

    Tuning=SmoothieConfig['interpolation']['tuning']

    Algorithm=SmoothieConfig['interpolation']['algorithm']

    return (Process, Arguments, FPS, Speed, Tuning, Algorithm)
"""     

  

    



