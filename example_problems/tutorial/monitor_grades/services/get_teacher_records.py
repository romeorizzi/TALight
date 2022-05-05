#!/usr/bin/env pyhton3

from os import environ
import os
from LibGrades import LibGrades
from Token import Token

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

        Token.tupleToTable(("Token", "Course"))
        Token.tupleToTable(a, 2)
    elif ENV['countProblemOk'] == 1:
        a = l.getProblemList().countTokenOkAndNoGoals()

        Token.tupleToTable(('Token', 'OK'))
        Token.tupleToTable(a, 2)
    elif ENV['countServiceOk'] == 1:
        a = l.getProblemList().countProblemOkAndNoGoals()

        Token.tupleToTable(("Token", "Problem", "OK"))
        Token.tupleToTable(a, 3)
    elif ENV['countGoalOk'] == 1:
        a = l.getProblemList().countServiceOkAndNoGoals()

        Token.tupleToTable(("Token", "Problem", "Service", "OK"))
        Token.tupleToTable(a, 4)
    else:
        print('Invalid choice')

if __name__ == "__main__":
    if DEBUG:
        main("all_problems", "all_service", "123456__RomeoRizzi", os.path.join(os.getcwd(), "log"))
    else:
        main(ENV['problem'], ENV['service'], environ['TAL_META_EXP_TOKEN'], environ['TAL_META_EXP_LOG_DIR'])
