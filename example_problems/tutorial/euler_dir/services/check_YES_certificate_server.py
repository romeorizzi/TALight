#!/usr/bin/env python3

from sys import stderr, exit

import collections
import random
from time import monotonic

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="euler-dir"
service="check_YES_certificate"
args_list = [
    ('n',str),
    ('m',str),
    ('goal',str),
    ('feedback',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

if ENV['n'] == 'lazy' and ENV['m'] == 'lazy':
    n,m = input().split()
    n = int(n)
    m = int(m)
  
edges = ""

for i in range(m):
         head, tail = input().split()
         if int(tail)>(n-1) or int(head)>(n-1) :
            TAc.print("\n# ERRORE: hai inserito un arco non può essere presente nel grafo!\n", "red")
            exit(0)
         edges = edges+f"{head} {tail}-"

if input() != '':
    exit(0)
prompt = input()
count = 0
error = ""

while prompt != '':
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


if count != m:
    error = error + "\nIl circuito non riporta il numero corretto di archi."

if circuit_end != circuit_start:
    error = error + "\nIl circuito non termina nel nodo iniziale."

if ENV['feedback'] == "full":
    TAc.print(f"{error}", "yellow")

if ENV['feedback'] == "none":
    if error != "":
        TAc.print("Il certificato non è corretto!","red")


