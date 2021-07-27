#!/usr/bin/env python3
from sys import exit
from collections import Counter
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import mastermind_utilities as Utilities


# METADATA OF THIS TAL_SERVICE:
problem="mastermind"
service="check_scoring_competence"
args_list = [
    ('num_pegs',int),
    ('num_colors',int),
    ('seed',str),
    ('feedback',str),
    ('lang',str),    
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

if ENV["seed"] == 'random_seed':
    seed = random.randint(100000,999999)    
else:
    seed = int(ENV["seed"])

numPegs = ENV["num_pegs"]
numColors = ENV["num_colors"]
secretCode = Utilities.generateRandomPegsList(numPegs, numColors, seed)
print(LANG.render_feedback("assigned-instance", f"# The assigned instance is:\n#   number of pegs: {ENV['num_pegs']}\n#   number of colors: {ENV['num_colors']}\n#   Seed: "), end="")
TAc.print(seed, "yellow")
TAc.print(LANG.render_feedback("secret-code", f"secret code:  {' '.join(map(str, secretCode))}"), ["bold"])
guessedCode = Utilities.generateRandomPegsList(numPegs, numColors, random.randint(100000,999999))
TAc.print(LANG.render_feedback("guessed-code", f"guessed code: {' '.join(map(str, guessedCode))}"), ["bold"])
print(LANG.render_feedback("prompt", "# Enter your evaluation in the form of a possibly empty sequence of 'w' and 'b' characters (separated by spaces). \n# Example:\n#   b w w\n"))
rightColor, rightPositonAndColor = Utilities.calculateScore(secretCode, guessedCode)
buffer = TALinput(
    str,
    regex=r"^(b|w)*$",
    regex_explained="a possibly empty sequence of 'w' and 'b' characters (separated by spaces). An example is: 'w b w'.",
    TAc=TAc
)
result = Counter(buffer)
if rightColor == result['w'] and rightPositonAndColor == result['b']:
    TAc.print(LANG.render_feedback("right", "Your scoring is correct!"), "green", ["bold"])
else:
    if ENV["feedback"] == "yes_no":
        TAc.print(LANG.render_feedback("error", "Your scoring is wrong."), "red", ["bold"])
    else:
        result = Utilities.getStringOfResult(rightColor, rightPositonAndColor)
        TAc.print(LANG.render_feedback("error-solution", f"Your scoring is wrong. The solution is {result}"), "red", ["bold"])
