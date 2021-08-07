
# TRILLY CONSTRUCT
# SERVER: grafo con ciclo euleriano
# STUDENT: sceglie un arco
# SERVER: cammino euleriano del grafo tolto l'arco (o no se non esiste)
# STUDENTE: chiama trilly o risponde
# goal: max 2 chiamate, max n, max m

#!/usr/bin/env python3

from sys import stderr, exit

import collections
import random
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="euler_dir"
service="trilly_decision"
args_list = [
    ('num_calls',str),
    ('lang',str),
    ('seed',str),
    ('n',int),
    ('m',int),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:
seed = ENV['seed']
n = ENV['n']
m = ENV['m']
g, graph, edges , a = GenerateGraph(seed,n,m)
print("# Graph G you have to understand whether it admits an eulerian walk.")
print(f"Seed dell'istanza: {a}\n")
print(f"{graph}")

walk = g.isEulerianWalk()
count = 0

print("#? Trilly: waiting for your final answer (y/n) or a single arc of G.")
# NON USO TALINPUT IN QUANTO IL DATO IN INGRESSO NON è DEFINITO (PUò ESSERE UN'ALTRA CHAMATA A TRILLY O LA RISPOSTA!)
prompt = input()
while prompt!= "y" and prompt!= "n":
    count += 1
    head, tail = prompt.split()
    if edges.find(prompt) == -1:
        TAc.print(LANG.render_feedback("error-arc", "L'arco non esiste nel grafo."),"red")
        exit(0)
    g_new, graph_new, edges_new, a_new = GenerateGraph(seed,n,m)
    g_new.rmvEdge(int(head),int(tail))
    if g_new.isEulerianWalk() == True:
        print("Il nuovo grafo ottenuto contiene un cammino euleriano.")
    else: 
        print("Il nuovo grafo ottenuto NON contiene un cammino euleriano.")
    prompt = input()

if ENV["num_calls"] == "any":
    if walk == True and prompt == "y":
        TAc.print(LANG.render_feedback("ok-yes-any-calls", "Corretto!"),"green")
    elif walk == False and prompt == "n":
        TAc.print(LANG.render_feedback("ok-no-any-calls", "Corretto!"),"green")
    else:
        TAc.print(LANG.render_feedback("error-any-calls", "Sbagliato!"),"red")

if ENV["num_calls"] == "at_most_2":
    if walk == True and prompt == "y":
        if count <=2 :
            TAc.print(LANG.render_feedback("ok-yes-2-calls", "Corretto! Hai utilizzato massimo 2 chiamate al servizio trilly."),"green")
        else:
            TAc.print(LANG.render_feedback("no-yes-2-calls", "Corretto! Hai utilizzato però più di 2 chiamate al servizio trilly."),"yellow")
    elif walk == False and prompt == "n":
        if count <=2 :
            TAc.print(LANG.render_feedback("ok-no-2-calls", "Corretto! Hai utilizzato massimo 2 chiamate al servizio trilly."),"green")
        else:
            TAc.print(LANG.render_feedback("no-no-2-calls", "Corretto! Hai utilizzato però più di 2 chiamate al servizio trilly."),"yellow")
    else:
        TAc.print(LANG.render_feedback("error-2-calls", "Sbagliato!"),"red")   

if ENV["num_calls"] == "at_most_n":
    if walk == True and prompt == "y":
        if count <=n :
            TAc.print(LANG.render_feedback("ok-yes-n-calls", f"Corretto! Hai utilizzato massimo {n} chiamate al servizio trilly."),"green")
        else:
            TAc.print(LANG.render_feedback("no-yes-n-calls", f"Corretto! Hai utilizzato però più di {n} chiamate al servizio trilly."),"yellow")
    elif walk == False and prompt == "n":
        if count <=n :
            TAc.print(LANG.render_feedback("ok-no-n-calls", f"Corretto! Hai utilizzato massimo {n} chiamate al servizio trilly."),"green")
        else:
            TAc.print(LANG.render_feedback("no-no-n-calls", f"Corretto! Hai utilizzato però più di {n} chiamate al servizio trilly."),"yellow")
    else:
        TAc.print(LANG.render_feedback("error-n-calls", "Sbagliato!"),"red") 

if ENV["num_calls"] == "at_most_m":
    if walk == True and prompt == "y":
        if count <=m :
            TAc.print(LANG.render_feedback("ok-yes-m-calls", f"Corretto! Hai utilizzato massimo {m} chiamate al servizio trilly."),"green")
        else:
            TAc.print(LANG.render_feedback("no-yes-m-calls", f"Corretto! Hai utilizzato però più di {m} chiamate al servizio trilly."),"yellow")
    elif walk == False and prompt == "n":
        if count <=m :
            TAc.print(LANG.render_feedback("ok-no-m-calls", f"Corretto! Hai utilizzato massimo {m} chiamate al servizio trilly."),"green")
        else:
            TAc.print(LANG.render_feedback("no-no-m-calls", f"Corretto! Hai utilizzato però più di {m} chiamate al servizio trilly."),"yellow")
    else:
        TAc.print(LANG.render_feedback("error-m-calls", "Sbagliato!"),"red") 

    



