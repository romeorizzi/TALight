#!/usr/bin/env python3
from sys import exit
from collections import Counter
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import mastermind_utilities as Utilities


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('num_pegs',int),
    ('num_colors',int),
    ('feedback',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

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
probingCode = Utilities.generateRandomPegsList(numPegs, numColors, random.randint(100000,999999))
TAc.print(LANG.render_feedback("probing-code", f"probing code: {' '.join(map(str, probingCode))}"), ["bold"])
print(LANG.render_feedback("prompt", "# Enter your evaluation in the form of a possibly empty sequence of 'w' and 'b' characters (separated by spaces). \n# Example:\n#   b w w\n"))
buffer = TALinput(
    str,
    regex=r"^(b|w)*$",
    regex_explained="a possibly empty sequence of 'w' and 'b' characters (separated by spaces). An example is: 'w b w'.",
    TAc=TAc
)
user_scoring = Counter(buffer)
numWhites, numBlacks = Utilities.calculateScore(secretCode, probingCode)
if numWhites == user_scoring['w'] and numBlacks == user_scoring['b']:
    TAc.print(LANG.render_feedback("right", "Ok! Your scoring is correct!"), "green", ["bold"])
else:
    if ENV["feedback"] == "yes_no":
        TAc.print(LANG.render_feedback("error", "No! Your scoring is wrong."), "red", ["bold"])
    elif ENV["feedback"] == "provide_correct_score":
        correct_scoring = Utilities.getStringOfResult(numWhites, numBlacks)
        TAc.print(LANG.render_feedback("error-score", f"No! Your scoring is wrong. The correct score is {correct_scoring}"), "red", ["bold"])
    else:
        if numBlacks != user_scoring['b']:
            TAc.print(LANG.render_feedback("black-score", f"No! The number of positions where the probing code and the secret code have the same color is not {user_scoring['b']}."), "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback("black-score", f"No! We agree that the number of positions where the probing code and the secret code have the same color is {user_scoring['b']} (ok!). However, the number of correct but out of place colors is not {user_scoring['w']}."), "red", ["bold"])

