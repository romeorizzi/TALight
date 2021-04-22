#!/usr/bin/env python3

# "This service will check your statement that a directed graph you provide us is Eulerian"

from sys import stderr, exit, argv

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from euler_dir_lib import *

# aggiorna meta.yaml
# METADATA OF THIS TAL_SERVICE:
problem="euler-dir"
service="eval_find_scc"
args_list = [
    ('graph',str),
    ('goal',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

if ENV['graph'] == '1':  
    TAc.print("\n# Graph 1:","yellow")
    example_graph(1)
    TAc.print("\n# Inserisci le componenti fortemente connesse che hai calcolato, in ordine crescente e in un formato come abc ef gh : \n","yellow")
    sin = input()
    scheck = scc(1)
    if check_scc(scheck,sin):
        TAc.print("\n ESATTO! \nAdesso, che hai calcolato le corrette componeti fortemente connesse per il grafo fornito, prova a stabilire se e' euleriano o meno (Y/N):\n","yellow")
        eulin = input()
        eulup = eulin.upper()
        if eulup == check_is_eul(1):
            TAc.print("\n ESATTO!","yellow")
        else:
            TAc.print("\n SBAGLIATO! Gioca un altro po' con noi!","yellow")
    else:
        TAc.print("\nLe corrette componenti fortemente connesse sono : "+scc(1),"yellow")

if ENV['graph'] == '2':  
    TAc.print("\n# Graph 2:","yellow")
    example_graph(2)
    TAc.print("\n# Inserisci le componenti fortemente connesse che hai calcolato, in ordine crescente e in un formato come abc ef gh : \n","yellow")
    sin = input()
    scheck = scc(2)
    if check_scc(scheck,sin):
        TAc.print("\n ESATTO! \nAdesso, che hai calcolato le corrette componeti fortemente connesse per il grafo fornito, prova a stabilire se e' euleriano o meno (Y/N):\n","yellow")
        eulin = input()
        eulup = eulin.upper()
        if eulup == check_is_eul(2):
            TAc.print("\n ESATTO!","yellow")
        else:
            TAc.print("\n SBAGLIATO! Gioca un altro po' con noi!","yellow")
    else:
        TAc.print("\nLe corrette componenti fortemente connesse sono : "+scc(2),"yellow")

if ENV['graph'] == '3':  
    TAc.print("\n# Graph 3:","yellow")
    example_graph(3)
    TAc.print("\n# Inserisci le componenti fortemente connesse che hai calcolato, in ordine crescente e in un formato come abc ef gh : \n","yellow")
    sin = input()
    scheck = scc(3)
    if check_scc(scheck,sin):
        TAc.print("\nESATTO! \nAdesso, che hai calcolato le corrette componeti fortemente connesse per il grafo fornito, prova a stabilire se e' euleriano o meno (Y/N):\n","yellow")
        eulin = input()
        eulup = eulin.upper()
        if eulup == check_is_eul(3):
            TAc.print("\n ESATTO!","yellow")
        else:
            TAc.print("\n SBAGLIATO! Gioca un altro po' con noi!","yellow")  
    else:
        TAc.print("\nLe corrette componenti fortemente connesse sono : "+scc(3),"yellow")

if ENV['graph'] == '4':  
    TAc.print("\n# Graph 4:","yellow")
    example_graph(4)
    TAc.print("\n# Inserisci le componenti fortemente connesse che hai calcolato, in ordine crescente e in In un formato come abc ef gh : \n","yellow")
    sin = input()
    scheck = scc(4)
    if check_scc(scheck,sin):
        TAc.print("\n ESATTO! \nAdesso, che hai calcolato le corrette componeti fortemente connesse per il grafo fornito, prova a stabilire se e' euleriano o meno (Y/N):\n","yellow")
        eulin = input()
        eulup = eulin.upper()
        if eulup == check_is_eul(4):
            TAc.print("\n ESATTO!","yellow")
        else:
            TAc.print("\n SBAGLIATO Gioca un altro po' con noi!!","yellow")
    else:
        TAc.print("\nLe corrette componenti fortemente connesse sono : "+scc(4),"yellow")

if ENV['graph'] == '5':  
    TAc.print("\n# Graph 5:","yellow")
    example_graph(5)
    TAc.print("\n# Inserisci le componenti fortemente connesse che hai calcolato, in ordine crescente e in un formato come abc ef gh : \n","yellow")
    sin = input()
    scheck = scc(5)
    if check_scc(scheck,sin):
        TAc.print("\n ESATTO! \nAdesso, che hai calcolato le corrette componeti fortemente connesse per il grafo fornito, prova a stabilire se e' euleriano o meno (Y/N):\n","yellow")
        eulin = input()
        eulup = eulin.upper()
        if eulup == check_is_eul(5):
            TAc.print("\n ESATTO!","yellow")
        else:
            TAc.print("\n SBAGLIATO! Gioca un altro po' con noi!","yellow")
    else:
        TAc.print("\nLe corrette componenti fortemente connesse sono : "+scc(5),"yellow")

if ENV['graph'] == '6':  
    TAc.print("\n# Graph 6:","yellow")
    example_graph(6)
    TAc.print("\n# Inserisci le componenti fortemente connesse che hai calcolato, in ordine crescente e in un formato come abc ef gh : \n","yellow")
    sin = input()
    scheck = scc(6)
    if check_scc(scheck,sin):
        TAc.print("\n ESATTO! \nAdesso, che hai calcolato le corrette componeti fortemente connesse per il grafo fornito, prova a stabilire se e' euleriano o meno (Y/N):\n","yellow")
        eulin = input()
        eulup = eulin.upper()
        if eulup == check_is_eul(6):
            TAc.print("\n ESATTO!","yellow")
        else:
            TAc.print("\n SBAGLIATO! Gioca un altro po' con noi!","yellow")
    else:
        TAc.print("\nLe corrette componenti fortemente connesse sono : "+scc(6),"yellow")

if ENV['graph'] == '7':  
    TAc.print("\n# Graph 7:","yellow")
    example_graph(7)
    TAc.print("\n# Inserisci le componenti fortemente connesse che hai calcolato, in ordine crescente e in un formato come abc ef gh : \n","yellow")
    sin = input()
    scheck = scc(7)
    if check_scc(scheck,sin):
        TAc.print("\n ESATTO! \nAdesso, che hai calcolato le corrette componeti fortemente connesse per il grafo fornito, prova a stabilire se e' euleriano o meno (Y/N):\n","yellow")
        eulin = input()
        eulup = eulin.upper()
        if eulup == check_is_eul(7):
            TAc.print("\n ESATTO!","yellow")
        else:
            TAc.print("\n SBAGLIATO! Gioca un altro po' con noi!","yellow")
    else:
        TAc.print("\nLe corrette componenti fortemente connesse sono : "+scc(7),"yellow")
