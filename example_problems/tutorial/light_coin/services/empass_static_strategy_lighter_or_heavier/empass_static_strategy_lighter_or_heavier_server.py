#!/usr/bin/env python3
from sys import exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import LightCoinUtilities as Utilities

# METADATA OF THIS TAL_SERVICE:
problem="light_coin"
service="empass_static_strategy_lighter_or_heavier"
args_list = [
    ('lb', int),
    ('lang', str),
    ('ISATTY', bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:
n = ENV['lb'] + 1
while n % 3 != 2:
    n += 1
stopping_command_set="#end"
print(f"# lower bound lb={ENV['lb']}, n={n}")
print(f"# Notice: the n={n} coins are numbered from 1 to {n}.")
print("#? waiting for the list of measures comprising your static strategy.\nPlease, each measure should go on a different line and specify the coins on the left plate, then a comma, then the coins on the tight plate.\nExample:\n   1 3 5, 2 4 6.\nWhen you have finished, insert a closing line '#end' as last line; this will signal us that your input is complete. Any other line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file whose last line is '#end'. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")

def getStaticStrategy():
    weighedList = []
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
            if any(item > n for item in leftScale):
                TAc.print(LANG.render_feedback("error-coins-out-range", f"You have inserted a coin out of range! The range of coin labels goes from 1 to {n}."), "red", ["bold"])
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
    

def checkCoinWeightStrategy(weighedList):
    weighedResults = [{'coin': i + 1, 'weighed': []} for i in range(n)]
    for i in range(len(weighedResults)):
        for leftScale, rightScale in weighedList:
            if (weighedResults[i]['coin'] % 2) == 0:
                result = Utilities.makeWeighWithFalseLighter(leftScale, rightScale, weighedResults[i]['coin'])
            else:
                result = Utilities.makeWeighWithFalseHeavier(leftScale, rightScale, weighedResults[i]['coin'])
            weighedResults[i]['weighed'].append(result)
    coinsNotDistinct = findEqualWeighs(weighedResults)
    if len(coinsNotDistinct) == 0:
        TAc.print(LANG.render_feedback("found-coin-weight", 'Congratulations! Your strategy finds the false coin weight.'), "green", ["bold"])
    else:
        TAc.NO()
        TAc.print(LANG.render_feedback("not-found-coin-weight", f'Your measures do not suffice. Indeed, these measures not distinguish if this coins {coinsNotDistinct} are more heavier or lighter.'), "red", ["bold"])



weighedList = getStaticStrategy()
checkCoinWeightStrategy(weighedList)   
exit(0)
