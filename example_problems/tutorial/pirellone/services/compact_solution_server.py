#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="compact_solution"
args_list = [
    ('m',int), 
    ('n',int),
    ('goal',str),
    ('seed',str),
    ('please_do_it_for_me',bool),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
import random 
import copy
import pirellone_lib as pl
from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 
m=ENV['m'] 
n=ENV['n'] 
goal=ENV['goal']  
doit=ENV['please_do_it_for_me'] 
s=ENV['seed']

if ENV['seed']=='any': 
    istanza,seed=pl.random_pirellone(m, n, solvable=True)
    TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
    pirellone0=copy.deepcopy(istanza)
    pirellone1=copy.deepcopy(istanza)
    pirellone2=copy.deepcopy(istanza)
    pl.print_pirellone(istanza)
    
    
    TAc.print(LANG.render_feedback("long-sol","Too long solution: "), "yellow", ["bold"])
    shortsol=pl.soluzione(pirellone0,m,n)
    longsol,_=pl.solution_toolong(shortsol,m,n)
    pl.stampa_lista(longsol) 
else:
    istanza,seed=pl.random_pirellone(m, n,s, solvable=True)
    TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
    pirellone0=copy.deepcopy(istanza)
    pirellone1=copy.deepcopy(istanza)
    pirellone2=copy.deepcopy(istanza)
    pl.print_pirellone(istanza)
    
    
    TAc.print(LANG.render_feedback("long-sol","Too long solution: "), "yellow", ["bold"])
    shortsol=pl.soluzione(pirellone0,m,n)
    longsol,_=pl.solution_toolong(shortsol,m,n,s)
    pl.stampa_lista(longsol)

TAc.print("Short solution: ", "yellow", ["bold"])
solu=input()
solu=solu.split()

sol_togive=pl.soluzione_min(pirellone2,m,n)
if goal=="m_plus_n":
    g=n+m
elif goal=="m_plus_n_half":
    g=round((n+m)/2)
elif goal=="min":
    g=len(sol_togive)
    

risultato=pl.off_lista_noprint(pirellone1,solu)
if risultato and len(solu)<g:
    TAc.OK()
    TAc.print(LANG.render_feedback("shoter","Shorter than what you set in goal and all lights are off."), "green", ["bold"])
elif risultato and len(solu)==g:
    TAc.OK()
    TAc.print(LANG.render_feedback("same","Same lenght as you set in goal and all lights are off."), "yellow", ["bold"])
elif risultato and len(solu)>g:
    TAc.NO()
    TAc.print(LANG.render_feedback("bigger","Bigger than what you set in goal but all lights are off."), "red", ["bold"])
    if doit==1:
        TAc.print(LANG.render_feedback("sol","Solution: "), "blue", ["bold"])
        pl.stampa_lista(random.shuffle(sol_togive))
        
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("same-on","Some lights are on "), "red", ["bold"])
    if doit==1:
        TAc.print(LANG.render_feedback("sol","Solution: "), "blue", ["bold"])
        pl.stampa_lista(sol_togive)
    
exit(0)
