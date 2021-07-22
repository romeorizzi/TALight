#!/usr/bin/env python3
from sys import exit
from collections import Counter

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import mastermind_utilities as Utilities


# METADATA OF THIS TAL_SERVICE:
problem="mastermind"
service="check_scoring_competence"
args_list = [
    ('num_pegs',int),
    ('num_colors',int),
    ('lang',str),    
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

print(f"# Notice: the number of pegs is {ENV['num_pegs']} and the number of colors is {ENV['num_colors']}.")
print("# After the key and an attempted solution has been given, I expect to receive the correct punctuation in the form of a sequence of 'w' or 'b' separated by a space or an empty sequence. \nExample:\n   w b w w\n")
# print("# waiting for ...")


def main():
    numPegs = ENV["num_pegs"]
    numColors = ENV["num_colors"]
    if numPegs > numColors:
        TAc.print(LANG.render_feedback("error-generate-randome-pegs-list", f"The number of pegs cannot be greater than the number of colors."), "red", ["bold"])
        exit(0)
    key = Utilities.generateRandomPegsList(numPegs, numColors)
    TAc.print(LANG.render_feedback("key", f"key: {' '.join(map(str, key))}"), ["bold"])
    attempt = Utilities.generateRandomPegsList(numPegs, numColors)
    TAc.print(LANG.render_feedback("attempt", f"attempt: {' '.join(map(str, attempt))}"), ["bold"])
    rightColor, rightPositonAndColor = Utilities.checkAttempt(key, attempt)
    buffer = TALinput(
        str,
        sep=' ',
        regex=r"^(\s|b|w)*$",
        regex_explained="a sequence of b or w separated by a space or an empty line. An example is: 'w b w'.",
        TAc=TAc
    )
    buffer = list(filter(None, buffer))
    result = Counter(buffer)
    if rightColor == result['w'] and rightPositonAndColor == result['b']:
        TAc.print(LANG.render_feedback("right", "The punctuation is correct."), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("error", "The punctuation is wrong."), "red", ["bold"])


if __name__ == "__main__":
    main()
    exit(0)
