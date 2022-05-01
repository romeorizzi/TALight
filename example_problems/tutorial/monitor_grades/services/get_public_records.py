#!/usr/bin/env pyhton3

from os import environ, listdir
from os.path import isfile, isdir, join
import os
from FolderData import FolderData
from FileData import FileData
from Token import Token
from LibGrades import LibGrades

DEBUG = False

if not DEBUG:
    from multilanguage import Env, Lang, TALcolors
    from TALfiles import TALfilesHelper

    # METADATA OF THIS SERVICE
    args_list = [
        ('problem', str),
        ('service', str),
        ('download', int),
        ('token', str)
    ]

    ENV = Env(args_list)
    TAc = TALcolors(ENV)
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
    TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

def main(problem : str, service : str, token : str, path : str): 
    l = LibGrades()
    l.loadFile(problem, service, token, path)

    if not DEBUG:
            if ENV['download'] == 1:
                TALf.str2output_file(l.getProblemList().instanceToString(), "result.csv")
        
if __name__ == "__main__":
    if DEBUG:
        main("all_problems", "all_service", "123456__RomeoRizzi", os.path.join(os.getcwd(), "log"))
    else:
        main(ENV['problem'], ENV['service'], environ['token'], environ['TAL_META_EXP_LOG_DIR'])
