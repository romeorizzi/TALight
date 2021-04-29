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
service="eval_longest_subseq"
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
TAc.print(LANG.render_feedback("explain-protocol","# Each instance gives you a sequence of numbers T. You should answer with the length of the longest increasing sub-sequence."), "green")
MAX_M_correct = 20 # len_T
NUM_instances_correct = 20
if ENV["code_lang"]=="compiled":
    MAX_M_correct += 2 
instances = []
# creo i descrittori di istanza per le istanze che è necessario superare per ottenere conferma di correttezza:
for i in range(NUM_instances_correct):
    m_instance = MAX_M_correct - i%5         
    seed_instance = seed_service + i
    instances.append((m_instance, seed_instance))

# creo ulteriori istanze per le valutazioni di efficienza:
MAX_M_efficient = 10000 # len_T
NUM_instances_efficient = 20
if ENV["goal"] == "efficient":
    if ENV["code_lang"]=="compiled":
        MAX_M_efficient *= 20
    # crescita graduale (rischio soluzione esponenziale):
    for i in range(MAX_M_correct+1, 2*MAX_M_correct):
        m_instance = i          
        seed_instance = seed_service + i + NUM_instances_correct
        instances.append((m_instance, seed_instance))
    # crescita geometrica (ora sappiamo che la soluzione è polinomiale):    
    scaling_factor = 1.5
    tmp = instances[-1]
    m = tmp[0]
    s = tmp[1]
    while True:
        m = 1 + int(m * scaling_factor)
        seed_instance = seed_service + m
        if (m > MAX_M_efficient):
            break
        instances.append((m, seed_instance))



def one_test(m,max_val,seed):
    TAc.print(LANG.render_feedback("seed-all-run",f"#Check on Instance (m={m},max_val={max_val},seed {seed}): "), "yellow", ["bold"])
    T,seed = generate_random_seq(m, max_val, seed)
    TAc.print(" ".join(map(str,T)), "yellow", ["bold"])
    mdc = min_decreasing_col(T)
    n_col = n_coloring(mdc)
    start = monotonic()
    
    risp = input()
    end = monotonic()
    t = end - start # è un float, in secondi
    if n_col != int(risp):
        TAc.print("#NO, it isn't the  maximum increasing subsequence of T", "red")
        exit(0)
    return t  

count = 0
for instance in instances:
    time = one_test(instance[0], max_val, instance[1])
    count +=1
    print(f"#Correct! [took {time} seconds on your machine]")
    if time > 2.5:
        if count > NUM_instances_correct:
            TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. ♥ Your solution answers correctly on a first set of instances (with |T|, the length of T, up to {instance[0]}.'), "green")
        TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to answer on an instance where |T|={instance[0]}.'), "red", ["bold"])        
        exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. ♥  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥ Your solution is efficient: its running time is linear in the length of T.'), "green")

exit(0)


    