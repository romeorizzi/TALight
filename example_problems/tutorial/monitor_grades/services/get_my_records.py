#!/usr/bin/env pyhton3

from os import environ
from lib_grades import lib_grades

from multilanguage import Env, Lang, TALcolors
from TALfiles import TALfilesHelper

# METADATA OF THIS SERVICE
args_list = [
    ("problem", str),
    ("service", str),
    ("all_submissions", bool),
    ("download", bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg="now")
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:

lg = lib_grades()
lg.loadFile(ENV["problem"], ENV["service"], environ["TAL_META_EXP_TOKEN"], environ["TAL_META_EXP_LOG_DIR"])
lg.getProblemList().printToConsole(ENV["all_submissions"] == 1)
if ENV["download"]:
    TALf.str2output_file(lg.getProblemList().instanceToString(ENV["all_submissions"]), "result.csv")
