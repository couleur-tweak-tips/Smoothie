import os
from config import ConfigRead 
from vs_script import Resample
from vs_script import Interpolate
from re import findall
from time import sleep
import subprocess

Temp=os.environ["TEMP"]

# Variables

def Render(VideoList, Option):
    Settings=ConfigRead(Option)
    for Video in list(VideoList):
        
        Video=os.path.abspath(Video)
        VideoPath=os.path.split(Video)[0]
        VideoFile=os.path.split(Video)[1]
        Arguments=Settings[1]  

        if Option == "resample":
            Resample(Video,Settings[2],Settings[3])
            Prefix="Resampled"
        elif Option == "interpolate":
            Interpolate(Video,Settings[2],Settings[3],Settings[4],Settings[5],Settings[6],Settings[7]) 
            Prefix="Interpolated" 

        Output=f"{VideoPath}\\{Prefix}_{VideoFile}"

        if os.path.isfile(Output):
            os.remove(Output)
        # Variables
        if "ffmpeg.exe" in os.path.split(Settings[0])[1]:
            Input=['-loglevel', 'error', '-hide_banner', '-stats', '-i', '-']
            Pipe=['vspipe', '-y', Temp+'\\Render.vpy','-','|']
            Output=[Output]
        elif "av1an.exe" in os.path.split(Settings[0])[1]:
            Input=['-i', f'{Temp}\\Render.vpy']
            Pipe=[]
            Output=['-o', Output]
  
        if Arguments=="":
            Arguments=[]
        else:
            Arguments=Settings[1].split(" ")    
        Main=Pipe+[Settings[0]]+Input+Arguments+Output
        print(f"Video: {Video}\n")      
        subprocess.run(Main,shell=True) 
        print("")

        

