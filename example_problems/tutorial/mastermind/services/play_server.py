#!/usr/bin/env python3
from engine import *

from multilanguage import *
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
problem = "mastermind"
service = "play"
args_list = [('max_num_attempts',str),
    ('num_pegs',str),
    ('num_colors',str),
    ('lang',str),
    ('ISATTY',bool),]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

num_pegs = ENV['num_pegs']
num_colors = ENV['num_colors']
max_num_attempts = ENV['max_num_attempts']
lang = ENV["lang"]

def main():
    if play(num_pegs, num_colors, max_num_attempts):
        TAc.OK()
    else:
        TAc.NO()

if __name__ == "__main__":
    main()
