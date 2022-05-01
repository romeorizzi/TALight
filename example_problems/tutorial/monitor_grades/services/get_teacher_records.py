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
        ('countTotalTries', int),
        ('countTotalOkAndNo', int),
        ('countProblem', int),
        ('countService', int),
    ]

    ENV = Env(args_list)
    TAc = TALcolors(ENV)
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
    TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

def main(problem : str, service : str, token : str, path : str): 
    l = LibGrades()
    l.loadFile(problem, service, token, path)

    if ENV['countTotalTries'] == 1:
        a = l.getProblemList().countTokenTries()

        for i in a:
            print(i[0], i[1])
    elif ENV['countTotalOkAndNo'] == 1:
        a = l.getProblemList().countTokenOkAndNoGoals()

        for i in a:
            print(i[0], i[1])
    elif ENV['countProblem'] == 1:
        a = l.getProblemList().countProblemOkAndNoGoals()

        for i in a:
            print(i[0], i[1], i[2])
    elif ENV['countService'] == 1:
        a = l.getProblemList().countServiceOkAndNoGoals()

        for i in a:
            print(i[0], i[1], i[2], i[3])
    else:
        raise

if __name__ == "__main__":
    if DEBUG:
        main("all_problems", "all_service", "123456__RomeoRizzi", os.path.join(os.getcwd(), "log"))
    else:
        main(ENV['problem'], ENV['service'], environ['TAL_META_EXP_TOKEN'], environ['TAL_META_EXP_LOG_DIR'])
