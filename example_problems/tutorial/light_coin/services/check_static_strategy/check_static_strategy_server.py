#!/usr/bin/env python3
from sys import exit
import math

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import LightCoinUtilities as Utilities

# METADATA OF THIS TAL_SERVICE:
problem="light_coin"
service="check_static_strategy"
args_list = [
    ('n', int),
    ('version', str),
    ('goal', str),
    ('feedback', str),
    ('lang', str),
    ('META_TTY', bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

stopping_command_set="#end"
print(f"# Notice: the n={ENV['n']} coins are numbered from 1 to {ENV['n']}.")
print("#? waiting for the list of measures comprising your static strategy.\nPlease, each measure should go on a different line and specify the coins on the left plate, then a comma, then the coins on the tight plate.\nExample:\n   1 3 5, 2 4 6.\nWhen you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete. Any other line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file whose last line is '#end'. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")

def getStaticStrategy():
    weighedList = []
    line = [0]
    while line[0] != stopping_command_set:
        line = TALinput(
            str,
            num_tokens=2,
            sep=',',
            exceptions = {stopping_command_set},
            regex=r"^\s*(([1-9][0-9]{0,9}\s+)*[1-9][0-9]{0,9}\s*)$",
            regex_explained="a sequence of numbers from 1 to n, separated by a space. An example of what should go on a plate of the scale (one of the two expected token of the line) is: '2 5 7'.",
            TAc=TAc
        )
        if line[0] != stopping_command_set:
            leftScale = [int(part) for part in line[0].split()]
            rightScale = [int(part) for part in line[1].split()]
            if any(item in leftScale for item in rightScale):
                TAc.print(LANG.render_feedback("error-same-coin", "A same coin can not be placed on both plates of the scale (within a same weighing)."), "red", ["bold"])
                exit(0)
            if any(item > ENV['n'] for item in leftScale) or any(item > ENV['n'] for item in rightScale):
                TAc.print(LANG.render_feedback("error-coins-out-range", f"You have inserted a coin out of range! The range of coin labels goes from 1 to {ENV['n']}."), "red", ["bold"])
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
    weighedResults = [{'coin': i + 1, 'weighed': []} for i in range(ENV['n'])]
    for i in range(len(weighedResults)):
        for leftScale, rightScale in weighedList:
            if falseCoinIsLeighter:
                result = Utilities.makeWeighWithFalseLighter(leftScale, rightScale, weighedResults[i]['coin'])
            else:
                result = Utilities.makeWeighWithFalseHeavier(leftScale, rightScale, weighedResults[i]['coin'])
            weighedResults[i]['weighed'].append(result)
    coinsNotDistinct = findEqualWeighs(weighedResults)
    numberOfScale = len(weighedList)
    feedback = ENV['feedback']
    if len(coinsNotDistinct) == 0 and output:
        if ENV['goal'] == 'optimal':
            optimalNumOfScales = math.ceil(math.log(ENV['n'], 3))
            if numberOfScale > optimalNumOfScales:
                if feedback == 'provide_counterexample':
                    TAc.print(LANG.render_feedback("found-false-coin-not-optimal", 'Your strategy finds the false coin but it\'s not optimal.'), "red", ["bold"])
                else:
                    TAc.print(LANG.render_feedback("found-false-coin-not-optimal-yes-no", 'Your strategy not find the false coin or it\'s not optimal.'), "red", ["bold"])
            else:
                TAc.print(LANG.render_feedback("found-false-coin-optimal", 'Congratulations! Your strategy finds the false coin and it\'s optimal.'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("found-false-coin", 'Congratulations! Your strategy finds the false coin.'), "green", ["bold"])
    elif len(coinsNotDistinct) != 0 and output:
        TAc.NO()
        if feedback == "provide_counterexample":
            TAc.print(LANG.render_feedback("ambiguos-strategy", f'Your strategy is ambiguous because it doesn\'t distinguish the coins {coinsNotDistinct}.'), "red", ["bold"])
        else:
            if ENV['goal'] == 'optimal':
                TAc.print(LANG.render_feedback("found-false-coin-not-optimal-yes-no", 'Your strategy not find the false coin or it\'s not optimal.'), "red", ["bold"])
            else:
                TAc.print(LANG.render_feedback("fail-strategy", 'Your strategy doesn\'t find the false coin.'), "red", ["bold"])
    return coinsNotDistinct


def checkCoinWeightStrategy(weighedList):
    weighedResults = [{'coin': i + 1, 'weighed': []} for i in range(ENV['n'])]
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
    numberOfScale = len(weighedList)
    feedback = ENV['feedback']
    if resultCheckWeight and resultStrategy:
        if ENV['goal'] == 'optimal':
            optimalNumOfScales = math.ceil(math.log((ENV['n'] * 2) + 1, 3))
            if numberOfScale > optimalNumOfScales:
                if feedback == 'provide_counterexample':
                    TAc.print(LANG.render_feedback("found-coin-weight-not-optimal", 'Your strategy finds the false coin weight and position but it\'s not optimal.'), "red", ["bold"])
                else:
                    TAc.print(LANG.render_feedback("found-coin-weight-not-optimal-yes-no", 'Your strategy does not find the position of the false coin or whether it is heavier or lighter or it\'s not optimal.'), "red", ["bold"])
            else:
                TAc.print(LANG.render_feedback("found-coin-weight-optimal", 'Congratulations! Your strategy finds the false coin weight and position and it\'s optimal.'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("found-coin-weight", 'Congratulations! Your strategy finds the false coin weight and position.'), "green", ["bold"])
    elif feedback == "provide_counterexample":
        TAc.NO()
        if not resultCheckWeight and resultStrategy:
            TAc.print(LANG.render_feedback("not-found-coin-weight", 'Your measures do not suffice. Actually, with this set of measures you can not even tell whether the false coin is lighter or heavier than the others. However, if we knew this a priori (whether the false coin is heavier or lighter) then your strategy would always identify the false coin.'), "red", ["bold"])
        elif resultCheckWeight and not resultStrategy:
            TAc.print(LANG.render_feedback("not-found-coin-weight", f'Your measures do not suffice. Indeed, these measures understand if the false coin is heavier or lighter but not which it because it does not distinguish the coins {coinsNotDistinct}.'), "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback("not-found-coin-weight", 'Your strategy does not find the position of the false coin or whether it is heavier or lighter.'), "red", ["bold"])
    else:
        TAc.NO()
        if ENV['goal'] == 'optimal':
            TAc.print(LANG.render_feedback("found-coin-weight-not-optimal-yes-no", 'Your strategy does not find the position of the false coin or whether it is heavier or lighter or it\'s not optimal.'), "red", ["bold"])
        else:  
            TAc.print(LANG.render_feedback("not-found-coin-weight", 'Your strategy does not find the position of the false coin or whether it is heavier or lighter.'), "red", ["bold"])




weighedList = getStaticStrategy()

if ENV['version'] == 'false_is_leighter':
    checkStaticStrategy(weighedList, falseCoinIsLeighter=True)
elif ENV['version'] == 'false_is_heavier':
    checkStaticStrategy(weighedList, falseCoinIsLeighter=False)  
elif ENV['version'] == 'false_has_different_weight':
    manageDifferentFalseCoinWeight(weighedList)
   
exit(0)
