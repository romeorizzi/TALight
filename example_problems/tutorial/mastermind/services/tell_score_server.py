#!/usr/bin/env python3
from sys import exit
from collections import Counter

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import mastermind_utilities as Utilities


# METADATA OF THIS TAL_SERVICE:
problem="mastermind"
service="tell_score"
args_list = [
    ('secret_code',str),
    ('probing_code',str),
    ('lang',str),    
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

print(LANG.render_feedback("your-input", f"Secret code entered:  {ENV['secret_code']}\nProbing code entered: {ENV['probing_code']}\n"))
secretCode = [int(s) for s in ENV["secret_code"].split()]
probingCode = [int(s) for s in ENV["probing_code"].split()]
if len(secretCode) != len(probingCode):
    TAc.print(LANG.render_feedback("error-len-probing_code", f"The length of the probing code must be the same as that of the secret code."), "red", ["bold"])
    exit(0)
rightColor, rightPositonAndColor = Utilities.calculateScore(secretCode, probingCode)
result = Utilities.getStringOfResult(rightColor, rightPositonAndColor)
print(LANG.render_feedback("correct-evaluation", f"Evaluation: {result}"))

