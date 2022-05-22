#!/usr/bin/env pyhton3

from os import environ
import os

from lib_grades import lib_grades
from Token import Token


from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

# METADATA OF THIS SERVICE
args_list = [
    ("problem", str),
    ("service", str),
    ("download", int),
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


def main(
    problem: str, service: str, token: str, path: str, counttype: str, student: str
):
    if not Token.isTeacher(token):
        print("Unauthorized")
        return

    lg = lib_grades()
    lg.loadFile(problem, service, student, path)

    if counttype == "student_tries":
        table = lg.getProblemList().countTokenTries(ENV["mode"])

        Token.tupleToTable(("Token", "#Tries"), table)

        if ENV["download"] == 1:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif counttype == "student_ok_and_no":
        table = lg.getProblemList().countTokenOkAndNoGoals()

        Token.tupleToTable(("Token", "#OK", "#NO"), table)

        if ENV["download"] == 1:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif counttype == "problem":
        table = lg.getProblemList().countProblemOkAndNoGoals(ENV["requirement"])

        Token.tupleToTable(("Token", "#Problem"), table)

        if ENV["download"] == 1:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif counttype == "service":
        table = lg.getProblemList().countServiceOkAndNoGoals(ENV["requirement"])

        Token.tupleToTable(("Token", "Problem", "#Service"), table)

        if ENV["download"] == 1:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    elif counttype == "goal":
        table = lg.getProblemList().countGoalsOkAndNoGoals()

        Token.tupleToTable(("Token", "Problem", "Service", "#Goal"), table)

        if ENV["download"] == 1:
            TALf.str2output_file(Token.tupleToFile(table), "result.csv")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main(
        ENV["problem"],
        ENV["service"],
        environ["TAL_META_EXP_TOKEN"],
        environ["TAL_META_EXP_LOG_DIR"],
        ENV["count_type"],
        ENV["student"],
    )
