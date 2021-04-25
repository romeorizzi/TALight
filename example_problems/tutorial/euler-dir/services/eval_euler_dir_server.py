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

TAc.print("\nIl seguente grafo è euleriano? Rispondi con Y o N.\n(NB: come per gli altri servizi la prima riga riporta numero nodi e numero archi, a seguire su ogni nuova riga è indicato un arco del grafo).\n","yellow")

num = random.randrange(1,7)
example_graph_eval_euler(num)

start = monotonic()
PS_answer = input()
end = monotonic()
time_yes_no = end - start

if num == 1:
    g = Graph(7)
    g.addEdge(5,6)
    g.addEdge(0,1)
    g.addEdge(3,0)
    g.addEdge(3,1)
    g.addEdge(1,2)
    g.addEdge(2,3)
    g.addEdge(1,4)
    g.addEdge(4,3)

    m = 8
    edges = "5 6-0 1-3 0-3 1-1 2-2 3-1 4-4 3"
    true_answer = g.isEulerianCycle()

if num == 2:
    g = Graph(6)
    g.addEdge(5,5)
    g.addEdge(0,1)
    g.addEdge(1,2)
    g.addEdge(4,1)
    g.addEdge(0,3)
    g.addEdge(3,4)

    m = 6
    edges = "5 5-0 1-1 2-4 1-0 3-3 4"
    true_answer = g.isEulerianCycle()

if num == 3:
    g = Graph(8)
    g.addEdge(6,7)
    g.addEdge(0,1)
    g.addEdge(0,3)
    g.addEdge(1,2)
    g.addEdge(5,1)
    g.addEdge(4,2)
    g.addEdge(4,3)
    g.addEdge(5,3)

    m = 8
    edges = "6 7-0 1-0 3-1 2-5 1-4 2-4 3-5 3"
    true_answer = g.isEulerianCycle()

if num == 4:
    g = Graph(8)
    g.addEdge(7,6)
    g.addEdge(4,5)
    g.addEdge(5,0)
    g.addEdge(2,0)
    g.addEdge(0,6)
    g.addEdge(4,2)
    g.addEdge(6,4)
    g.addEdge(3,4)
    g.addEdge(0,1)
    g.addEdge(1,2)
    g.addEdge(2,3)
    g.addEdge(0,7)

    m = 12
    edges = "7 6-4 5-5 0-2 0-0 6-4 2-6 4-3 4-0 1-1 2-2 3-0 7"
    true_answer = g.isEulerianCycle()

if num == 5:
    g = Graph(6)
    g.addEdge(5,2)
    g.addEdge(4,5)
    g.addEdge(1,0)
    g.addEdge(2,1)
    g.addEdge(3,4)
    g.addEdge(0,3)

    m = 6
    edges = "5 2-4 5-1 0-2 1-3 4-0 3"
    true_answer = g.isEulerianCycle()

if num == 6:
    g = Graph(8)
    g.addEdge(6,7)
    g.addEdge(1,2)
    g.addEdge(7,0)
    g.addEdge(5,6)
    g.addEdge(4,5)
    g.addEdge(3,4)
    g.addEdge(0,1)
    g.addEdge(2,3)

    m = 8
    edges = "6 7-1 2-7 0-5 6-4 5-3 4-0 1-2 3"
    true_answer = g.isEulerianCycle()

if num == 7:
    g = Graph(8)
    g.addEdge(0,1)
    g.addEdge(1,2)
    g.addEdge(2,0)
    g.addEdge(3,2)
    g.addEdge(3,1)
    g.addEdge(3,4)
    g.addEdge(4,3)
    g.addEdge(4,5)
    g.addEdge(5,2)
    g.addEdge(5,6)
    g.addEdge(6,5)
    g.addEdge(7,4)
    g.addEdge(7,6)
    g.addEdge(7,7)

    m = 14
    edges = "0 1-1 2-2 0-3 2-3 1-3 4-4 3-4 5-5 2-5 6-6 5-7 4-7 6-7 7"
    true_answer = g.isEulerianCycle()


if PS_answer == 'Y' or PS_answer == 'y':
    PS_answer = "yes"
if PS_answer == 'N' or PS_answer == 'n':
    PS_answer = "no"
if PS_answer!= 'yes' and PS_answer!='no':
        TAc.print("Input non valido, scrivere Y/y o N/n\n","red")
        exit(0)

if true_answer == True:
    if PS_answer == 'yes':
        TAc.print("CORRETTO, il grafo è euleriano\n","green")
    
    if PS_answer == 'no':
        TAc.print("SBAGLIATO, il grafo è euleriano\n","red")
        exit(0)

    if ENV['goal1'] == 'yes_no' and ENV['goal2'] == 'efficient':
        TAc.print(f"Ci sono voluti {time_yes_no} secs sulla tua macchina!\n","yellow")
        if time_yes_no > 1:
            TAc.print("Il tuo algoritmo non è molto efficiente, ci mette più di un secondo\n","red")
        else:
            TAc.print("Il tuo algoritmo sembra essere efficiente!\n","green")
        exit(0)


if true_answer == False:
    if PS_answer == 'no':
        TAc.print("CORRETTO, il grafo non è euleriano\n","green")

    if PS_answer == 'yes':
        TAc.print("SBAGLIATO, il grafo non è euleriano\n","red")
        exit(0)

    if ENV['goal1'] == 'yes_no' and ENV['goal2'] == 'efficient':
        TAc.print(f"Ci sono voluti {time_yes_no} secs sulla tua macchina!\n","yellow")
        if time_yes_no > 1:
            TAc.print("Il tuo algoritmo non è molto efficiente, ci mette più di un secondo\n","red")
        else:
            TAc.print("Il tuo algoritmo sembra essere efficiente!\n","green")
        exit(0)

    if ENV['goal1'] == 'with_yes_certificate' and ENV['goal2'] == 'efficient':
        TAc.print(f"Ci sono voluti {time_yes_no} secs sulla tua macchina!\n","yellow")
        if time_yes_no > 1:
            TAc.print("Il tuo algoritmo complessivamente non è molto efficiente, ci mette più di un secondo\n","red")
        else:
            TAc.print("Il tuo algoritmo complessivamente sembra essere efficiente!\n","green")
        exit(0)



if ENV['goal1'] == 'with_yes_certificate':
    count = 0
    PS_circuit = []

    TAc.print("\nStampa il certificato (la permutazione di archi costituisce il circuito euleriano, ogni arco su una nuova riga).\nInserisci su una nuova riga '#' quando hai terminato gli archi del circuito.\n", "yellow")
    start2 = monotonic()
    for i in range(m):
        prompt = input()

        if prompt == '#':
            if i < m:
               TAc.print("\nLa permutazione hai inserito non rispetta il numero degli archi del grafo fornito\n", "red")
               exit(0)

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
    time_with_certificate = time_yes_no + (end2 - start2)
    
    TAc.print("\nCertificato corretto.\n", "green")

    if ENV['goal1'] == 'with_yes_certificate' and ENV['goal2'] == 'efficient':
            TAc.print(f"Ci sono voluti {time_yes_no} secs sulla tua macchina!\n","yellow")
            if time_yes_no > 1:
                TAc.print("Il tuo algoritmo complessivamente non è molto efficiente, ci mette più di un secondo\n","red")
            else:
                TAc.print("Il tuo algoritmo complessivamente sembra essere efficiente!\n","green")

exit(0)
