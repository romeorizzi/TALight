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
    ("csv_filename", str),
    ("regex_filename", str),
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
        ENV["problem"],
        ENV["service"],
        ENV["student"],
        environ["TAL_META_EXP_LOG_DIR"],
        ENV["regex_filename"],
    )

    if str(ENV["watch"]).startswith("num_total_"):
        table = lg.getProblemList().countTokenTriesWithoutStudent(ENV["watch"])

        Token.tupleToTable(("#Tries"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), ENV["csv_filename"])
    elif ENV["watch"] == "num_ok_and_no":
        table = lg.getProblemList().countTokenOkAndNoGoalsWithoutStudent()

        Token.tupleToTable(("#OK", "#NO"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), ENV["csv_filename"])
    elif str(ENV["watch"]).startswith("num_problems_"):
        table = lg.getProblemList().countProblemOkAndNoGoalsWithoutStudent(ENV["watch"])

        Token.tupleToTable(("#Problem"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), ENV["csv_filename"])
    elif str(ENV["watch"]).startswith("num_services_"):
        table = lg.getProblemList().countServiceOkAndNoGoalsWithoutStudent(ENV["watch"])

        Token.tupleToTable(("Problem", "#Service"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), ENV["csv_filename"])
    elif str(ENV["watch"]).startswith("num_goals_"):
        table = lg.getProblemList().countGoalsOkAndNoGoalsWithoutStudent()

        Token.tupleToTable(("Problem", "Service", "#Goal"), table)

        if ENV["download"]:
            TALf.str2output_file(Token.tupleToFile(table), ENV["csv_filename"])
    else:
        print("Invalid choice")
