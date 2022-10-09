import subprocess
import PyTaskbar
from subprocess import Popen
from os import get_terminal_size, path
from helpers import *

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
        spinnertext = f'\033[?25lIndexing {path.basename(video)}'
        
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
        log = []
        for current in process.stdout:
            log += current
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
                barsize = columns - (47 + len(path.basename(video)))
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
                    stats['speed'] = str(round((float(stats['speed'].replace('x',''))), 2)) + 'x'
                
                w = "\033[38;5;255m"
                g = "\033[38;5;245m"
                print(
f"\033[u\033[0J\033[?25l\
{w}{path.basename(video)} {g}| \
{w}time{g}: {stats['time']} \033[38;5;245m| \
{w}speed{g}: {stats['speed']} \033[38;5;245m| \
{w}{percentage}\033[38;5;87m% \033[38;5;245m|\033[0m \
{bar}", end='\r')
                #print(f"\033[u\033[0J{percentage}", end='\r')
                if percentage >= 100: break
        if isWT==True: setWTprogress(0) # Reset
        else: prog.setProgress(0);prog.setState('normal');prog.setState('done')
        
        process.communicate()
        if process.returncode != 0:
            return log
        else:
            return None
        
    except KeyboardInterrupt:
        process.kill()
        spinner.stop()
        if isWT==True: setWTprogress(0)
        else: prog.setProgress(0);prog.setState('normal');prog.setState('done')
        print('\033[?25hInterrupted Smoothie (CTRL+C), exitting')    