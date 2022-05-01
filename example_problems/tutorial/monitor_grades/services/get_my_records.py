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
        ('download', int)
    ]

    ENV = Env(args_list)
    TAc = TALcolors(ENV)
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
    TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

# WARNING: these two enviroment variables are deprecated (introduced now to get the job done, but will be later discharged:
#TAc.print(LANG.render_feedback("TAL_META_EXP_TOKEN", f'TAL_META_ENV.EXP_TOKEN={environ["TAL_META_EXP_TOKEN"]}'), 'red', ['bold'])
#TAc.print(LANG.render_feedback("TAL_META_EXP_LOG_DIR", f'ENV.TAL_META_EXP_LOG_DIR={environ["TAL_META_EXP_LOG_DIR"]}'), 'red', ['bold'])
# END WARNING

#print([ (var_name, environ[var_name]) for var_name in environ if var_name[:4] == "TAL_"])

def main(problem : str, service : str, token : str, path : str): 
    pass


# Student Token
# ----------------------
# Problem: Service
# Goal1 -> OK or NO

if __name__ == "__main__":
    if DEBUG:
        main("all_problems", "all_service", "123456__RomeoRizzi", os.path.join(os.getcwd(), "log"))
    else:
        main(ENV['problem'], ENV['service'], environ['TAL_META_EXP_TOKEN'], environ['TAL_META_EXP_LOG_DIR'])

# formato della cartella:
# 123456_RomeoRizzi+Problem+Service+2022-02-24_20-56-54_425

# formato del file contenuto nella cartella:
# OK_nomeproblema_nomeservizio_goal
