#!/usr/bin/env pyhton3

from os import environ, listdir
from os.path import isfile, isdir, join
import os
from FolderData import FolderData
from FileData import FileData
from Token import Token

DEBUG = False

if not DEBUG:
    from multilanguage import Env, Lang, TALcolors
    import monitor_grades_lib as mgl
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

ALLPROBLEM = "all_problems"
ALLSERVICE = "all_services"
OKCONSTANT = "OK"

problemlist = Token()

def main(problem : str, service : str, token : str, path : str): 
    for x in listdir(path):
        fullpath = os.path.join(path, x)
        if (isdir(fullpath)):
            folderdata = FolderData(x, fullpath)

            if (folderdata.token == token or ("__" in token)):
                for y in listdir(fullpath):
                    filedata = FileData(y, os.path.join(fullpath, y), folderdata)
                        
                    if (filedata.folderdata.problem == problem or problem == ALLPROBLEM):
                        if (filedata.folderdata.service == service or service == ALLSERVICE):
                            problemlist.addToken(filedata)

    for x in problemlist.countTokenTries():
        print("Total tries [", x[1], ']:', x[1])
    problemlist.printToConsole()

    if not DEBUG:
        if ENV['download'] == 1:
            TALf.str2output_file(problemlist.instanceToString(), "result.csv")

# Student Token
# ----------------------
# Problem: Service
# Goal1 -> OK or NO

if __name__ == "__main__":
    if DEBUG:
        main(ALLPROBLEM, ALLSERVICE, "123456__RomeoRizzi", os.path.join(os.getcwd(), "log"))
    else:
        main(ENV['problem'], ENV['service'], environ['TAL_META_EXP_TOKEN'], environ['TAL_META_EXP_LOG_DIR'])

# formato della cartella:
# 123456_RomeoRizzi+2022-02-24_20-56-54_425

# formato del file contenuto nella cartella:
# OK_nomeproblema_nomeservizio_goal
