#!/usr/bin/env pyhton3

from os import environ, listdir
from os.path import isfile, isdir, join
from sys import exit
import os
import datetime
import time
from typing import MutableSequence

DEBUG = False

if not DEBUG:
    from multilanguage import Env, Lang, TALcolors
    import monitor_grades_lib as mgl

    # METADATA OF THIS SERVICE
    args_list = [
        ('problem', str),
        ('service', str),
    ]

    ENV = Env(args_list)
    TAc = TALcolors(ENV)
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
    #TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

# WARNING: these two enviroment variables are deprecated (introduced now to get the job done, but will be later discharged:
#TAc.print(LANG.render_feedback("TAL_META_EXP_TOKEN", f'TAL_META_ENV.EXP_TOKEN={environ["TAL_META_EXP_TOKEN"]}'), 'red', ['bold'])
#TAc.print(LANG.render_feedback("TAL_META_EXP_LOG_DIR", f'ENV.TAL_META_EXP_LOG_DIR={environ["TAL_META_EXP_LOG_DIR"]}'), 'red', ['bold'])
# END WARNING

print([ (var_name, environ[var_name]) for var_name in environ if var_name[:4] == "TAL_"])

ALLPROBLEM = "all_problems"
ALLSERVICE = "all_services"
OKCONSTANT = "OK"

def main(problem : str, service : str, token : str, log_dir : str):
    path = os.path.join(os.getcwd(), log_dir)

    recent_date = ""
    recent_folder = ""
    
    for x in listdir(path):
        fullpath = os.path.join(os.getcwd(), log_dir, x)

        s = str(x).split('+')

        if (s[0] == token):
            date_time_obj = time.strptime(s[1], '%Y-%m-%d_%H-%M-%S_%f')

            if recent_date == "":
                recent_date = date_time_obj
                recent_folder = fullpath

            if date_time_obj > recent_date:
                recent_date = date_time_obj
                recent_folder = fullpath
                
    printConsole("Student: " + token, True)
    printConsole("------------------------", True)
                
    for x in listdir(recent_folder):
        s = str(x).split('_')
        goal = s[3].split('.')[0]

        if (s[1] == problem or problem == ALLPROBLEM):
            if (s[2] == service or service == ALLSERVICE):
                if (s[0] == OKCONSTANT):
                    printConsole(goal, True)
                else:
                    printConsole(goal, False)
               
                printFileContent(os.path.join(recent_folder, x))

                printConsole("--------------------", True)

def printFileContent(filename : str):
    file_descriptor = open(filename)
    file_contents = file_descriptor.read()

    printConsole(file_contents, True)

def printConsole(msg : str, isOK : bool):
    if not DEBUG:
        if (isOK):
            TAc.print(msg, "green", ['bold'])
        else:
            TAc.print(msg, "red", ['bold'])
    else:
        if (isOK):
            print("OK", msg)
        else:
            print("NO", msg)

if __name__ == "__main__":
    print(f"{os.getcwd()=}")
    print(f"{environ['TAL_META_LOG_FILES']=}")
    print(f"{environ['TAL_META_EXP_LOG_DIR']=}")
    print(f"{environ['TAL_META_EXP_TOKEN']=}")
    
        
    if DEBUG:
        main("nomeproblema", "nomeservizio", "123456_RomeoRizzi", "log_algorithms")
    else:
        main(ENV['problem'], ENV['service'], environ['TAL_META_EXP_TOKEN'], environ['TAL_META_EXP_LOG_DIR'])

# formato del filename dello .yaml file principale che descrive i contenuto di una cartella di LOG:
# 123456_RomeoRizzi+2022-02-24_20-56-54_425        
