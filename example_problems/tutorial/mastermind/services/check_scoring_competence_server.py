#!/usr/bin/env python3
from engine import *

from multilanguage import *
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
problem = "mastermind"
service = "check_scoring_competence"
args_list = [('num_questions',int),
    ('num_pegs',int),
    ('num_colors',int),
    ('lang',str),    
    ('ISATTY',bool),]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

num_questions = ENV["num_questions"]
num_pegs = ENV["num_pegs"]
num_colors = ENV["num_colors"]
lanbg = ENV["lang"]

def main():
    if isCorrect(num_pegs, num_colors, num_questions):
        TAc.OK()
    else:
        TAc.NO()

if __name__ == "__main__":
    main()
