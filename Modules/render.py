import os
from config import ConfigRead 
from vspipe import Resample
from vspipe import Interpolate
from subprocess import run

def Render(VideoList, Option):
    Settings=ConfigRead(Option)
    Temp=os.environ["TEMP"]
    for Video in list(VideoList):
        
        Video=os.path.abspath(Video)
        VideoPath=os.path.split(Video)[0]
        VideoFile=os.path.split(Video)[1]
        Process=Settings[0]
        Arguments=Settings[1]  

        if Option == "resample":
            VSPipeArgs=Resample(Video,Settings[2],Settings[3])
            Prefix="Resampled"
        elif Option == "interpolate":
            VSPipeArgs=Interpolate(Video,Settings[2],Settings[3],Settings[4],Settings[5],Settings[6],Settings[7]) 
            Prefix="Interpolated" 

        Output=f"{VideoPath}\\{Prefix}_{VideoFile}"

        if os.path.isfile(Output):
            os.remove(Output)

        # Variables
        if "ffmpeg.exe" in os.path.split(Process)[1]:
            Input="-i -"
            VSPipe=f'vspipe -c y4m {VSPipeArgs} - |'
            Output=f'"{Output}"'

        elif "av1an.exe" in os.path.split(Process)[1]:
            Input=f'-i "{Temp}\\Render.vpy"'
            VSPipe=""
            Output=f'-o "{Output}"'

        else:
            print("Specified Process isn't supported by Smoothie.")
            exit()    

        Arguments=Arguments.format(Input=Input,Output=Output)  
        Command=f'{VSPipe} {Process} {Arguments}'
        
        print(f"Video: {Video}\n")    
        run(Command,shell=True) 
        print("")

        

