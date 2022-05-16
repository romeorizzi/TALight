#!/usr/bin/env pyhton3

from os import environ
import os

from LibGrades import LibGrades
from Token import Token

DEBUG = True

if not DEBUG:
    from multilanguage import Env, Lang, TALcolors
    from TALfiles import TALfilesHelper

    # METADATA OF THIS SERVICE
    args_list = [
        ('problem', str),
        ('service', str),
        ('download', int),
        ('student', int),
        ('countStudentTries', int),
        ('countStudentOkAndNo', int),
        ('countProblemOk', int),
        ('countServiceOk', int),
        ('countGoalOk', int),
    ]

    ENV = Env(args_list)
    TAc = TALcolors(ENV)
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
    TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

def main(problem : str, service : str, token : str, path : str, counttype : str, student : str):
    if (("__" in token) == False):
        print('Unauthorized')
        return

    lg = LibGrades()
    lg.loadFile(problem, service, student, path)

    if counttype == "student_tries":
        a = lg.getProblemList().countTokenTries()

        Token.tupleToTable(("Token", "#Tries"))
        Token.tupleToTable(a)

        if ENV['download'] == 1:
            TALf.str2output_file(Token.tupleToFile(a), "result.csv")
    elif counttype == "student_ok_and_no":
        a = lg.getProblemList().countTokenOkAndNoGoals()

        Token.tupleToTable(('Token', '#OK', '#NO'))
        Token.tupleToTable(a)

        if ENV['download'] == 1:
            TALf.str2output_file(Token.tupleToFile(a), "result.csv")
    elif counttype == "problem":
        a = lg.getProblemList().countProblemOkAndNoGoals()

        Token.tupleToTable(("Token", "#Problem"))
        Token.tupleToTable(a)
        
        if ENV['download'] == 1:
            TALf.str2output_file(Token.tupleToFile(a), "result.csv")
    elif counttype == "service":
        a = lg.getProblemList().countServiceOkAndNoGoals()

        Token.tupleToTable(("Token", "Problem", "#Service"))
        Token.tupleToTable(a)

        if ENV['download'] == 1:
            TALf.str2output_file(Token.tupleToFile(a), "result.csv")
    elif counttype == "goal":
        a = lg.getProblemList().countGoalsOkAndNoGoals()

        Token.tupleToTable(('Token', 'Problem', 'Service', '#Goal'))
        Token.tupleToTable(a)

        if ENV['download'] == 1:
            TALf.str2output_file(Token.tupleToFile(a), "result.csv")
    else:
        print('Invalid choice')

if __name__ == "__main__":
    if DEBUG:
        main("all_problems", "all_services", "123456__RomeoRizzi", os.path.join(os.getcwd(), "log_algorithms"), "problem", "all_students")
    else:
        main(ENV['problem'], ENV['service'], environ['TAL_META_EXP_TOKEN'], environ['TAL_META_EXP_LOG_DIR'], ENV['count_type']. ENV['student'])
