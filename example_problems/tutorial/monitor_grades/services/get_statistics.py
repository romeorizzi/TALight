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
    ("watch", str),
    ("student", str),
    ("mode", str),
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
    lg.loadFile(
        ENV["problem"], ENV["service"], ENV["student"], environ["TAL_META_EXP_LOG_DIR"]
    )

    if ENV["watch"] == "num_tokened_submissions":
        table = lg.getProblemList().countTokenTries(ENV["mode"])

        Token.tupleToTable(("Token", "#Tries"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif ENV["watch"] == "num_ok_and_no":
        table = lg.getProblemList().countTokenOkAndNoGoals()

        Token.tupleToTable(("Token", "#OK", "#NO"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif str(ENV["watch"]).startswith("num_problems_"):
        table = lg.getProblemList().countProblemOkAndNoGoals(ENV["watch"])

        Token.tupleToTable(("Token", "#Problem"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif str(ENV["watch"]).startswith("num_services_"):
        table = lg.getProblemList().countServiceOkAndNoGoals(ENV["watch"])

        Token.tupleToTable(("Token", "Problem", "#Service"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif str(ENV["watch"]).startswith("num_goals_"):
        table = lg.getProblemList().countGoalsOkAndNoGoals()

        Token.tupleToTable(("Token", "Problem", "Service", "#Goal"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    else:
        print("Invalid choice")
