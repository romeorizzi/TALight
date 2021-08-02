from sys import stderr, exit, argv

import collections
import random
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="euler_dir"
service="trilly_construction"
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
# crea grafo con cammino euleriano
g, graph, edges , a = GenerateGraph(seed,n,m)
while g.isEulerianWalk() != True:
    g, graph, edges , a = GenerateGraph(seed,n,m)

print("# Construct an Eulerian walk within this graph G that admits at least one.")
print(f"Seed dell'istanza: {a}\n")
print(f"{graph}")

count = 0
print("#? Trilly: waiting for your final answer (write 'walk' and then each arc of the walk in a new line) or a single arc of G.")
prompt = input()

while prompt!= "walk":
    count += 1
    g_new, graph_new, edges_new, a_new = GenerateGraph(seed,n,m)
    head, tail = prompt.split()
    if edges_new.find(prompt) == -1:
        TAc.print(LANG.render_feedback("error-arc", "L'arco non esiste nel grafo."),"red")
        exit(0)
    g_new.rmvEdge(int(head),int(tail))
    if g_new.isEulerianWalk() == False:
        print("Il nuovo grafo non contiene un cammino euleriano.\n")
    else:
        print("walk:")
        g_new.printEulerTour()
        print("\n")
    prompt = input()

for i in range(m):
    prompt = input()
    if edges.find(prompt) == -1:
        print("\nL'arco non esiste nel grafo G.")
        exit(0)
    head, tail = prompt.split()
    if i == 0:
            prec_tail = tail
    if i > 0:
        if head == prec_tail:
            prec_tail = tail
        else:
            TAc.print("\nL'arco che hai inserito non è collegato al precedente, non puoi di certo creare un cammino con questa permutazione\n", "red")
            exit(0)
    edges.replace(prompt, "")

TAc.print(LANG.render_feedback("correct-trilly_con", "Corretto!"),"green")


if ENV["num_calls"] == "at_most_1":
    if count <=1 :
            TAc.print(LANG.render_feedback("ok-1-calls", "Corretto! Hai utilizzato 1 chiamata al servizio trilly."),"green")
    else:
        TAc.print(LANG.render_feedback("no-1-calls", "Corretto! Hai utilizzato però più di 1 chiamata al servizio trilly."),"yellow")
  
if ENV["num_calls"] == "at_most_2":
    if count <=2 :
            TAc.print(LANG.render_feedback("ok-2-calls", "Corretto! Hai utilizzato massimo 2 chiamate al servizio trilly."),"green")
    else:
        TAc.print(LANG.render_feedback("no-2-calls", "Corretto! Hai utilizzato però più di 2 chiamate al servizio trilly."),"yellow")
  
if ENV["num_calls"] == "at_most_n":
    if count <=n :
            TAc.print(LANG.render_feedback("ok-2-calls", f"Corretto! Hai utilizzato massimo {n} chiamate al servizio trilly."),"green")
    else:
        TAc.print(LANG.render_feedback("no-2-calls", f"Corretto! Hai utilizzato però più di {n} chiamate al servizio trilly."),"yellow")
  
if ENV["num_calls"] == "at_most_m":
    if count <=m :
            TAc.print(LANG.render_feedback("ok-2-calls", f"Corretto! Hai utilizzato massimo {m} chiamate al servizio trilly."),"green")
    else:
        TAc.print(LANG.render_feedback("no-2-calls", f"Corretto! Hai utilizzato però più di {m} chiamate al servizio trilly."),"yellow")
  
