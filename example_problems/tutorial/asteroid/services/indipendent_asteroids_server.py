#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="asteroid"
service="minimum_laser_server"
args_list = [
    ('level',str),
    ('seed',str),
    ('lang',str),
]

from sys import exit
import asteroid_lib as al



from multilanguage import Env, Lang, TALcolors
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 
if ENV['level']=='easy':
    q=5
if ENV['level']=='medium':
    q=8
if ENV['level']=='difficult':  
    q=11
quad,seed=al.gen_instance(q,ENV['seed'])
TAc.print(LANG.render_feedback("instance", f'Instance (of seed: {seed}):'), "yellow", ["bold"])
al.visualizza(quad)  
TAc.print(LANG.render_feedback("solu", 'Insert your solution: '), "yellow", ["bold"]) 
solu0=input().split(' ')
solu=[]
for i in range(len(solu0)):
    solu.append((int(solu0[i][0]),int(solu0[i][2])))

al.verifica_asteroidi_indipendenti(solu,quad,TAc,LANG)
    
    
exit(0)
