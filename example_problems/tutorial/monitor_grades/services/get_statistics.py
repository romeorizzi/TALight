#!/usr/bin/env pyhton3

from os import environ

from lib_grades import lib_grades
from Token import Token


from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

# METADATA OF THIS SERVICE
args_list = [
    ("problem", str),
    ("service", str),
    ("download", bool),
    ("count_type", str),
    ("student", str),
    ("mode", str),
    ("requirement", str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg="now")
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:


if not Token.isTeacher(environ["TAL_META_EXP_TOKEN"]):
    print("Unauthorized")
else:
    lg = lib_grades()
    lg.loadFile(ENV["problem"], ENV["service"], ENV["student"], environ["TAL_META_EXP_LOG_DIR"])

    if ENV["count_type"] == "tokened_submissions":
        table = lg.getProblemList().countTokenTries(ENV["mode"])

        Token.tupleToTable(("Token", "#Tries"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif ENV["count_type"] == "student_ok_and_no":
        table = lg.getProblemList().countTokenOkAndNoGoals()

        Token.tupleToTable(("Token", "#OK", "#NO"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif ENV["count_type"] == "problem":
        table = lg.getProblemList().countProblemOkAndNoGoals(ENV["requirement"])

        Token.tupleToTable(("Token", "#Problem"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif ENV["count_type"] == "service":
        table = lg.getProblemList().countServiceOkAndNoGoals(ENV["requirement"])

        Token.tupleToTable(("Token", "Problem", "#Service"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif ENV["count_type"] == "goal":
        table = lg.getProblemList().countGoalsOkAndNoGoals()

        Token.tupleToTable(("Token", "Problem", "Service", "#Goal"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    else:
        print("Invalid choice")
