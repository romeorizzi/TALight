#!/usr/bin/env python3
from sys import exit
import os.path

from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('flag_instance',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
print(f"ENV.INPUT_FILES={ENV.INPUT_FILES}")
file_instance = os.path.join(ENV.INPUT_FILES,'instance')
file_model = os.path.join(ENV.INPUT_FILES,'model')
file_datafile = os.path.join(ENV.INPUT_FILES,'datafile')
if os.path.isfile(file_instance):
    instance=open(file_instance,'r').readlines()
else:
    file_instance=["marcondirondello","martello"]

mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))


exit(0)
