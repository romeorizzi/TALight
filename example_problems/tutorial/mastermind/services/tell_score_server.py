#!/usr/bin/env python3
from engine import *

from multilanguage import *
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
problem = "mastermind"
service = "tell_score_server"
args_list = [('secret_code',str),
    ('probing_code',str),
    ('lang',str),
    ('ISATTY',bool),]

ENV = Env(problem, service, args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

secret_code = ENV['secret_code']
probing_code = ENV['probing_code']
lang = ENV["lang"]

def main():
    pos, col = check(secret_code, probing_code)
    printf(pos, col)

if __name__ == "__main__":
    main()
