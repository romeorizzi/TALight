#!/usr/bin/env python3

import defaults_general as def_gen

def ext(filename):
    pieces = filename.split('.')
    if len(pieces) == 1:
        return ''
    return '.'.join(pieces[1:])

def kernel(filename):
    basename = filename.split('.')[0]
    return basename.split('_')[-1]
        
def is_instance_id(kernel):
    if not isdecimal(kernel):
        return False
    n = int(kernel)
    if n < 1:
        return False
    if n > 999:
        return False
    return True
        
    
CEND      = def_gen.CEND
CBOLD     = def_gen.CBOLD
CITALIC   = def_gen.CITALIC
CURL      = def_gen.CURL
CBLINK    = def_gen.CBLINK
CRED      = def_gen.CRED
CGREEN    = def_gen.CGREEN
CYELLOW   = def_gen.CYELLOW
CBLUE     = def_gen.CBLUE
CVIOLET   = def_gen.CVIOLET
CBEIGE    = def_gen.CBEIGE
CWHITE    = def_gen.CWHITE

def confirm_to_continue(allow_skip_all = False):
    if confirm_to_continue.skip_all_active:
        return
    if allow_skip_all:
        answ = input(f"\n{CBOLD}{CYELLOW}Continuare?{CEND} (Premi {CBOLD}{CBEIGE}<RETURN/Enter>{CEND} per proseguire su questa singola operazione. Immetti '{CBOLD}{CBEIGE}go{CEND}' se vuoi eseguire tutti i comandi senza ulteriori conferme. Se vuoi abortire immetti '{CBOLD}{CBEIGE}stop{CEND}' o premi {CBOLD}{CBEIGE}Ctrl-C{CEND})\n >>> ")
        if answ.upper().strip() == "GO":
            confirm_to_continue.skip_all_active = True
    else:
        answ = input(f"\n{CBOLD}{CYELLOW}Continuare?{CEND} (Premi {CBOLD}{CBEIGE}<RETURN/Enter>{CEND} per proseguire. Se vuoi abortire immetti '{CBOLD}{CBEIGE}stop{CEND}' o premi {CBOLD}{CBEIGE}Ctrl-C{CEND})\n >>> ")
    if answ.upper().strip() == "STOP":
        print("Ok. Script abortito")
        exit(1)
    print("Ok. Proseguiamo ...")
confirm_to_continue.skip_all_active = False


