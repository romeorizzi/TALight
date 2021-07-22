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
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

print(f"# Notice: the secret code entered is [{ENV['secret_code']}] and the probing code is [{ENV['probing_code']}].\n")


def main():
    secret_code = [int(s) for s in ENV["secret_code"].split()]
    probing_code = [int(s) for s in ENV["probing_code"].split()]
    if len(secret_code) != len(probing_code):
        TAc.print(LANG.render_feedback("error-len-probing_code", f"The length of the probing code must be the same as that of the secret code."), "red", ["bold"])
        exit(0)
    rightColor, rightPositonAndColor = Utilities.checkAttempt(secret_code, probing_code)
    result = Utilities.getStringOfResult(rightColor, rightPositonAndColor)
    print(result)


if __name__ == "__main__":
    main()
    exit(0)
