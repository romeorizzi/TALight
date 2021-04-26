#!/usr/bin/env python3
from sys import stderr, exit, argv
import re
import random
import time

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
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:

if ENV['seed']=='random_seed': 
    seed_service = random.randrange(sys.maxsize)
else:
    seed_service = int(ENV['seed'])
random.seed(seed_service)
TAc.print(LANG.render_feedback("seed-service",f"# The service is running with seed={seed_service}"), "green")
TAc.print(LANG.render_feedback("explain-protocol","# Each instance gives you a sequence of numbers T and then, on the next row, a sequence of numbers s. You should say whether s is a sub-sequence of T or not (y/n).", "green")

MAX_M_correct = 20 # len_T
MAX_N_correct = 20 # len_s
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
    instances.append((m_instance, n_instance, seed_instance, i%2))

# creo ulteriori istanze per le valutazioni di efficienza:
MAX_M_efficient = 10000 # len_T
MAX_N_efficient =   100 # len_s
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
    instances.append((m_instance, n_instance, seed_instance, i%2))
# crescita geometrica (ora sappiamo che la soluzione è polinomiale):    
scaling_factor = 1.5
m,n,s = instances[-1]
while True:
    m = 1 + int(m * scaling_factor)
    n = 1 + int(n * scaling_factor)
    seed_instance = seed_service + m + n
    if (m > MAX_M_efficient) or (n > MAX_N_efficient):
        break
    instances.append(m, n, seed_instance, random.randint(0,1))


def one_test(m,n,max_val,yes_instance,seed):
    TAc.print(LANG.render_feedback("seed-all-run",f"Check on Instance (m={m},n={n},max_val={max_val},yes_instance={yes_instance},seed {seed}): "), "yellow", ["bold"])
    T,s,seed = gen_subseq_instance(m, n, max_val, yes_instance, seed)
    TAc.print(T, "yellow", ["bold"])
    TAc.print(s, "yellow", ["bold"])
    start = monotonic()
    risp = input(str,num_tokens=1,regex="^(y|n|Y|N|0|1|yes|no|YES|NO|Yes|No)$")
    end = monotonic()
    t = end - start # è un float, in secondi
    if risp[0] in {'y','Y','1'}:
        risp = 1
    else:
        risp = 0
    if risp != yes_instance:
        TAc.print(LANG.render_feedback("not-correct", f'# No. Your solution is NOT correct. The next wff is\n {yes_instance}. Not\n {risp}.'), "red", ["bold"])                        
        exit(0)
    return t   
        
for n_pairs in instances:
    if ENV["sorting_criterion"] == "loves_opening_par":
        first = '('*n_pairs + ')'*n_pairs
        last = '()'*n_pairs
    else:
        first = '()'*n_pairs
        last = '('*n_pairs + ')'*n_pairs
    for i in range(3):
        wff = p.rand_gen(n_pairs, seed=n_pairs*i+ENV["seed"])
        if wff == last:
            wff = first
        time = one_test(wff)
        print(f"#Correct! [took {time} secs on your machine]")
        if time > 1:
            if n_pairs > 13:
                TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. ♥ Your solution correctly computes the well formed formula immidiately following a given one (checked with formulas up to {n_pairs} pairs of parentheses).'), "green")
            TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to compute the next well-formed formula of this last wff with {n_pairs} pairs of parentheses.'), "red", ["bold"])        
            exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. ♥  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. ♥ Your solution is efficient: its running time is polynomial in the length of the formulas it manipulates.'), "green")

exit(0)




#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")
'''
string_T = ""
string_s = ""
length = 10
TAc.print("\nIn this problem you are given a sequence of numbers T. You are asked to evaluate whether a sub-sequence s is part of T "+str(length)+" times. \nAnswer \"y\" if you think s is a subsequence of T, \"n\" otherwise.", "green")
T = generate_random_seq(10, 100)
TAc.print(list_to_string(T[0]), "green")
cert = ENV['cert']

seed = ENV['seed']
n_seed = None

if re.match(r"^[1-9]|[0-9]{2,5}$", seed):
    n_seed = int(seed)

for i in range(0, length):
    x = random.randint(1,10)
    if i == 0 or x % 2 == 0:
        s = get_rand_subseq(T[0], n_seed)
    else:
        s = get_not_subseq(T[0], 100)
    TAc.print(list_to_string(s[0]),"green")

    value, timing  = get_input_with_time()

    if res == "y" or res == "Y": 
        res = True
    elif res =="n" or res == "N":
        res = False
    else: 
        TAc.print("WRONG INPUT FORMAT: only \"y\" or \"n\" are allowed as answer.","red")
        exit(0)
    ret = is_subseq_with_position(s[0],T[0])
    if ret[0] == res:
        TAc.print("OK, your answer is correct!\n","green")
    else:
        TAc.print("NO, your answer isn't correct.\n","red")
        
        if cert:
            if ret[0]:
                print(remove_duplicate_spaces(list_to_string(T[0])))
                print(get_yes_certificate(T[0], ret[1]))
            else:
                if not ret[1]:
                    print("T doesn't contains s")
                else:
                    print("T contains only these elements of s")
                    print(remove_duplicate_spaces(list_to_string(T[0])))
                    print(get_yes_certificate(T[0], ret[1]))
        print("\n")           
                    
'''

cert = ENV['cert']
seed = ENV['seed']

n_seed = None
if re.match(r"^[1-9]|[0-9]{2,5}$", seed):
    n_seed = int(seed)
growth = []
n_instances = 10
T_length = 10
timing = 0
previous = 0
correct = True
seed, seeds = list_of_seed(n_seed, 3 * n_instances)
for i in range(0, n_instances * 3 ,3):
    if not correct:
        break
    T = generate_random_seq(T_length, 100, seeds[i + 1])
    print(" ".join(map(str, T[0])))
    T_length *= 2

    random.seed(seeds[i + 2])
    x = random.randint(1,10)
    if i == 0 or x % 2 == 0:
        s = get_rand_subseq(T[0], i + 3)
    else:
        s = get_not_subseq(T[0], 100, n_seed)
    TAc.print(list_to_string(s[0]),"green")
    if i != 0:
        previous = timing

    res, timing, ok  = get_input_with_time()

    if res == "y" or res == "Y": 
        res = True
    elif res =="n" or res == "N":
        res = False
    else: 
        TAc.print("WRONG INPUT FORMAT: only \"y\" or \"n\" are allowed as answer.","red")
        exit(0)
    ret = is_subseq_with_position(s[0],T[0])
    if ret[0] == res:
        TAc.print("OK, your answer is correct!\n","green")
    else:
        TAc.print("NO, your answer isn't correct.\n","red")
        TAc.print("Seed of this test: " + str(seed))
        
        correct = False
        if cert:
            if ret[0]:
                print(remove_duplicate_spaces(list_to_string(T[0])))
                print(get_yes_certificate(T[0], ret[1]))
            else:
                if not ret[1]:
                    print("T doesn't contains s")
                else:
                    print("T contains only these elements of s")
                    print(remove_duplicate_spaces(list_to_string(T[0])))
                    print(get_yes_certificate(T[0], ret[1]))
        print("\n")
    if i != 0 and ENV['goal'] == 'efficient':        
        growth.append(get_growth_rate(previous,timing))


if ENV['goal'] == 'efficient' and correct:
    linear = True
    for i in growth:
        if i > 2:
            linear = False
    
    if linear == True:
        print("Linear")
    else:
        print("Not linear")
