#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="light_coin"
service="check_dynamic_strategy"
args_list = [
    ('n', int),
    ('seed',str),
    ('version', str),
    ('lang', str),
    ('ISATTY', bool),
]

from sys import exit
import LightCoinUtilities as Utilities
from TALinputs import TALinput
from TALinputs import MyTALinput
from multilanguage import Env, Lang, TALcolors
import random


# START CODING YOUR SERVICE:
def getScales(coinsNum):
    possibleSolution =  [str(x) for x in range(1, coinsNum + 1)]
    line = MyTALinput(
        str,
        num_tokens=2,
        sep=', ',
        exceptions = possibleSolution,
        regex=r"^(\[([1-9](\s)?)+\])",
        regex_explained="in square brackets, a series of numbers from one to n, separated by a space. An example is: '[1 2], [3 4]'",
        TAc=TAc
    )
    if line[0] in possibleSolution:
        return [int(line[0])]
    rightScale = [int(part) for part in line[0][1:-1].split()]
    leftScale = [int(part) for part in line[1][1:-1].split()]
    if any(item in leftScale for item in rightScale):
        TAc.print(LANG.render_feedback("error-same-coin", "Scales cannot contain the same coin."), "red", ["bold"])
        exit(0)
    if any(item > coinsNum for item in leftScale):
        TAc.print(LANG.render_feedback("error-coins-out-range", f"You have inserted a coin out of range! The range of coins goes from 0 to {coinsNum}."), "red", ["bold"])
        exit(0)
    return [leftScale, rightScale]


def falseCoinIsLeighter():
    while True:
        inputResult = getScales(coinsNum)
        if len(inputResult) == 1:
            possibleLocation = inputResult[0]
            if possibleLocation == falseCoinPos:
                TAc.print(LANG.render_feedback("found-false-coin", 'Congratulations! You have spotted the false coin:'), "green", ["bold"])
                exit(0)
            else:
                TAc.print(LANG.render_feedback("not-found-false-coin", 'Ops, it is not here!'), "red", ["bold"])
                exit(0)
        leftScale, rightScale = inputResult
        result = Utilities.getLighterScale(leftScale, rightScale, falseCoinPos)
        if result == Utilities.LEFT:
            TAc.print(LANG.render_feedback("right-scale-heavier", 'the right scale is heavier'), "green", ["bold"])
        elif result == Utilities.RIGHT:
            TAc.print(LANG.render_feedback("left-scale-heavier", 'the left scale is heavier'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("same-scale-weight", 'the scales have the same weight'), "green", ["bold"])


def falseCoinIsHeavier():
    while True:
        inputResult = getScales(coinsNum)
        if len(inputResult) == 1:
            possibleLocation = inputResult[0]
            if possibleLocation == falseCoinPos:
                TAc.print(LANG.render_feedback("found-false-coin", 'Congratulations! You have spotted the false coin:'), "green", ["bold"])
                exit(0)
            else:
                TAc.print(LANG.render_feedback("not-found-false-coin", 'Ops, it is not here!'), "red", ["bold"])
                exit(0)
        leftScale, rightScale = inputResult
        result = Utilities.getHeavierScale(leftScale, rightScale, falseCoinPos)
        if result == Utilities.LEFT:
            TAc.print(LANG.render_feedback("left-scale-heavier", 'the left scale is heavier'), "green", ["bold"])
        elif result == Utilities.RIGHT:
            TAc.print(LANG.render_feedback("right-scale-heavier", 'the right scale is heavier'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("same-scale-weight", 'the scales have the same weight'), "green", ["bold"])



ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)

LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

coinsNum = ENV['n']
falseCoinPos, seed = Utilities.getRandomFalseCoinPosition(coinsNum, ENV['seed'])
TAc.print(LANG.render_feedback("instance-seed",f"Seed = {seed}"), "yellow", ["bold"])
print("\n")
# print("CoinsNum:", coinsNum)
# print("falseCoinPos", falseCoinPos)

if ENV['version'] == 'false_is_leighter':
    falseCoinIsLeighter()
elif ENV['version'] == 'false_is_heavier':
    falseCoinIsHeavier()  
elif ENV['version'] == 'false_has_different_weight':
    if random.randrange(2):
        falseCoinIsLeighter()
    else:
        falseCoinIsHeavier()
  
exit(0)