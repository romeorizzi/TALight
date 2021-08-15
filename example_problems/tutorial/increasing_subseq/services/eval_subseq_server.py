#!/usr/bin/env python3
from sys import stderr, exit
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
    instances.append({
        "m": MAX_M_correct - i%5,      
        "n": MAX_N_correct - i%MAX_N_correct,
        "max_val": max_val,
        "yes": i%2,
        "seed": seed_service + i })    
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
        instances.append({
        "m": i,      
        "n": i//2,
        "max_val": max_val,
        "yes": i%2,
        "seed": seed_service + i + NUM_instances_correct })
    # crescita geometrica (ora sappiamo che la soluzione è polinomiale):    
    scaling_factor = 1.5
    tmp = instances[-1]
    m = tmp["m"]
    n = tmp["n"]
    s = tmp["seed"]
    while True:
        m = 1 + int(m * scaling_factor)
        n = 1 + int(n * scaling_factor)
        if (m > MAX_M_efficient) or (n > MAX_N_efficient):
            break
        instances.append({
        "m": m,      
        "n": n,
        "max_val": max_val,
        "yes": random.randint(0,1),
        "seed": seed_service + m + n })


def one_test(m,n,max_val,yes_instance,seed):
    TAc.print(LANG.render_feedback("seed-all-run",f"#Check on Instance (m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed {seed}): "), "yellow", ["bold"])
    T,S,seed = gen_subseq_instance(m, n, max_val, yes_instance, seed)
    TAc.print(" ".join(map(str,T)), "yellow", ["bold"])
    TAc.print(" ".join(map(str,S)), "yellow", ["bold"])
    start = monotonic()
    risp = TALinput(str,num_tokens=1,regex="^(0|1|y|n|Y|N|yes|no|YES|NO|Yes|No)$", regex_explained="the allowed answers here were: '0','1','y','n','Y','N','yes','no','YES','NO','Yes','No'", TAc=TAc, LANG=LANG)

    end = monotonic()
    t = end - start # è un float, in secondi
    if risp[0][0] in {'1','y','Y'}:
        risp = 1
    else:
        risp = 0 
    if risp != yes_instance:
        TAc.print(LANG.render_feedback("not-correct", f'# No. Your answer is NOT correct.\nThe correct answer is {yes_instance}.\nNot {risp}.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")                        
        exit(0)

    if ENV['cert'] and risp == 1:
        start = monotonic()
        #YES_cert = TALinput(int, num_tokens=len(S), regex="^(0|[1-9][0-9]{0,9} *$", TAc=TAc, LANG=LANG)
        YES_cert = input()
        while YES_cert[0] == '#':
            YES_cert = input()
            #YES_cert = TALinput(int, num_tokens=len(S), regex="^(0|[1-9][0-9]{0,9} *$", TAc=TAc, LANG=LANG)
        end = monotonic()
        YES_cert = parse_input(YES_cert)
        t += end - start


        for i in YES_cert:
            if i < 0 or i > len(T) - 1:
                TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your YES certificate is NOT correct. There are indexes that fall outside the interval [0,|T|-1]'), "red", ["bold"])
                TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
                exit(0) 

        if len(YES_cert) != len(S):
            TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your YES certificate is NOT correct. The sequence of indexes has not length |S|'), "red", ["bold"])
            TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
            exit(0)
        elif not strictly_increasing(YES_cert):
            TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your YES certificate is NOT correct. The sequence of indexes is not increasing'), "red", ["bold"])
            TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
            exit(0)
        
        pos = 0
        for i in YES_cert:
            if T[i] == S[pos]:
                pos += 1

        if pos == len(S):
            TAc.print(LANG.render_feedback("correct-cert", f'# Ok. ♥ Your YES certificate is valid.'), "green")
        else:
            TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your YES certificate is NOT correct. For some i, S[i] <> T[index_i]'), "red", ["bold"])                        
            TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")                        
            exit(0)
    return t   

count = 0
for instance in instances:
    time = one_test(instance["m"], instance["n"], instance["max_val"], instance["yes"], instance["seed"])
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
