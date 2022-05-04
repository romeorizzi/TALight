#!/usr/bin/env pyhton3

from os import environ
import os
from LibGrades import LibGrades

DEBUG = False

if not DEBUG:
    from multilanguage import Env, Lang, TALcolors
    from TALfiles import TALfilesHelper

    # METADATA OF THIS SERVICE
    args_list = [
        ('problem', str),
        ('service', str),
        ('countStudentTries', int),
        ('countProblemOk', int),
        ('countServiceOk', int),
        ('countGoalOk', int),
    ]

    ENV = Env(args_list)
    TAc = TALcolors(ENV)
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
    TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

def main(problem : str, service : str, token : str, path : str): 
    l = LibGrades()
    l.loadFile(problem, service, token, path)

    if ENV['countStudentTries'] == 1:
        a = l.getProblemList().countTokenTries()

        print('Token', 'Total tries', sep='\t')
        for i in a:
            print(i[0], i[1], sep='\t')
    elif ENV['countProblemOk'] == 1:
        a = l.getProblemList().countTokenOkAndNoGoals()

        print('Token', 'OK', sep='\t')
        for i in a:
            print(i[0], i[1], sep='\t')
    elif ENV['countServiceOk'] == 1:
        a = l.getProblemList().countProblemOkAndNoGoals()

        print('Token', 'Problem', 'OK', sep='\t')
        for i in a:
            print(i[0], i[1], i[2], sep='\t')
    elif ENV['countGoalOk'] == 1:
        a = l.getProblemList().countServiceOkAndNoGoals()

        print('Token', 'Problem', 'Service', sep='\t')
        for i in a:
            print(i[0], i[1], i[2], i[3], '\t')
    else:
        print('Invalid choice')

if __name__ == "__main__":
    if DEBUG:
        main("all_problems", "all_service", "123456__RomeoRizzi", os.path.join(os.getcwd(), "log"))
    else:
        main(ENV['problem'], ENV['service'], environ['TAL_META_EXP_TOKEN'], environ['TAL_META_EXP_LOG_DIR'])
