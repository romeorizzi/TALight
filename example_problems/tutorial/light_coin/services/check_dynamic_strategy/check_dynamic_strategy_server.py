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
from multilanguage import Env, Lang, TALcolors
import random


# START CODING YOUR SERVICE:
def getScales(coinsNum):
    leftScale = 0
    haveSameCoin = True
    while haveSameCoin:
        isValidScaled = False
        while not isValidScaled:
            leftScale = Utilities.getInputScale( \
                LANG.render_feedback("insert-coins-left-place", 'Coins in the left scale:'), \
                LANG.render_feedback("error-input-int", 'The position of the coin must be an integer.'), \
                TAc \
            )
            if any(i > coinsNum for i in leftScale):
                TAc.print(LANG.render_feedback("error-coins-out-range", f"You have inserted a coin out of range! The range of coins goes from 0 to {coinsNum}."), "red", ["bold"])
                isValidScaled = False
            else:
                isValidScaled = True
        rightScale = 0
        isValidScaled = False
        while not isValidScaled:
            rightScale = Utilities.getInputScale( \
                LANG.render_feedback("insert-coins-right-place", 'Coins in the right scale:'), \
                LANG.render_feedback("error-input-int", 'The position of the coin must be an integer.'), \
                TAc \
            )
            if any(i > coinsNum for i in rightScale):
                TAc.print(LANG.render_feedback("error-coins-out-range", f"You have inserted a coin out of range! The range of coins goes from 0 to {coinsNum}."), "red", ["bold"])
                isValidScaled = False
            else:
                isValidScaled = True
        # Check if scales contains the same coin
        if any(item in leftScale for item in rightScale):
            TAc.print(LANG.render_feedback("error-same-coin", "Scales cannot contain the same coin."), "red", ["bold"])
            haveSameCoin = True
        else:
            haveSameCoin = False
    return leftScale, rightScale

def falseCoinIsLeighter():
    isFound = False
    while not isFound:
        leftScale, rightScale = getScales(coinsNum)
        result = Utilities.getLighterScale(leftScale, rightScale, falseCoinPos)
        if result == Utilities.LEFT:
            TAc.print(LANG.render_feedback("right-scale-heavier", 'the right scale is heavier'), "green", ["bold"])
        elif result == Utilities.RIGHT:
            TAc.print(LANG.render_feedback("left-scale-heavier", 'the left scale is heavier'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("same-scale-weight", 'the scales have the same weight'), "green", ["bold"])
        print("\n")
        TAc.print(LANG.render_feedback("postion-question", 'If you found the false coin insert its position (no otherwise):'), "yellow", ["bold"])
        try:
            possibleLocation = int(input())
            if possibleLocation == falseCoinPos:
                TAc.print(LANG.render_feedback("found-false-coin", 'Congratulations! You have spotted the false coin:'), "green", ["bold"])
                isFound = True
            else:
                TAc.print(LANG.render_feedback("not-found-false-coin", 'Ops, it is not here! Try again with other weighs.'), "red", ["bold"])
                isFound = False
        except ValueError:
            isFound = False

def falseCoinIsHeavier():
    isFound = False
    while not isFound:
        leftScale, rightScale = getScales(coinsNum)
        result = Utilities.getHeavierScale(leftScale, rightScale, falseCoinPos)
        if result == Utilities.LEFT:
            TAc.print(LANG.render_feedback("left-scale-heavier", 'the left scale is heavier'), "green", ["bold"])
        elif result == Utilities.RIGHT:
            TAc.print(LANG.render_feedback("right-scale-heavier", 'the right scale is heavier'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("same-scale-weight", 'the scales have the same weight'), "green", ["bold"])
        print("\n")
        TAc.print(LANG.render_feedback("postion-question", 'If you found the false coin insert its position:'), "yellow", ["bold"])
        try:
            possibleLocation = int(input())
            if possibleLocation == falseCoinPos:
                TAc.print(LANG.render_feedback("found-false-coin", 'Congratulations! You have spotted the false coin:'), "green", ["bold"])
                isFound = True
            else:
                TAc.print(LANG.render_feedback("not-found-false-coin", 'Ops, it is not here! Try again with other weighs.'), "red", ["bold"])
                isFound = False
        except ValueError:
            isFound = False



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