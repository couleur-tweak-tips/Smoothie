# credits to atzur and topito

import os;os.system('')

eol = end = reset = '\33[0m'

class style:
    bold      = '\33[1m' 
    italic    = '\33[3m' 
    url       = '\33[4m'
    blink     = '\33[5m' 
    altblink  = '\33[6m' 
    selected  = '\33[7m'
    invisible = '\33[8m'
    strike    = '\33[9m'

class foreground:
    rgb     = lambda r,g,b: f'\33[38;2;({r};{g};{b})m'
    black   = '\33[30m'
    red     = '\33[31m'
    green   = '\33[32m'
    yellow  = '\33[33m'
    blue    = '\33[34m'
    violet  = '\33[35m'
    beige   = '\33[36m'
    white   = '\33[37m'
    grey    = '\33[90m'
    lred    = '\33[91m'
    lgreen  = '\33[92m'
    lyellow = '\33[93m'
    lblue   = '\33[94m'
    lviolet = '\33[95m'
    lbeige  = '\33[96m'
    lwhite  = '\33[97m' 

class background:
    rgb     = lambda r,g,b: f'\33[48;2;({r};{g};{b})m'
    black   = '\33[40m'
    red     = '\33[41m'
    green   = '\33[42m'
    yellow  = '\33[43m'
    blue    = '\33[44m'
    violet  = '\33[45m'
    beige   = '\33[46m'
    white   = '\33[47m'
    grey    = '\33[100m'
    lred    = '\33[101m'
    lgreen  = '\33[102m'
    lyellow = '\33[103m'
    lblue   = '\33[104m'
    lviolet = '\33[105m'
    lbeige  = '\33[106m'
    lwhite  = '\33[107m' 

# Aliases
fg = foreground
bg = background   
st = style 
