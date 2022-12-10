import subprocess
from fnmatch import fnmatch
from os import get_terminal_size, path
from time import sleep
from helpers import *
import colors
import constants

if constants.ISWIN:
    import PyTaskbar

def Bar (cmd: dict):
    try:
        process = subprocess.Popen(
            (cmd['vs'] + '|' + cmd['ff']),
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True
            )
        from yaspin import yaspin, Spinner
        from yaspin.spinners import Spinners
        spinnertext = f'\033[s\033[?25lIndexing {path.basename(cmd["path"])}'
        
        if constants.ISWIN:
            if isWT: # then user is running Windows Terminal
                endchar = "\r"
                prog = PyTaskbar.Progress()
                
                spinner = yaspin(
                    Spinners,
                    text=spinnertext
                    )
            else: # user is running something else (most probably conhost), I'll add support for more terminals soon if asked
                endchar = None
                prog = PyTaskbar.Progress()
                prog.init()
                prog.setState('loading')
                
                spinner = yaspin(
                    Spinner(['\\', '|', '/', '-'], 50),  # type: ignore
                    text=spinnertext)
        else:
            endchar = None

        spinner.start()        
        duration = probe(cmd["path"])['duration']
        vid_length = float(duration)
        
        def display_bar (current: str) -> str:
            columns = get_terminal_size()[0]
            barsize = columns - (52 + len(path.basename(cmd["path"])))

            stats = {}
            statistic = current.replace('  ',' ').replace('  ',' ').replace('= ','=').replace('= ','=').split(' ')
            for stat in statistic:
                if '=' in stat:
                    key, val = stat.split('=')
                    # print(key, val)
                    stats[key] = val
 
            if 'time' not in stats.keys():
                return "Bar: FFmpeg output does not contain time value yet"
            elif stats['time'].startswith("-"): # negative time happens at first sometimes, can be disturbing
                return ""
            
            secs_rendered = get_sec(stats['time'])
            percentage = round((secs_rendered*100) / vid_length, 1)
            progress = round(((percentage / 100) * barsize)) # per*size of colums*tage

            if 'x' in stats['speed']:
                stats['speed'] = float(stats['speed'].strip('x'))
                if stats['speed'] >= 100:
                    stats['speed'] = 99.99
                stats['speed'] = str(round((stats['speed']), 2)) + 'x'

            if isWT:
                setWTprogress(percentage)
                bar = '\033[38;5;83m\033[9m' + (" " * progress)
                bar += '\033[38;5;241m' + (" " * (barsize - progress)) + '\033[29m\033[0m'
            else:
                prog.setProgress(int(percentage))
                bar = '\033[38;5;83m' + ("━" * progress)
                bar += '\033[38;5;241m' + ("─" * (barsize - progress)) + '\033[0m'  
            if (percentage <= 10): bar = ' ' + bar
                        
            w = "\033[38;5;255m"
            g = "\033[38;5;245m"
            return str(
f"\033[u\033[0J\033[?25l\
{w}{path.basename(cmd['path'])} {g}| \
{w}time{g}: {stats['time']} \033[38;5;245m| \
{w}speed{g}: {stats['speed']} \033[38;5;245m| \
{w}{percentage}\033[38;5;87m% \033[38;5;245m|\033[0m \
{bar}")
            #return str(f"{secs_rendered}*100/{vid_length}={percentage}")

        log = []
        for line in iter(process.stderr.readline, ""):
            current = line.strip()
            spinner.stop()
            indexText = "Creating lwi index file "
            if current.startswith(indexText):
                message = "Indexing: " + current.strip(indexText)
            elif fnmatch(current, "frame=*fps=*q=*size=*time=*bitrate=*speed=*"):
                message = display_bar(current)
            elif fnmatch(current, "Output * frames in * seconds (* fps)"):
                break
            else:
                # I doubledog dare you find a better way in Python
                # to both error handle and format stdout like I do
                message = current
                log.append(current)
            
            print(message, end=endchar)
            sleep(0.15)
            if len(current) == 0: # if be finished
                break
        if log:
            return log
    except KeyboardInterrupt:
        process.kill()
        spinner.stop()
        if constants.ISWIN:
            if isWT==True: setWTprogress(0)
            else: prog.setProgress(0);prog.setState('normal');prog.setState('done')
        colors.printc('\033[?25h&RESETInterrupted @LBLUESmoothie&RESET (CTRL+C), exitting')    