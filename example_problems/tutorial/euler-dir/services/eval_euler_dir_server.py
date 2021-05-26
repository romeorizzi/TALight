#!/usr/bin/env python3

# This service will check if given a directed graph, you can decide whether it is Eulerian? And can you do it efficiently?

from sys import stderr, exit, argv

import collections
import random
from time import monotonic

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="euler-dir"
service="eval_euler_dir"
args_list = [
    ('goal1',str),
    ('goal2',str),
    ('code_lang',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

g, graph, edges , m = GenerateGraph()
true_answer = g.isEulerianCycle()

TAc.print(f"{graph}", "yellow")

if true_answer == False:
    start = monotonic()
    PS_answer = input()
    end = monotonic()
    time1 = end - start

    if PS_answer == 'Y' or PS_answer == 'y':
        PS_answer = "yes"
    if PS_answer == 'N' or PS_answer == 'n':
        PS_answer = "no"
    if PS_answer!= 'yes' and PS_answer!='no':
        TAc.print("Input non valido, scrivere Y/y o N/n\n","red")
        exit(0)

    if PS_answer == 'yes':
        TAc.print("\nSBAGLIATO, il grafo non è euleriano\n","red")
        exit(0)
    if ENV['goal1'] == 'yes_no' and ENV['goal2'] == 'correct':
        TAc.print(f"\nRISPOSTA CORRETTA!\n", "green")
    if ENV['goal1'] == 'yes_no' and ENV['goal2'] == 'efficient':
        TAc.print(f"\nCORRETTO!\nCi sono voluti {time1} secs sulla tua macchina!\n","yellow")
        if time1 > 1:
            TAc.print("Il tuo algoritmo non è molto efficiente, ci mette più di un secondo\n","red")
        else:
            TAc.print("Il tuo algoritmo sembra essere efficiente!\n","green")
        exit(0)  
    if ENV['goal1'] == 'with_yes_certificate' and ENV['goal2'] == 'efficient':
        TAc.print(f"CORRETTO!\nCi sono voluti {time1} secs sulla tua macchina!\n","yellow")
        if time1 > 1:
            TAc.print("Il tuo algoritmo complessivamente non è molto efficiente, ci mette più di un secondo\n","red")
        else:
            TAc.print("Il tuo algoritmo complessivamente sembra essere efficiente!\n","green")
        exit(0) 


if true_answer == True:
    start = monotonic()
    PS_answer = input()
    end1 = monotonic()
    if PS_answer == 'Y' or PS_answer == 'y':
        PS_answer = "yes"
    if PS_answer == 'N' or PS_answer == 'n':
        PS_answer = "no"
    if PS_answer!= 'yes' and PS_answer!='no':
        TAc.print("Input non valido, scrivere Y/y o N/n\n","red")
        exit(0)
    if PS_answer == 'no':
        TAc.print("\nSBAGLIATO, il grafo è euleriano\n","red")
        exit(0)    

    for i in range(m):
        prompt = input()
        head, tail = prompt.split()
        if edges.find(prompt) == -1:
            TAc.print("\nL'arco non esiste nel grafo.\n","red")
            exit(0)
        if i == 1:
            prec_tail = tail
        if i > 1:
            if head == prec_tail:
                prec_tail = tail
            else:
                TAc.print("\nL'arco che hai inserito non è collegato al precedente, non puoi di certo creare un circuito con questa permutazione\n", "red")
                exit(0)
    end2 = monotonic()
    time2 = end2 - start
    time1 = end1 - start

    if ENV['goal1'] == 'yes_no' and ENV['goal2'] == 'correct':
        TAc.print(f"\nRISPOSTA CORRETTA!\n","green")
    if ENV['goal1'] == 'yes_no' and ENV['goal2'] == 'efficient':
        TAc.print(f"\nCORRETTO!\nCi sono voluti {time1} secs sulla tua macchina!\n","yellow")
        if time1 > 1:
            TAc.print("Il tuo algoritmo non è molto efficiente, ci mette più di un secondo\n","red")
        else:
            TAc.print("Il tuo algoritmo sembra essere efficiente!\n","green")
        exit(0)
    if ENV['goal1'] == 'with_yes_certificate' and ENV['goal2'] == 'efficient':
            TAc.print(f"\nCORRETTO!\nCi sono voluti {time2} secs sulla tua macchina!\n","yellow")
            if time2 > 1:
                TAc.print("Il tuo algoritmo complessivamente non è molto efficiente, ci mette più di un secondo\n","red")
            else:
                TAc.print("Il tuo algoritmo complessivamente sembra essere efficiente!\n","green")

exit(0)

 