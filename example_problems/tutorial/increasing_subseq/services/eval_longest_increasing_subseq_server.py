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
    ('YES_cert', bool),
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
        seed_instance = seed_service + m
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
    mdc = min_decreasing_col(T) #trova la colorazione minima decrescente
    n_col = n_coloring(mdc) #trova il numero di colori usati nella colorazione
    start = monotonic() 
    risp = input()
    end = monotonic()
    t = end - start # è un float, in secondi
    correct = True
    if n_col != int(risp):
        TAc.print(f"#NO, it isn't the  maximum increasing subsequence of T. To retry this test use seed: {seed_service}", "red")
        correct = False
        exit(0)

    if ENV['YES_cert'] and correct:    
        start = monotonic()
        #YES_cert = TALinput(int, num_tokens=len(S), regex="^(0|[1-9][0-9]{0,9} *$", TAc=TAc, LANG=LANG)
        YES_cert = input()
        while YES_cert[0] == '#':
            YES_cert = input()
            #YES_cert = TALinput(int, num_tokens=len(S), regex="^(0|[1-9][0-9]{0,9} *$", TAc=TAc, LANG=LANG)
        end = monotonic()
        YES_cert = parse_input(YES_cert)
        t += end - start


        if len(YES_cert) != n_col:
            TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your YES certificate is NOT correct. This isn\'t the longest increasing sequence'), "red", ["bold"])
            TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
            exit(0)
        elif not strictly_increasing(YES_cert):
            TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your YES certificate is NOT correct. The sequence is not increasing'), "red", ["bold"])
            TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
            exit(0)
        
        for i in YES_cert:
            if not i in T:
                TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your YES certificate is NOT correct. The number {i} isn\'t in T'), "red", ["bold"])
                TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
                exit(0)
        TAc.print(LANG.render_feedback("correct-cert", f'# Ok. ♥ Your YES certificate is valid.'), "green")
       
    return t  

count = 0
for instance in instances:
    time = one_test(instance["m"], instance["max_val"], instance["seed"])
    count +=1
    print(f"#Correct! [took {time} seconds on your machine]")
    if time > 2.5:
        if count > NUM_instances_correct:
            TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. ♥ Your solution answers correctly on a first set of instances (with |T|, the length of T, up to {instance["m"]}.'), "green")
        TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to answer on an instance where |T|={instance["m"]}.'), "red", ["bold"])        
        exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. ♥  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥ Your solution is efficient: its running time is linear in the length of T.'), "green")

exit(0)


    