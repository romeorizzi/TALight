#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="trilly"
args_list = [
    ('size',str),
    ('num_calls',int),
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
if ENV['size']=='small':
    m=3
    n=3
if ENV['size']=='medium':
    m=5
    n=5
if ENV['size']=='large':
    m=8
    n=8
if ENV['size']=='huge':
    m=12
    n=12
if ENV['size']=='unbearable':
    m=15
    n=15
    
pirellone,seed=pl.random_pirellone(m, n, solvable=True)
empty=[[0 for j in range(0,len(pirellone[0]))] for i in range(0,len(pirellone))]
TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
pl.print_pirellone(pirellone)
for _ in range(ENV['num_calls']):
    TAc.print(LANG.render_feedback("step","Step: "), "yellow", ["bold"])
    pl.soluzione_min_step(pirellone,m,n)
    if empty==pirellone:      
        TAc.print(LANG.render_feedback("end","Finished "), "green", ["bold"])
        exit(0)
exit(0)