#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="light_coin"
service="check_static_strategy"
args_list = [
    ('n', int),
    ('version', str),
    ('lang', str),
    ('ISATTY', bool),
]

from sys import exit
import LightCoinUtilities as Utilities
from TALinputs import TALinput
from TALinputs import MyTALinput
from multilanguage import Env, Lang, TALcolors

# START CODING YOUR SERVICE:
def getStaticStrategy(coinsNum):
    weighedList = []
    stoppingCommand = "end"
    line = [0]
    while line[0] != stoppingCommand:
        line = MyTALinput(
            str,
            num_tokens=2,
            sep=', ',
            exceptions = stoppingCommand,
            regex=r"^(\[([1-9](\s)?)+\])",
            regex_explained="in square brackets, a series of numbers from one to n, separated by a space. An example is: '[1 2], [3 4]'",
            TAc=TAc
        )
        if line[0] != stoppingCommand:
            rightScale = [int(part) for part in line[0][1:-1].split()]
            leftScale = [int(part) for part in line[1][1:-1].split()]
            if any(item in leftScale for item in rightScale):
                TAc.print(LANG.render_feedback("error-same-coin", "Scales cannot contain the same coin."), "red", ["bold"])
                exit(0)
            if any(item > coinsNum for item in leftScale):
                TAc.print(LANG.render_feedback("error-coins-out-range", f"You have inserted a coin out of range! The range of coins goes from 0 to {coinsNum}."), "red", ["bold"])
                exit(0)
            weighedList.append([leftScale, rightScale])
    return weighedList


def findEqualWeighs(weighedResults):
    weighedResults.sort(key=lambda e:e['weighed'])
    results = set()
    for i in range(len(weighedResults) - 1):
        if weighedResults[i]['weighed'] == weighedResults[i + 1]['weighed']:
            results.add(weighedResults[i]['coin'])
            results.add(weighedResults[i + 1]['coin'])
    return results
    

def checkStaticStrategy(weighedList, falseCoinIsLeighter, output=True):
    weighedResults = [{'coin': i + 1, 'weighed': []} for i in range(coinsNum)]
    for i in range(len(weighedResults)):
        for leftScale, rightScale in weighedList:
            if falseCoinIsLeighter:
                result = Utilities.makeWeighWithFalseLighter(leftScale, rightScale, weighedResults[i]['coin'])
            else:
                result = Utilities.makeWeighWithFalseHeavier(leftScale, rightScale, weighedResults[i]['coin'])
            weighedResults[i]['weighed'].append(result)
    coinsNotDistinct = findEqualWeighs(weighedResults)
    if len(coinsNotDistinct) == 0 and output:
        TAc.print(LANG.render_feedback("found-false-coin", 'Congratulations! Your strategy finds the false coin.'), "green", ["bold"])
    elif len(coinsNotDistinct) != 0 and output:
        TAc.print(LANG.render_feedback("ambiguos-strategy", f'Your strategy is ambiguous because it doesn\'t distinguish the coins {coinsNotDistinct}.'), "red", ["bold"])
    return coinsNotDistinct


def checkCoinWeightStrategy(weighedList):
    weighedResults = [{'coin': i + 1, 'weighed': []} for i in range(coinsNum)]
    for i in range(len(weighedResults)):
        for leftScale, rightScale in weighedList:
            if (weighedResults[i]['coin'] % 2) == 0:
                result = Utilities.makeWeighWithFalseLighter(leftScale, rightScale, weighedResults[i]['coin'])
            else:
                result = Utilities.makeWeighWithFalseHeavier(leftScale, rightScale, weighedResults[i]['coin'])
            weighedResults[i]['weighed'].append(result)
    coinsNotDistinct = findEqualWeighs(weighedResults)
    return len(coinsNotDistinct) == 0
    

def manageDifferentFalseCoinWeight(weighedList):
    resultCheckWeight = checkCoinWeightStrategy(weighedList)
    coinsNotDistinct = checkStaticStrategy(weighedList, falseCoinIsLeighter=True, output=False)
    resultStrategy = len(coinsNotDistinct) == 0
    if resultCheckWeight and resultStrategy:
        TAc.print(LANG.render_feedback("found-coin-weight", 'Congratulations! Your strategy finds the false coin weight and position.'), "green", ["bold"])
    elif not resultCheckWeight and resultStrategy:
        TAc.print(LANG.render_feedback("not-found-coin-weight", 'Your strategy doesn\'t find if the false coin is lighter or heavier but it would find the position of the false coin if he knew a priori whether it is heavier or lighter.'), "red", ["bold"])
    elif resultCheckWeight and not resultStrategy:
        TAc.print(LANG.render_feedback("not-found-coin-weight", f'Your strategy doesn\'t find the position of the false coin because it doesn\'t distinguish the coins {coinsNotDistinct} however, it manages to find if the false coin is heavier or lighter.'), "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback("not-found-coin-weight", 'Your strategy does not find the position of the false coin or whether it is heavier or lighter.'), "red", ["bold"])



ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

coinsNum = ENV['n']
print("\n")
# print("CoinsNum:", coinsNum)

weighedList = getStaticStrategy(coinsNum)

if ENV['version'] == 'false_is_leighter':
    checkStaticStrategy(weighedList, falseCoinIsLeighter=True)
elif ENV['version'] == 'false_is_heavier':
    checkStaticStrategy(weighedList, falseCoinIsLeighter=False)  
elif ENV['version'] == 'false_has_different_weight':
    manageDifferentFalseCoinWeight(weighedList)
   
exit(0)