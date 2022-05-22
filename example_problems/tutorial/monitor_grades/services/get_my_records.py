#!/usr/bin/env pyhton3

from os import environ
import os
from lib_grades import lib_grades

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

# METADATA OF THIS SERVICE
args_list = [
    ("problem", str),
    ("service", str),
    ("all_submissions", int),
    ("download", int),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg="now")
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:


def main(problem: str, service: str, token: str, path: str):
    lg = lib_grades()
    lg.loadFile(problem, service, token, path)

    lg.getProblemList().printToConsole(ENV["all_submissions"] == 1)

    if ENV["download"] == 1:
        TALf.str2output_file(lg.getProblemList().instanceToString(True), "result.csv")


if __name__ == "__main__":
    main(
        ENV["problem"],
        ENV["service"],
        environ["TAL_META_EXP_TOKEN"],
        environ["TAL_META_EXP_LOG_DIR"],
    )
