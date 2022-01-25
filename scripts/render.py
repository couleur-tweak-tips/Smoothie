import os
from config import ConfigRead 
from vs_script import Resample
from vs_script import Interpolate
from subprocess import run

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
            Options='-loglevel error -hide_banner -stats'
            Input="-i -"
            Pipe=f'vspipe -y {Temp}\\Render.vpy - | '
            Output=Output
            Arguments=Arguments.format(Options=Options,Input=Input,Output=Output)

        elif "av1an.exe" in os.path.split(Settings[0])[1]:
            Input=f'-i {Temp}\\Render.vpy'
            Pipe=""
            Output=f'-o {Output}'
            Arguments=Arguments.format(Input=Input,Output=Output)  

        Main=Pipe+Settings[0]+f' {Arguments}'
        print(f"Video: {Video}\n")      
        run(Main,shell=True) 
        print("")

        

