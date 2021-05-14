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
service="eval_longest_increasing_subseq"
args_list = [
    ('seed', str),
    ('yield', str),
    ('feedback_level', int),
    ('goal', str),
    ('code_lang',str),
    ('lang', str),
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
TAc.print(LANG.render_feedback("explain-protocol","# Each instance gives you a sequence of numbers T. You should answer with the length of the longest increasing sub-sequence."), "green")


#                       N                           opt
# correct     | 20 compilato;  15 python, java     | *  |
# quadratic   | 500 compilato; 100 python, java    | *  |
# n_times_opt | 50000 compilato; 2000 python, java | 20 |
# quasi_linar | 100000 compilato; 10000 python, java | *, anche lunghe |
#
# 1 secondo

# come generare n = 100000, opt = 20 (si mette in sequenza o si fà un multi-merge arbitrario di 20 sequenze non-crescenti)


#correct

MAX_M_correct = 20 # len_T



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




#quadratic

# creo ulteriori istanze per le valutazioni di efficienza:
MAX_M_quadratic = 100 # len_T
NUM_instances_quadratic = 20
if ENV["goal"] == "quadratic":
    if ENV["code_lang"]=="compiled":
        MAX_M_quadratic *= 5
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
        if (m > MAX_M_quadratic):
            break
        instances.append({
        "m": m,      
        "max_val": max_val,
        "seed": seed_service + m})


# n_times opt

MAX_M_n_opt = 2000 # len_T
NUM_instances_n_opt = 20
if ENV["goal"] == "n_times_opt":
    if ENV["code_lang"]=="compiled":
        MAX_M_n_opt = 5000
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
        if (m > MAX_M_n_opt):
            break
        instances.append({
        "m": m,      
        "max_val": max_val,
        "seed": seed_service + m})





# quasi linear

MAX_M_log = 10000 # len_T
NUM_instances_log = 20
if ENV["goal"] == "quasi_linear":
    if ENV["code_lang"]=="compiled":
        MAX_M_log *= 10
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
        if (m > MAX_M_log):
            break
        instances.append({
        "m": m,      
        "max_val": max_val,
        "seed": seed_service + m})



def one_test(m,max_val,seed):
    TAc.print(LANG.render_feedback("seed-all-run",f"#Check on Instance (m={m},max_val={max_val},seed {seed}): "), "yellow", ["bold"])
    
    if ENV["goal"] == "n_times_opt":
        T, seed = get_n_log_increasing_instance(m, max_val, seed)
    else:
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

    if ENV['feedback_level'] == 3 and correct:    
        start = monotonic()
        #feedback = TALinput(int, num_tokens=len(S), regex="^(0|[1-9][0-9]{0,9} *$", TAc=TAc, LANG=LANG)
        sequence = input()
        if ENV['yield'] != "only_opt_val" :
            while sequence[0] == '#':
                sequence = input()
            sequence = parse_input(sequence)

        coloring = input()
        if ENV['yield'] == "both_certificate":
            while coloring[0] == '#':
                coloring = input()
            coloring = parse_input(coloring)
                #feedback = TALinput(int, num_tokens=len(S), regex="^(0|[1-9][0-9]{0,9} *$", TAc=TAc, LANG=LANG)
        end = monotonic()
        
        
        t += end - start

        if ENV['yield'] == "a_max_subseq" or ENV['yield'] == "both_certificates": 
            if len(sequence) != n_col:
                TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your YES certificate is NOT correct. This isn\'t the longest increasing sequence'), "red", ["bold"])
                TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
                exit(0)
            elif not strictly_increasing(sequence):
                TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your YES certificate is NOT correct. The sequence is not increasing'), "red", ["bold"])
                TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
                exit(0)
        
            for i in sequence:
                if not i in T:
                    TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your YES certificate is NOT correct. The number {i} isn\'t in T'), "red", ["bold"])
                    TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
                    exit(0)
            TAc.print(LANG.render_feedback("correct-cert", f'# Ok. ♥ Your YES certificate is valid.'), "green")

        if ENV['yield'] == "a_min_col" or ENV['yield'] == "both_certificates": 

            if len(set(coloring)) != n_col:
                TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your coloring is not valid. It is not the minimum decreasing coloring for T'), "red", ["bold"])
                TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
                exit(0)
        
            dec_coloring = [] * len(set(coloring))
            for i in range(0, len(coloring)):
                dec_coloring[coloring[i]-1].append(T[i])

            for i in dec_coloring:
                if strictly_increasing(i):
                    TAc.print(LANG.render_feedback("not-correct-cert", f'# No. Your coloring is not valid'), "red", ["bold"])
                    TAc.print(LANG.render_feedback("to-retry", f'# To retry this very same eval run the service with seed={seed_service}. The description of this very last instance is <m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed={seed}>'), "orange")
                    exit(0)
            TAc.print(LANG.render_feedback("correct-cert", f'# Ok. ♥ Your coloring is valid.'), "green")
            
    return t  

count = 0
for instance in instances:
    time = one_test(instance["m"], instance["max_val"], instance["seed"])
    count +=1
    print(f"#Correct! [took {time} seconds on your machine]")
    if time > 1:
        if count > NUM_instances_correct:
            TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. ♥ Your solution answers correctly on a first set of instances (with |T|, the length of T, up to {instance["m"]}.'), "green")
        TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to answer on an instance where |T|={instance["m"]}.'), "red", ["bold"])        
        exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. ♥  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥ Your solution is efficient: its running time is linear in the length of T.'), "green")

exit(0)


    
