#!/usr/bin/env python3
from sys import stderr, exit, argv
import re
import random
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import *
# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="eval_count_increasing_subseq"
args_list = [
    ('seed', str),
    ('lang', str),
    ('goal', str),
    ('code_lang',str),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

max_val = 100
if ENV['seed']=='random_seed': 
    seed_service = random.randint(100000,999999)
else:
    seed_service = int(ENV['seed'])
random.seed(seed_service)

TAc.print(LANG.render_feedback("seed-service",f"# The service is running with seed={seed_service}"), "green")
TAc.print(LANG.render_feedback("explain-protocol","# Each instance gives you a sequence of numbers T. You should answer with the number of the increasing sub-sequences."), "green")
MAX_M_correct = 20 # len_T
NUM_instances_correct = 20
if ENV["code_lang"]=="compiled":
    MAX_M_correct += 2 
instances = []
# creo i descrittori di istanza per le istanze che è necessario superare per ottenere conferma di correttezza:
for i in range(NUM_instances_correct):
    instances.append({
        "m": MAX_M_correct - i%5,      
        "max_val": max_val,
        "seed": seed_service + i }) 

# creo ulteriori istanze per le valutazioni di efficienza:
MAX_M_efficient = 10000 # len_T
NUM_instances_efficient = 20
if ENV["goal"] == "efficient":
    if ENV["code_lang"]=="compiled":
        MAX_M_efficient *= 20
    # crescita graduale (rischio soluzione esponenziale):
    for i in range(MAX_M_correct+1, 2*MAX_M_correct):
        instances.append({
           "m": i,      
           "max_val": max_val,
           "seed": seed_service + i + NUM_instances_correct })
    # crescita geometrica (ora sappiamo che la soluzione è polinomiale):    
    scaling_factor = 1.5
    tmp = instances[-1]
    m = tmp["m"]
    s = tmp["seed"]
    while True:
        m = 1 + int(m * scaling_factor)
        if (m > MAX_M_efficient):
            break
        instances.append({
        "m": m,      
        "max_val": max_val,
        "seed": seed_service + m})



def one_test(m,max_val,seed):
    TAc.print(LANG.render_feedback("seed-all-run",f"#Check on Instance (m={m},max_val={max_val},seed {seed}): "), "yellow", ["bold"])
    T,seed = generate_random_seq(m, max_val, seed)
    TAc.print(" ".join(map(str,T)), "yellow", ["bold"])
    num_increasing_subseq = count_increasing_sub(T,m, max_val)
    start = monotonic()
    risp = input()
    end = monotonic()
    t = end - start # è un float, in secondi
    if num_increasing_subseq != int(risp):
        TAc.print(f"#NO, it isn't the number of increasing subsequences of T. The correct number is {num_increasing_subseq}. To retry this test use seed: {seed_service}", "red")
        exit(0)
    return t  

count = 0
for instance in instances:
    time = one_test(instance["m"], instance["max_val"], instance["seed"])
    count +=1
    print(f"#Correct! [took {time} seconds on your machine]")
    if time > 10:
        if count > NUM_instances_correct:
            TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. ♥ Your solution answers correctly on a first set of instances (with |T|, the length of T, up to {instance["m"]}.'), "green")
        TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to answer on an instance where |T|={instance["m"]}.'), "red", ["bold"])        
        exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. ♥  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥ Your solution is efficient: its running time is linear in the length of T.'), "green")

exit(0)
