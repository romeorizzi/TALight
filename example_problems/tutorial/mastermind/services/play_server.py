#!/usr/bin/env python3
from sys import exit
from collections import Counter
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import mastermind_utilities as Utilities


# METADATA OF THIS TAL_SERVICE:
problem="mastermind"
service="play_server"
args_list = [
    ('max_num_attempts',int),
    ('num_pegs',int),
    ('num_colors',int),
    ('seed',str),
    ('difficulty',str),
    ('lang',str),    
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

if ENV["difficulty"] == "normal":
    if ENV["seed"] == 'random_seed':
        seed = random.randint(100000,999999)    
    else:
        seed = int(ENV["seed"])
    print(LANG.render_feedback("assigned-instance", f"# The assigned instance is:\n#   number of pegs: {ENV['num_pegs']}\n#   number of colors: {ENV['num_colors']}\n#   Seed: "), end="")
    TAc.print(seed, "yellow")
elif ENV["difficulty"] == "hard":
    print(LANG.render_feedback("assigned-instance", f"# The assigned instance is:\n#   number of pegs: {ENV['num_pegs']}\n#   number of colors: {ENV['num_colors']}"))

print(LANG.render_feedback("prompt", f"# Enter your first attempt which must be a sequence of {ENV['num_pegs']} colors separated by spaces.\n# example: \n#   1 4 3 \n# The server will respond with as many 'b' as the colors in the correct position and as many 'w' as the correct colors. \n"))


maxNumAttempts = ENV["max_num_attempts"]
numPegs = ENV["num_pegs"]
numColors = ENV["num_colors"]
if ENV["difficulty"] == "normal":
    secretCode = Utilities.generateRandomPegsList(numPegs, numColors, seed)

count = 0
bufferOld = None
buffer = None
secretCodeAlive = None
while count <= maxNumAttempts - 1:
    count += 1
    bufferOld = buffer
    buffer = TALinput(
        str,
        num_tokens=numPegs,
        regex=r"^([1-" + str(numColors) + "])$",
        regex_explained="a sequence of number from 1 to " + str(numColors) + " separated by spaces. An example is: '4 2 1'.",
        TAc=TAc
    )
    guessedCode = [int(i) for i in buffer]
    if ENV["difficulty"] == "normal":
        rightColor, rightPositonAndColor = Utilities.calculateScore(secretCode, guessedCode)
    elif ENV["difficulty"] == "hard":
        (rightColor, rightPositonAndColor), secretCodeAlive = Utilities.getHardSecretCode(guessedCode, numPegs, numColors, secretCodeAlive)
    result = Utilities.getStringOfResult(rightColor, rightPositonAndColor)
    print(result)
    if rightPositonAndColor == numPegs and rightColor == 0:
        TAc.print(LANG.render_feedback("right-secret-code", f"You found the secret code in {count} attempts."), "green", ["bold"])
        exit(0)

guessedCode = [int(i) for i in buffer]
if ENV["difficulty"] == "normal":
    rightColor, rightPositonAndColor = Utilities.calculateScore(secretCode, guessedCode)
elif ENV["difficulty"] == "hard":
    (rightColor, rightPositonAndColor), secretCodeAlive = Utilities.getHardSecretCode(guessedCode, numPegs, numColors, secretCodeAlive)
if rightPositonAndColor == numPegs:
    TAc.print(LANG.render_feedback("right-secret-code", f"You found the secret code in {count} attempts."), "green", ["bold"])
else:
    if ENV["difficulty"] == "normal":
        TAc.print(LANG.render_feedback("wrong-secret-code", f"You didn't find the secret code, the secret code is [{' '.join(map(str, secretCode))}]"), "red", ["bold"])
    elif ENV["difficulty"] == "hard":
        TAc.print(LANG.render_feedback("wrong-secret-code", f"You didn't find the secret code, the secret code is [{' '.join(map(str, secretCodeAlive[0]))}]"), "red", ["bold"])