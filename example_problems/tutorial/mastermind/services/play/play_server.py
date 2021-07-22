#!/usr/bin/env python3
from sys import exit
from collections import Counter

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
    ('lang',str),    
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

stopping_command_set="#end"
print(f"# Notice: the number of pegs is {ENV['num_pegs']}, the number of colors is {ENV['num_colors']} and the max number of attempts is {ENV['max_num_attempts']}")
print("#? waiting for your first attempt like for example: \n   1 4 3 \nThe server will respond with as many 'b' as the colors in the correct position and as many 'w' as the correct colors. \n")



def main():
    maxNumAttempts = ENV["max_num_attempts"]
    numPegs = ENV["num_pegs"]
    numColors = ENV["num_colors"]
    if numPegs > numColors:
        TAc.print(LANG.render_feedback("error-generate-randome-pegs-list", f"The number of pegs cannot be greater than the number of colors."), "red", ["bold"])
        exit(0)
    secretCode = Utilities.generateRandomPegsList(numPegs, numColors)

    count = 0
    bufferOld = None
    buffer = None
    while count <= maxNumAttempts:
        count += 1
        bufferOld = buffer
        buffer = TALinput(
            str,
            exceptions = {stopping_command_set},
            num_tokens=numPegs,
            sep=' ',
            regex=r"^([1-" + str(numColors) + "])$",
            regex_explained="a sequence of number from 1 to " + str(numColors) + " separated by a space. An example is: '4 2 1'.",
            TAc=TAc
        )
        if buffer[0] != stopping_command_set:
            attempt = [int(i) for i in buffer]
            rightColor, rightPositonAndColor = Utilities.checkAttempt(secretCode, attempt)
            result = Utilities.getStringOfResult(rightColor, rightPositonAndColor)
            print(result)
        else:
            oldAttempt = [int(i) for i in bufferOld]
            rightColor, rightPositonAndColor = Utilities.checkAttempt(secretCode, oldAttempt) 
            if rightPositonAndColor == numPegs:
                TAc.print(LANG.render_feedback("right-secret-code", f"You found the secret code in {count - 1} attempts."), "green", ["bold"])
            else:
                TAc.print(LANG.render_feedback("wrong-secret-code", f"You didn't find the secret code, the secret code is [{' '.join(map(str, secretCode))}]"), "red", ["bold"])
            exit(0)

    attempt = [int(i) for i in buffer]
    rightColor, rightPositonAndColor = Utilities.checkAttempt(secretCode, attempt)
    if rightPositonAndColor == numPegs:
        TAc.print(LANG.render_feedback("right-secret-code", f"You found the secret code in {count - 1} attempts."), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("wrong-secret-code", f"You didn't find the secret code, the secret code is [{' '.join(map(str, secretCode))}]"), "red", ["bold"])


if __name__ == "__main__":
    main()
    exit(0)
