#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="light_coin"
service="check_static_strategy"
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

def getWeighedList():
    weighedList = []
    while True:
        TAc.print(LANG.render_feedback("input-choice", "Type 'i' to insert a new weight or 'q' to end: "), "yellow", ["bold"])
        i = input()
        if i == 'i' or i == 'I':
            leftScale, rightScale = getScales(coinsNum)
            weighedList.append([leftScale, rightScale])
        elif i == 'q' or i == 'Q':
            return weighedList

def getPossibleFalseCoin(weighedResults):
    possibleSolution = []
    maxValue = max(weighedResults)
    for i in range(len(weighedResults)):
        if weighedResults[i] == maxValue:
            possibleSolution.append(i + 1)
    return possibleSolution

def checkSolution(possibleSolution):
    if len(possibleSolution) == 1:
        if falseCoinPos == possibleSolution[0]:
            TAc.print(LANG.render_feedback("found-false-coin", f'Congratulations! You have spotted the false coin in {falseCoinPos} position.'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("not-found-false-coin", f'Ops, your strategy doesn\'t work, according to it the false coin is in {possibleSolution[0]} positions but is in {falseCoinPos} position.'), "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback("ambiguos-strategy", f'Your strategy is ambiguous because it returns {len(possibleSolution)} possible positions which are {possibleSolution} and the false coin is in {falseCoinPos} position.'), "red", ["bold"])

def doWeighed(weighedList, falseCoinLighter):
    weighedResults = [0] * coinsNum
    for leftScale, rightScale in weighedList:
        if falseCoinLighter:
            result = Utilities.getLighterScale(leftScale, rightScale, falseCoinPos)
        else:
            result = Utilities.getHeavierScale(leftScale, rightScale, falseCoinPos)
        if result == Utilities.LEFT:
            for i in leftScale:
                weighedResults[i-1] += 1
        elif result == Utilities.RIGHT:
            for i in rightScale:
                weighedResults[i-1] += 1
        else:
            for i in leftScale:
                weighedResults[i-1] -= 1
            for i in rightScale:
                weighedResults[i-1] -= 1
    possibleSolution = getPossibleFalseCoin(weighedResults)
    checkSolution(possibleSolution)
    
def falseCoinIsLeighter():
    weighedList = getWeighedList()
    doWeighed(weighedList, True)

def falseCoinIsHeavier():
    weighedList = getWeighedList()
    doWeighed(weighedList, True)


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