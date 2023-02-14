
BLACK   = '\u001b[30m'
BLUE    = '\u001b[34m'
CYAN    = '\u001b[36m'
GREEN   = '\u001b[32m'
MAGENTA = '\u001b[35m'
RED     = '\u001b[31m'
RESET   = '\u001b[0m'
YELLOW  = '\u001b[33m'
WHITE   = '\u001b[37m'



def black(string:str) -> str:
    return BLACK+string+RESET

def blue(string:str) -> str:
    return BLUE+string+RESET

def cyan(string:str) -> str:
    return CYAN+string+RESET

def green(string:str) -> str:
    return GREEN+string+RESET

def magenta(string:str) -> str:
    return MAGENTA+string+RESET

def red(string:str) -> str:
    return RED+string+RESET

def reset(string:str) -> str:
    return RESET

def yellow(string:str) -> str:
    return YELLOW+string+RESET

def white(string:str) -> str:
    return WHITE+string+RESET

#import re

#highlighted_cmd = "masterworkflows"
#for key in list("wfsm"):
#    highlighted_cmd =re.sub(rf'(.*?){key}(.*)',rf'\1\033[36m{key}\033[0m\2', highlighted_cmd)
#print( highlighted_cmd)

