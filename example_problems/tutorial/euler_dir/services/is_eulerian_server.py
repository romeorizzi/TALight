#!/usr/bin/env python3

# "This service will check your statement that a directed graph you provide us admits an eulerian walk (of the specified type)""

from os import EX_TEMPFAIL
from sys import stderr, exit

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="euler_dir"
service="check_is_eulerian"
args_list = [
    ('walk_type',str),
    ('feedback',str),
    ('lang',str),
    ('eulerian',bool),
    ('MAXN',int),
    ('MAXM',int),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

MAXN = ENV['MAXN']
MAXM = ENV['MAXM']

# START CODING YOUR SERVICE:
print(f"#? waiting for your directed graph.\nFormat: each line two numbers separated by space. On the first line the number of nodes (an integer n in the interval [1,{MAXN}]) and the number of arcs (an integer m in the interval [1,{MAXM}]). Then follow m lines, one for each arc, each with two numbers in the interval [0,n). These specify the tail node and the head node of the arc, in this order.\nAny line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself.")
n, m = TALinput(int, 2, TAc=TAc)
if n < 1:
    TAc.print(LANG.render_feedback("n-LB", f"# ERRORE: il numero di nodi del grafo deve essere almeno 1. Invece il primo dei numeri che hai inserito è n={n}."), "red")
    exit(0)
if m < 0:
    TAc.print(LANG.render_feedback("m-LB", f"# ERRORE: il numero di archi del grafo non può essere negativo. Invece il secondo dei numeri che hai inserito è m={m}."), "red")
    exit(0)
if n > MAXN:
    TAc.print(LANG.render_feedback("n-UB", f"# ERRORE: il numero di nodi del grafo non può eccedere {ENV['MAXN']}. Invece il primo dei numeri che hai inserito è n={n}>{ENV['MAXN']}."), "red")
    exit(0)
if m > MAXM:
    TAc.print(LANG.render_feedback("m-UB", f"# ERRORE: il numero di archi del grafo non può eccedere {ENV['MAXM']}. Invece il secondo dei numeri che hai inserito è n={n}>{ENV['MAXM']}."), "red")
    exit(0)
g = Graph(int(n))
    
adj = [ [] for _ in range(n)]

for i in range(m):
     head, tail = TALinput(int, 2, TAc=TAc)
     if tail >= n or head >= n or tail < 0 or head < 0:
        TAc.print(LANG.render_feedback("n-at-least-1", f"# ERRORE: entrambi gli estremi di un arco devono essere nodi del grafo, ossia numeri interi ricompresi nell'intervallo [0,{ENV['MAXN']}."), "red")
        exit(0)
     g.addEdge(int(head),int(tail))
     adj[int(head)].append(int(tail))

eul = ENV['eulerian']

if eul == 1:

    if ENV['walk_type'] == "closed":
        answer1 = g.isEulerianCycle()
        if answer1 == eul:
            TAc.OK()
            if answer1 == True:
                TAc.print(LANG.render_feedback("eulerian", f"Il grafo ammette un eulerian cycle!"),"green")
                if ENV['feedback'] == "with_YES_certificate":
                    TAc.print(LANG.render_feedback("here-is-the-certificate", f"Eccone uno:"),"green")
                    printCircuit(adj)
                    exit(0)
            else:
                TAc.print(LANG.render_feedback("not-eulerian", f"Il grafo NON contiene alcun eulerian cycle!"),"red")
                exit(0)
        else:
            TAc.NO()
            exit(0)

    if ENV['walk_type'] == "open":
        answer1 = g.isEulerianWalk()
        answer2 = g.isEulerianCycle()
        if answer1 == eul and answer2==False and answer1 ==True :
            TAc.OK()
            if answer1 == True:
                TAc.print(LANG.render_feedback("eulerian", f"Il grafo ammette un eulerian walk!"),"green")
                if ENV['feedback'] == "with_YES_certificate":
                    TAc.print(LANG.render_feedback("here-is-the-certificate", f"Eccone uno:"),"green")
                    printCircuit(adj)
                    exit(0)
            else:
                TAc.print(LANG.render_feedback("not-eulerian", f"Il grafo NON contiene alcun eulerian walk!"),"red")
                exit(0)
        else:
            TAc.NO()
            exit(0)

    if ENV['walk_type'] == "any": 
        answer1 = g.isEulerianCycle()
        answer2 = g.isEulerianWalk()
        if answer1 == eul or answer2 == eul:
            TAc.OK()
            if answer1 == eul:
                TAc.print(LANG.render_feedback("eulerian", f"Il grafo ammette un eulerian cycle!"),"green")
                if ENV['feedback'] == "with_YES_certificate":
                    TAc.print(LANG.render_feedback("here-is-the-certificate", f"Eccone uno:"),"green")
                    printCircuit(adj)
                    exit(0) 
            if answer2 == eul:
                TAc.print(LANG.render_feedback("eulerian", f"Il grafo ammette un eulerian walk!"),"green")
                if ENV['feedback'] == "with_YES_certificate":
                    TAc.print(LANG.render_feedback("here-is-the-certificate", f"Eccone uno:"),"green")
                    g.printEulerTour()
                    exit(0)
        else:
            TAc.print(LANG.render_feedback("not-eulerian", f"Il grafo NON contiene alcun eulerian walk/cycle!"),"red")
            exit(0)


if eul == 0:

    if ENV['walk_type'] == "closed":
        answer1 = g.isEulerianCycle()
        if answer1 == eul:
            TAc.OK()
        else:
            TAc.NO()
            if answer1 == True:
                TAc.print(LANG.render_feedback("eulerian", f"Il grafo ammette un eulerian cycle!"),"red")
                if ENV['feedback'] == "with_YES_certificate":
                    TAc.print(LANG.render_feedback("here-is-the-certificate", f"Eccone uno:"),"red")
                    printCircuit(adj)
                    exit(0)
            exit(0)

    if ENV['walk_type'] == "open":
        answer1 = g.isEulerianWalk()
        answer2 = g.isEulerianCycle()
        if answer1 == eul:
            TAc.OK()
        else:
            TAc.NO()
            TAc.print(LANG.render_feedback("eulerian", f"Il grafo ammette un eulerian walk!"),"red")
            if ENV['feedback'] == "with_YES_certificate":
                TAc.print(LANG.render_feedback("here-is-the-certificate", f"Eccone uno:"),"red")
                printCircuit(adj)
                exit(0)
            

    if ENV['walk_type'] == "any": 
        answer1 = g.isEulerianCycle()
        answer2 = g.isEulerianWalk()
        if answer1 == True or answer2 == True:
            TAc.NO()
            if answer1 == True:
                TAc.print(LANG.render_feedback("eulerian", f"Il grafo ammette un eulerian cycle!"),"red")
                if ENV['feedback'] == "with_YES_certificate":
                    TAc.print(LANG.render_feedback("here-is-the-certificate", f"Eccone uno:"),"red")
                    printCircuit(adj)
                    exit(0) 
            if answer2 == True:
                TAc.print(LANG.render_feedback("eulerian", f"Il grafo ammette un eulerian walk!"),"red")
                if ENV['feedback'] == "with_YES_certificate":
                    TAc.print(LANG.render_feedback("here-is-the-certificate", f"Eccone uno:"),"red")
                    g.printEulerTour()
                    exit(0)
        else:
            TAc.OK()
            exit(0)
