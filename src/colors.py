from os import system; system('')

# & == method
# @ == foreground
# $ == background

codes = {'&RESET'    : '\33[0m',
         '&BOLD'     : '\33[1m',
         '&ITALIC'   : '\33[3m',
         '&URL'      : '\33[4m',
         '&BLINK'    : '\33[5m',
         '&ALTBLINK' : '\33[6m',
         '&SELECTED' : '\33[7m',
         '@BLACK'    : '\33[30m',
         '@RED'      : '\33[31m',
         '@GREEN'    : '\33[32m',
         '@YELLOW'   : '\33[33m',
         '@BLUE'     : '\33[34m',
         '@VIOLET'   : '\33[35m',
         '@BEIGE'    : '\33[36m',
         '@WHITE'    : '\33[37m',
         '@GREY'     : '\33[90m',
         '@LRED'    : '\33[91m',
         '@LGREEN'  : '\33[92m',
         '@LYELLOW' : '\33[93m',
         '@LBLUE'   : '\33[94m',
         '@LVIOLET' : '\33[95m',
         '@LBEIGE'  : '\33[96m',
         '@LWHITE'  : '\33[97m',
         '$BLACK'    : '\33[40m',
         '$RED'      : '\33[41m',
         '$GREEN'    : '\33[42m',
         '$YELLOW'   : '\33[43m',
         '$BLUE'     : '\33[44m',
         '$VIOLET'   : '\33[45m',
         '$BEIGE'    : '\33[46m',
         '$WHITE'    : '\33[47m',
         '$GREY'     : '\33[100m',
         '$LRED'    : '\33[101m',
         '$LGREEN'  : '\33[102m',
         '$LYELLOW' : '\33[103m',
         '$LBLUE'   : '\33[104m',
         '$LVIOLET' : '\33[105m',
         '$LBEIGE'  : '\33[106m',
         '$LWHITE'  : '\33[107m'}


def printc(text:str):
    print(formatc(text))


def formatc(text:str):

    formatted = text

    for key in list(codes):
        if key in formatted:
            formatted = formatted.replace(key, codes.get(key))

    formatted = formatted + codes.get('&RESET')

    return formatted


def print_success (text: str, prefix: bool = True, isolate: bool = False):

    out = formatc(f'@LGREEN{text}')

    if prefix:
        out = formatc(f'[&BOLD@GREENSUCCESS&RESET]: ') + out

    if isolate:
        out = '\n' + out + '\n'

    print(out)