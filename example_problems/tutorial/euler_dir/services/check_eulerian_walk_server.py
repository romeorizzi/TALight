#!/usr/bin/env python3

from sys import stderr, exit, argv

import collections
import random
from time import monotonic

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="euler_dir"
service="check_eulerian_walk"
args_list = [
    ('walk_type',str),
    ('MAXM',int),
    ('MAXN',int),
    ('feedback',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

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
edges=""
for i in range(m):
     head, tail = TALinput(int, 2, TAc=TAc)
     if tail >= n or head >= n or tail < 0 or head < 0:
        TAc.print(LANG.render_feedback("n-at-least-1", f"# ERRORE: entrambi gli estremi di un arco devono essere nodi del grafo, ossia numeri interi ricompresi nell'intervallo [0,{ENV['MAXN']}."), "red")
        exit(0)
     g.addEdge(int(head),int(tail))
     adj[int(head)].append(int(tail))
     edges = edges+f"{head} {tail}"

print("\n")
prompt = input()
count = 0
error = ""

while prompt!="":
    count += 1
    head, tail = prompt.split()
    if count == 1 :
        circuit_start = head
    circuit_end = tail
    if edges.find(prompt) == -1:
       error = "\nL'arco non esiste nel grafo."
    if count == 1:
        prec_tail = tail
    if count > 1:
        if head == prec_tail:
            prec_tail = tail
        else:
            error = error + "\nL'arco non è collegato al precedente."
    edges.replace(prompt, "")
    prompt = input()

if ENV['walk_type'] == "any":
    answer1 = g.isEulerianCycle()
    #caso: any=closed
    if answer1==True:
        if circuit_end != circuit_start:
            error = error + "\nIl circuito non termina nel nodo iniziale."
    if count != m:
        error = error + "\nIl circuito non riporta il numero corretto di archi."
    #caso: any=open
    if answer1==False:
        if circuit_end == circuit_start:
            error = error + "\nIl circuito non deve terminare nel nodo iniziale."
    if ENV['feedback'] == "full":
        if error != "":
            TAc.print(f"{error}", "yellow")
        else:
            TAc.print("Il certificato è corretto!","green")
    if ENV['feedback'] == "yes_no":
        if error != "":
            TAc.print("Il certificato non è corretto!","red")
        else:
            TAc.print("Il certificato è corretto!","green")

if ENV['walk_type'] == "closed":
    if circuit_end != circuit_start:
        error = error + "\nIl circuito non termina nel nodo iniziale."
    if count != m:
        error = error + "\nIl circuito non riporta il numero corretto di archi."
    if ENV['feedback'] == "full":
        if error != "":
            TAc.print(f"{error}", "yellow")
        else:
            TAc.print("Il certificato è corretto!","green")
    if ENV['feedback'] == "yes_no":
        if error != "":
            TAc.print("Il certificato non è corretto!","red")
        else:
            TAc.print("Il certificato è corretto!","green")

if ENV['walk_type'] == "open":
    if count != m:
        error = error + "\nIl circuito non riporta il numero corretto di archi."
    if circuit_end == circuit_start:
        error = error + "\nIl circuito non deve terminare nel nodo iniziale."
    if ENV['feedback'] == "full":
        if error != "":
            TAc.print(f"{error}", "yellow")
        else:
            TAc.print("Il certificato è corretto!","green")
    if ENV['feedback'] == "yes_no":
        if error != "":
            TAc.print("Il certificato non è corretto!","red")
        else:
            TAc.print("Il certificato è corretto!","green")