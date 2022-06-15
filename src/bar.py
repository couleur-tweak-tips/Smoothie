import subprocess
import PyTaskbar
from subprocess import Popen, run, PIPE 
from os import get_terminal_size, environ, path
from json import loads
from helpers import *
import sys
from textformat import *

def probe(file_path:str):
    
    command_array = ["ffprobe",
                 "-v", "quiet",
                 "-print_format", "json",
                 "-show_format",
                 "-show_streams",
                 file_path]
    result = run(command_array, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return [
        result.returncode,
        loads(result.stdout),
        result.stderr]

def get_length(file_path:str):
    stream = probe(file_path)[1]['streams'][0]

    if 'duration' in stream:
        length = stream['duration']
    elif 'DURATION' in stream['tags']:
        length = get_sec(stream['tags']['DURATION'])
    else:
        raise Exception('No duration found in video metadata')
    return round(float(length))

def Bar (command, video):
    
    try:
        process = Popen(
            (command[0] + '|' + command[1]),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=True
            )
        from yaspin import yaspin, Spinner
        from yaspin.spinners import Spinners
        spinnertext = f'Indexing {path.basename(video)}'
        
        if isWT: # then user is running Windows Terminal
            prog = PyTaskbar.Progress()
            
            spinner = yaspin(
                Spinners,
                text=spinnertext
                )
        else: # user is running something else (most probably conhost), I'll add support for more terminals soon if asked
            prog = PyTaskbar.Progress()
            prog.init()
            prog.setState('loading')
            spinner = yaspin(
                Spinner(['\\', '|', '/', '-'], 50),
                text=spinnertext)

        spinner.start()
        stats = {}
        vid_length = get_length(video)
        First = False
        for current in process.stdout:
            if not First:
                spinner.stop()
                First = True
            
            if current != '' or not current.startswith("Script"):
                statistic = current.replace('  ',' ').replace('  ',' ').replace('= ','=').replace('= ','=').split(' ')
                for stat in statistic:
                    if '=' in stat:
                        key, val = stat.split('=')
                        stats[key] = val

                #if stats == {}: # If it failed to parse
                #    print(process.stderr)
                #    raise Exception(f'\n\nVapourSynth failed to process the video, \n\nRun this in cmd for more info: sm -i "{path.abspath(video)}" -v ')

                if 'time' not in stats.keys(): continue
                secs_rendered = get_sec(stats['time'])
                percentage = round((secs_rendered*100) / vid_length, 1)

                columns = get_terminal_size()[0]
                barsize = columns - (23 + len(path.basename(video)))
                progress = round(((percentage / 100) * barsize))

                #━ ╸
                # If user is running Windows Terminal, use strikthrough
                # Else use ─ (not -) for progress bar
                # They both look the same, but are not compatible with eachanother
                
                if percentage > 100: percentage = 100
                
                if isWT:
                    setWTprogress(percentage)
                    bar = '\033[38;5;83m\033[9m' + (" " * progress)
                    bar += '\033[38;5;241m' + (" " * (barsize - progress)) + '\033[29m\033[0m'
                else:
                    prog.setProgress(int(percentage))
                    bar = '\033[38;5;83m' + ("━" * progress)
                    bar += '\033[38;5;241m' + ("─" * (barsize - progress)) + '\033[0m'  
                if (percentage <= 10): bar = ' ' + bar
                
                if 'x' in stats['speed']:
                    stats['speed'] = str(round((float(stats['speed'].replace('x',''))), 1)) + 'x'
                
                print(
f"\033[u\033[0J{path.basename(video)} \033[38;5;245m| \
speed: {stats['speed']} \033[38;5;255m{percentage}\033[38;5;87m% \033[38;5;245m|\033[0m \
{bar}", end='\r')
                #print(f"\033[u\033[0J{percentage}", end='\r')
                if percentage == 100: break
                
        if isWT==True: setWTprogress(0) # Reset
        else: prog.setProgress(0);prog.setState('normal');prog.setState('done')
        return process
    except KeyboardInterrupt:
        process.kill()
        spinner.stop()
        if isWT==True: setWTprogress(0)
        else: prog.setProgress(0);prog.setState('normal');prog.setState('done')
        print('Interrupted Smoothie (CTRL+C), exitting')
        sys.exit(0)