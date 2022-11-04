import subprocess
from subprocess import Popen
from os import get_terminal_size, path

from helpers import *
import colors
import constants

if constants.ISWIN:
    import PyTaskbar

    # if 'duration' in stream:
    #     length = stream['duration']
    # elif 'DURATION' in stream['tags']:
    #     length = get_sec(stream['tags']['DURATION'])
    # else:
    #     raise Exception('No duration found in video metadata')
    # return round(float(length))

def Bar (cmd: dict):
    try:
        # vs_proc = sp.Popen(cmd['ff'], stdout=sp.PIPE, stderr=sp.PIPE)
        # ff_proc = sp.Popen(cmd['vs'], stdin=vs_proc.stdout, stdout=sp.PIPE, stderr=sp.PIPE)
        process = Popen(
            (cmd['vs'] + '|' + cmd['ff']),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=True
            )
        from yaspin import yaspin, Spinner
        from yaspin.spinners import Spinners
        spinnertext = f'\033[s\033[?25lIndexing {path.basename(cmd["path"])}'
        
        if constants.ISWIN:
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
            Spinner(['\\', '|', '/', '-'], 50),  # type: ignore
            text=spinnertext)

        spinner.start()
        stats = {}
        duration = probe(cmd["path"])['duration']
        vid_length = round(float(duration))
        First = False
        log = []
        for current in process.stdout:
            log.append(current)
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
                barsize = columns - (52 + len(path.basename(cmd["path"])))
                progress = round(((percentage / 100) * barsize))

                #━ ╸
                # If user is running Windows Terminal, use strikthrough
                # Else use ─ (not -) for progress bar
                # They both look the same, but are not compatible with eachanother
                
                if percentage > 100: percentage = 100
                
                if constants.ISWIN:
                    if isWT:
                        setWTprogress(percentage)
                        sep = '｜'
                        bar = '\033[38;5;83m\033[9m' + (" " * progress)
                        bar += '\033[38;5;241m' + (" " * (barsize - progress)) + '\033[29m\033[0m'
                    else:
                        prog.setProgress(int(percentage))
                        sep = '|'
                        bar = '\033[38;5;83m' + ("━" * progress)
                        bar += '\033[38;5;241m' + ("─" * (barsize - progress)) + '\033[0m'  
                    
                #if (percentage <= 10): # needs a space before it grows a char when it passes 10
                #    pad = ' ' 
                #else:
                #    pad = ''
                
                if 'x' in stats['speed']:
                    stats['speed'] = float(stats['speed'].strip('x'))
                    if stats['speed'] >= 100:
                        stats['speed'] = 99.99
                    stats['speed'] = str(round((stats['speed']), 2)) + 'x'
                    
                if len(stats['speed']) == 4:
                    stats['speed'] = stats['speed'] + ' ' # Balances if it shrinks from 1.21x to 1.2x (1 less char)
                
                w = "\033[38;5;255m"
                g = "\033[38;5;245m"
                print(
f"\033[0J\033[?25l\
{w}{path.basename(cmd['path'])} {g}{sep} \
{w}time{g}: {stats['time']} \033[38;5;245m{sep} \
{bar} \033[38;5;245m{sep} \
{w}speed{g}: {stats['speed']} \033[38;5;245m{sep} \
{w}{percentage}\033[38;5;87m%\033[0m", end='\r')
                #print(f"\033[u\033[0J{percentage}", end='\r')
                if percentage >= 100: break
        if constants.ISWIN:
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
        if constants.ISWIN:
            if isWT==True: setWTprogress(0)
            else: prog.setProgress(0);prog.setState('normal');prog.setState('done')
        colors.printc('\033[?25h&RESETInterrupted @LBLUESmoothie&RESET (CTRL+C), exitting')    