#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('size',str),
    ('num_calls',int),
]

from sys import stderr, exit
import pirellone_lib as pl
from multilanguage import Env, Lang, TALcolors
ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
if ENV['size']=='small':
    m=2
    n=2
if ENV['size']=='medium':
    m=4
    n=4
if ENV['size']=='large':
    m=6
    n=6
if ENV['size']=='huge':
    m=8
    n=8
if ENV['size']=='unbearable':
    m=9
    n=9
    
pirellone,seed,sr,sc=pl.random_pirellone(m, n, solvable=True,s=True)
empty=[[0 for j in range(0,len(pirellone[0]))] for i in range(0,len(pirellone))]
TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
pl.print_pirellone(pirellone)
lista=pl.solution_irredundant(pirellone,sr,sc)
i=0
for _ in range(ENV['num_calls']):
    TAc.print(LANG.render_feedback("step","Step: "), "yellow", ["bold"])
    print(lista[i])
    pl.check_off_lights(pirellone,[lista[i]])
    pl.print_pirellone(pirellone)
    i+=1
    if empty==pirellone:      
        TAc.print(LANG.render_feedback("end","Finished "), "green", ["bold"])
        exit(0)
exit(0)