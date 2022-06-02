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
    ("all_submissions", bool),
    ("student", str),
    ("download", bool),
    ("csv_filename", str),
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
    lg.getProblemList().printToConsole(ENV["all_submissions"])
    if ENV["download"]:
        TALf.str2output_file(
            lg.getProblemList().instanceToString(ENV["all_submissions"]), ENV["csv_filename"]
        )
