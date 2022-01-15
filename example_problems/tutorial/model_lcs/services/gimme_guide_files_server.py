#!/usr/bin/env python3
from sys import exit
import os.path

from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper, get_problem_path_from

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('statement.txt',bool),
    ('statement.md',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

print(f"ENV['statement.txt']={ENV['statement.txt']}")
if ENV['statement.txt']:
    fout = open(os.path.join(ENV.OUTPUT_FILES,'statement.txt'),'w')
    print("ciao statement.txt", file=fout)
    fout.close()

if ENV['statement.md']:
    fout = open(os.path.join(ENV.OUTPUT_FILES,'statement.md'),'w')
    print("ciao statement.md", file=fout)
    fout.close()

exit(0)
