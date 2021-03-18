#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="compact_solution"
args_list = [
    ('n',int), 
    ('m',int),
    ('goal',str),
    ('please_do_it_for_me',bool),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
import random 
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
goal=ENV['goal']  
doit=ENV['please_do_it_for_me'] 

TAc.print("Instance: ", "yellow", ["bold"])
istanza=pl.random_pirellone(n, m, solvable=True)
pirellone0=copy.deepcopy(istanza)
pirellone1=copy.deepcopy(istanza)
pirellone2=copy.deepcopy(istanza)
pl.print_pirellone(istanza)


TAc.print("Too long solution: ", "yellow", ["bold"])
shortsol=pl.soluzione(pirellone0,n,m)
longsol=pl.solution_toolong(shortsol,n,m)
pl.stampa_lista(longsol)

TAc.print("Short solution: ", "yellow", ["bold"])
solu=input()
solu=solu.split()

sol_togive=pl.soluzione_min(pirellone2,n,m)
if goal=="m_plus_n":
    g=m+n
elif goal=="m_plus_n_half":
    g=round((m+n)/2)
elif goal=="min":
    g=len(sol_togive)
    

risultato=pl.off_lista_noprint(pirellone1,solu)
if risultato and len(solu)<g:
    TAc.OK()
    TAc.print("Shorter than what you set in goal and all lights are off", "green", ["bold"])
elif risultato and len(solu)==g:
    TAc.OK()
    TAc.print("Same lenght as you set in goal and all lights are off ", "yellow", ["bold"])
elif risultato and len(solu)>g:
    TAc.NO()
    TAc.print("Bigger than what you set in goal but all lights are off  ", "red", ["bold"])
    if doit==1:
        TAc.print("Solution: ", "blue", ["bold"])
        pl.stampa_lista(random.shuffle(sol_togive))
        
else:
    TAc.NO()
    TAc.print("Some lights are on ", "red", ["bold"])
    if doit==1:
        TAc.print("Solution: ", "blue", ["bold"])
        pl.stampa_lista(sol_togive)
    
exit(0)
