#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="compact_solution"
args_list = [
    ('m',int), 
    ('n',int),
    ('goal',str),
    ('seed',str),
    ('level',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
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
level=ENV['level'] 
d=0
if level=="small":
    d=2
if level=="medium":
    d=4
if level=="difficult":
    d=6
    
if ENV['seed']=='random_seed': 
    pirellone,seed,sr,sc=pl.random_pirellone(m, n, solvable=True,s=True)
else:
    pirellone,seed,sr,sc=pl.random_pirellone(m, n,ENV['seed'], solvable=True,s=True)

TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
pl.print_pirellone(pirellone)
TAc.print(LANG.render_feedback("long-sol","Too long solution: "), "yellow", ["bold"])
shortsol=pl.solution_irredundant(pirellone,sr,sc)
longsol=pl.solution_pad(shortsol,m,n,m+n+d,seed)
print(" ".join(longsol))

TAc.print("Short solution: ", "yellow", ["bold"])
solu=input()
solu=solu.split()


if goal=="m_plus_n":
    g=n+m
elif goal=="m_plus_n_half":
    g=round((n+m)/2)
elif goal=="min":
    g=len(shortsol)
    

risultato,_=pl.check_off_lights(pirellone,solu)
if risultato and len(solu)<g:
    TAc.OK()
    TAc.print(LANG.render_feedback("shoter","Shorter than what you set in goal and all lights are off."), "green", ["bold"])
elif risultato and len(solu)==g:
    TAc.OK()
    TAc.print(LANG.render_feedback("same","Same lenght as you set in goal and all lights are off."), "yellow", ["bold"])
elif risultato and len(solu)>g:
    TAc.NO()
    TAc.print(LANG.render_feedback("bigger","Bigger than what you set in goal but all lights are off."), "red", ["bold"])
else:
    TAc.NO()
    TAc.print(LANG.render_feedback("same-on","Some lights are on!"), "red", ["bold"])

    
exit(0)
