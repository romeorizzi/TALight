#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="compact_solution"
args_list = [
    ('n',int), 
    ('m',int),
    ('goal',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
from random import randrange
import copy
import pirellone_lib as pl
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 
n=ENV['n'] 
m=ENV['m'] 
   

TAc.print("Instance: ", "yellow", ["bold"])
istanza=pl.random_pirellone(n, m, solvable=True)
pirellone0=copy.deepcopy(istanza)
pirellone1=copy.deepcopy(istanza)
pl.print_pirellone(istanza)


TAc.print("Too long solution: ", "yellow", ["bold"])
shortsol=pl.soluzione(pirellone0,n,m)
longsol=pl.solution_toolong(shortsol,n,m)
pl.stampa_lista(longsol)

TAc.print("Short solution: ", "yellow", ["bold"])
solu=input()
solu=solu.split()


risultato=pl.off_lista_noprint(pirellone1,solu)
if risultato and len(solu)<len(longsol):
    TAc.OK()
    TAc.print("Correct: more compact and all lights are off", "green", ["bold"])
elif risultato and len(solu)==len(longsol):
    TAc.NO()
    TAc.print("Same lenght but all lights are off ", "yellow", ["bold"])
elif risultato and len(solu)>len(longsol):
    TAc.NO()
    TAc.print("NO compact but all lights are off ", "red", ["bold"])
else:
    TAc.NO()
    TAc.print("Some lights are on ", "red", ["bold"])
    
exit(0)
