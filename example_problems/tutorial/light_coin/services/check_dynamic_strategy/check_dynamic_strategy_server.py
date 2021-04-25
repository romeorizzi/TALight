#!/usr/bin/env python3
from sys import exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import LightCoinUtilities as Utilities

# METADATA OF THIS TAL_SERVICE:
problem="light_coin"
service="check_dynamic_strategy"
args_list = [
    ('n', int),
    ('version', str),
    ('lang', str),
    ('ISATTY', bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)

LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

stopping_command_set="#end"
print(f"# Notice: the n={ENV['n']} coins are numbered from 1 to {ENV['n']}.")
print("# waiting for the list of measures comprising your dynamic strategy.\nPlease, each measure should go on a different line and specify the coins on the left plate, then a comma, then the coins on the tight plate.\nExample:\n   1 3 5, 2 4 6.\nWhen you send a measure you get the result immediately and after that you can enter the next measure.\nWhen you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete. Any other line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file whose last line is '#end'. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself waiting for the list of measures comprising your dynamic strategy.\n")


def manageScale(leftScale, rightScale, trueCoins, falseCoinIsLeighter, differentWeight=False):
    if differentWeight:
        result, trueCoins = Utilities.makeDynamicWeigh(leftScale, rightScale, trueCoins, ENV['n'])
    else:
        if falseCoinIsLeighter:
            result, trueCoins = Utilities.makeDynamicWeighWithFalseLighter(leftScale, rightScale, trueCoins, ENV['n'])
        else:
            result, trueCoins = Utilities.makeDynamicWeighWithFalseHeavier(leftScale, rightScale, trueCoins, ENV['n'])

    if result == Utilities.LEFT:
        TAc.print(LANG.render_feedback("left-scale-heavier", 'The left scale is heavier'), "green", ["bold"])
    elif result == Utilities.RIGHT:
        TAc.print(LANG.render_feedback("right-scale-heavier", 'The right scale is heavier'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("same-scale-weight", 'The scales have the same weight'), "green", ["bold"])
    return trueCoins


def manageFinal(trueCoins):
    result = []
    for i in range(1, ENV['n'] + 1):
        if i not in trueCoins:
            result.append(i)
    if len(result) == 1:
        TAc.print(LANG.render_feedback("found-false-coin", 'Congratulations! Your strategy finds the false coin.'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("ambiguos-strategy", f'Your strategy is ambiguous because it doesn\'t distinguish the coins {result}.'), "red", ["bold"])


def getScales(falseCoinIsLeighter=None, differentWeight=False):
    trueCoins = set()
    line = [0]
    while line[0] != stopping_command_set:
        line = TALinput(
            str,
            num_tokens=2,
            sep=', ',
            exceptions = stopping_command_set,
            regex=r"^(([1-9][0-9]{0,9}\s+)*[1-9][0-9]{0,9}\s*)$",
            regex_explained="a sequence of numbers from 1 to n, separated by a space. An example of what should go on a plate of the scale (one of the two expected token of the line) is: '2 5 7'.",
            TAc=TAc
        )
        if line[0] != stopping_command_set:
            leftScale = [int(part) for part in line[0].split()]
            rightScale = [int(part) for part in line[1].split()]
            if any(item in leftScale for item in rightScale):
                TAc.print(LANG.render_feedback("error-same-coin", "A same coin can not be place on both plates of the scale (within a same maesure)."), "red", ["bold"])
                exit(0)
            if any(item > ENV['n'] for item in leftScale):
                TAc.print(LANG.render_feedback("error-coins-out-range", f"You have inserted a coin out of range! The range of coin labels goes from 1 to {ENV['n']}."), "red", ["bold"])
                exit(0)
            trueCoin = manageScale(leftScale, rightScale, trueCoins, falseCoinIsLeighter, differentWeight)
    manageFinal(trueCoins)


if ENV['version'] == 'false_is_leighter':
    getScales(falseCoinIsLeighter=True)
elif ENV['version'] == 'false_is_heavier':
    getScales(falseCoinIsLeighter=False)  
elif ENV['version'] == 'false_has_different_weight':
    getScales(differentWeight=True)
exit(0)