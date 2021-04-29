#!/usr/bin/env python3
from sys import stderr, exit, argv
import re
import random
import time
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import *
# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="eval_subseq_server"
args_list = [
    ('seed',str),
    ('goal',str),
    ('code_lang',str),
    ('cert', bool),
    ('lang',str),
    ('ISATTY',bool),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:
max_val = 100
if ENV['seed']=='random_seed': 
    seed_service = random.randint(100000,999999)
else:
    seed_service = int(ENV['seed'])
random.seed(seed_service)
TAc.print(LANG.render_feedback("seed-service",f"# The service is running with seed={seed_service}"), "green")
TAc.print(LANG.render_feedback("explain-protocol","# Each instance gives you a sequence of numbers T and then, on the next row, a sequence of numbers S. You should say whether S is a sub-sequence of T or not (1/0)."), "green")
MAX_M_correct = 20 # len_T
MAX_N_correct = 20 # len_S
NUM_instances_correct = 20
if ENV["code_lang"]=="compiled":
    MAX_M_correct += 2
    MAX_N_correct += 2    
instances = []
# creo i descrittori di istanza per le istanze che è necessario superare per ottenere conferma di correttezza:
for i in range(NUM_instances_correct):
    m_instance = MAX_M_correct - i%5      
    n_instance = MAX_N_correct - i%MAX_N_correct      
    seed_instance = seed_service + i
    yes = i%2

    instances.append((m_instance, n_instance, seed_instance, yes))

# creo ulteriori istanze per le valutazioni di efficienza:
MAX_M_efficient = 10000 # len_T
MAX_N_efficient =   100 # len_S
NUM_instances_efficient = 20
if ENV["goal"] == "efficient":
    if ENV["code_lang"]=="compiled":
        MAX_M_efficient *= 20
        MAX_N_efficient *= 20
    # crescita graduale (rischio soluzione esponenziale):
    for i in range(MAX_M_correct+1, 2*MAX_M_correct):
        m_instance = i      
        n_instance = i // 2      
        seed_instance = seed_service + i + NUM_instances_correct
        yes = i%2
        instances.append((m_instance, n_instance, seed_instance, yes))
    # crescita geometrica (ora sappiamo che la soluzione è polinomiale):    
    scaling_factor = 1.5
    tmp = instances[-1]
    m = tmp[0]
    n = tmp[1]
    s = tmp[2]
    while True:
        m = 1 + int(m * scaling_factor)
        n = 1 + int(n * scaling_factor)
        seed_instance = seed_service + m + n
        if (m > MAX_M_efficient) or (n > MAX_N_efficient):
            break
        instances.append((m, n, seed_instance, random.randint(0,1)))


def one_test(m,n,max_val,seed,yes_instance):
    TAc.print(LANG.render_feedback("seed-all-run",f"#Check on Instance (m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed {seed}): "), "yellow", ["bold"])
    T,S,seed = gen_subseq_instance(m, n, max_val, yes_instance, seed)
    TAc.print(" ".join(map(str,T)), "yellow", ["bold"])
    TAc.print(" ".join(map(str,S)), "yellow", ["bold"])
    start = monotonic()
    #risp = input(str,num_tokens=1,regex="^(0|1|y|n|Y|N|yes|no|YES|NO|Yes|No)$")
    risp = input()
    end = monotonic()
    t = end - start # è un float, in secondi
    if risp[0] in {'1','y','Y'}:
        risp = 1
    elif risp[0] in {'0','n','N'}:
        risp = 0 
    else:
        TAc.print(LANG.render_feedback("not-recognized-answer", f'# Sorry, you answered with "{risp[0]}" which is not an allowed answer (allowed: 0,1,y,n,Y,N,yes,no,YES,NO,Yes,No).'), "red", ["bold"])                        
        exit(0)
    if risp != yes_instance:
        TAc.print(LANG.render_feedback("not-correct", f'# No. Your solution is NOT correct.\nThe correct solution is {yes_instance}.\nNot {risp}.'), "red", ["bold"])                        
        exit(0)
    return t   
    
count = 0
for instance in instances:
    time = one_test(instance[0], instance[1], max_val, instance[2], instance[3])
    count +=1
    print(f"#Correct! [took {time} seconds on your machine]")
    if time > 1:
        if count > NUM_instances_correct:
            TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. ♥ Your solution answers correctly on a first set of instances (with |T|, the length of T, up to {instance[0]}.'), "green")
        TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to answer on an instance where |T|={instance[0]} and |S|={instance[1]}.'), "red", ["bold"])        
        exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. ♥  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥ Your solution is efficient: its running time is linear in the length of T and S.'), "green")

exit(0)
