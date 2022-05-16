#!/usr/bin/env pyhton3

from os import environ
import os
from lib_grades import lib_grades

DEBUG = False
#DEBUG = True

if not DEBUG:
    from multilanguage import Env, Lang, TALcolors
    from TALfiles import TALfilesHelper

    # METADATA OF THIS SERVICE
    args_list = [
        ('problem', str),
        ('service', str),
        ('all_submission', str),
        ('download', int)
    ]

    ENV = Env(args_list)
    TAc = TALcolors(ENV)
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
    TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

def main(problem : str, service : str, token : str, path : str): 
    lg = lib_grades()
    lg.loadFile(problem, service, token, path)

    lg.getProblemList().printToConsole(True)
    
    if not DEBUG:
        if ENV['download'] == 1:
            TALf.str2output_file(lg.getProblemList().instanceToString(True), "result.csv")

if __name__ == "__main__":
    if DEBUG:
        main("all_problems", "all_services", "123456__RomeoRizzi", os.path.join(os.getcwd(), "log_algorithms"))
    else:
        main(ENV['problem'], ENV['service'], environ['TAL_META_EXP_TOKEN'], environ['TAL_META_EXP_LOG_DIR'])
