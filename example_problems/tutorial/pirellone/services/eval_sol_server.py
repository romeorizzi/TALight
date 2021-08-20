#!/usr/bin/env python3
from sys import exit
import re
import random
from time import monotonic

from multilanguage import Env, Lang, TALcolors

import pirellone_lib as pl

# METADATA OF THIS TAL_SERVICE:
problem="pirellone"
service="eval_sol"
args_list = [
    ('goal',str),
    ('seed',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 

if ENV['seed']=='random_seed': 
    seed_service = random.randint(10000,99999)
else:
    seed_service = int(ENV['seed'])
random.seed(seed_service)
TAc.print(LANG.render_feedback("seed-service",f'# The service is running with seed={seed_service}'), "green")
TAc.print(LANG.render_feedback("explain-protocol",'# The test instances are all 0,1-matrices that can be turned off with the allowed moves. Instances are dealt with subsequently, one at the time, up to termination of the evaluation or first detected fault. For each instance, the service prints only m and n (its number of rows and columns) separated by spaces and then answers your queries about the entries of the matrix. A query is a line beginning with \'?\' followed by a row index (in the interval [1,m]) and a column index (in the interval [1,n]) again separated by spaces. After the needed queries, you should answer with a solution, i.e., a sequence of moves leading to the all zero matrix (example: r1 c3 r5)'), "green")

#                   |   M                                | N  |
# correct           | 10 compilato; 7 python, java       | =M |
# polynomial_in_m   | 50                                 | 10 |
# efficient         | 50 compilato; 50 python, java      | =M |
# sub_linear        | 1000 compilato; 10000 python, java | 1000 compilato; 10000 python, java |
#
# 1 secondo


# definizione delle classi di istanze per il goal selezionato
def one_test(m,n,seed,max_queries=None):
    TAc.print(LANG.render_feedback("seed-all-run",f"#Check on Instance (m={m}, n={n}, solvable=True, seed={seed}): "), "yellow", ["bold"])
    M, seed, switches_row, switches_col = pl.random_pirellone(m, n, seed="random_seed", solvable=True, s=True)
    TAc.print(f"{m} {n}", "yellow", ["bold"])
    num_queries = 0
    start = monotonic()
    while True:
        line = input()
        if line[0] != "?":
            break
        matched = re.match("^(\?\s[1-9][0-9]{0,3}\s[1-9][0-9]{0,3})$", line)
        if not bool(matched):
            TAc.print(LANG.render_feedback("query-line-wrong-format",f'# Error! Your query line ({line}) is not accordant (it does not match the regular expression "^(?\n*[1-9][0-9]{0,3}\n*[1-9][0-9]{0,3})$"'), "red", ["bold"])
            exit(0)
        i,j = map(int, line[1:].split())
        if i > m:
            TAc.print(LANG.render_feedback("query-line-rows-exceeded",f'# Error! In your query line ({line}) the row index ({i}) exceeds the number of rows ({m})'), "red", ["bold"])
            exit(0)
        if j > n:
            TAc.print(LANG.render_feedback("query-line-cols-exceeded",f'# Error! In your query line ({line}) the column index ({j}) exceeds the number of columns ({n})'), "red", ["bold"])
            exit(0)
        TAc.print(M[i-1][j-1], "yellow", ["bold"])    
        #TAc.print((switches_row[i-1] + switches_col[j-1]) % 2, "yellow", ["bold"])
        num_queries += 1 
    line=input()
    end = monotonic()
    t = end - start # è un float, in secondi
    #provo a fare un altro metodo
    line=line.split()
    correction,_=pl.check_off_lights(M,line,LANG, TAc)
    if not correction:
        TAc.print(LANG.render_feedback("wrong",f"# No! Your solution does not turn off all the lights in the {m}x{n} matrix of seed={seed}."), "red", ["bold"])
        print(f"# pirellone spento?{M}")
        print(f"# {line}")
        exit(0)
    if t > 1:
        return False
    return True








def eval_correct():
    for _ in range(5):
        one_test(7,7,seed_service,max_queries=None)
    TAc.print(LANG.render_feedback("correct", '# Your solution meets the goal you set: correct .'), "green",["bold"])    
    return

def eval_polynomial_in_m():
    for _ in range(5):
        if not one_test(29,10,seed_service,max_queries=None):
            TAc.print(LANG.render_feedback("not-polynomial-in-m", '# No. Your solution is not polynomial in m. Run on your machine, it took more than one second to compute the solution.'), "red", ["bold"])   
            exit(0)
    TAc.print(LANG.render_feedback("correct-polynomial-in-m", '# Your solution meets the goal you set: polynomial_in_m .'), "green",["bold"])
    return

def eval_efficient():
    for _ in range(5):
        if not one_test(50,50,seed_service,max_queries=None):
            TAc.print(LANG.render_feedback("not-efficient", '# No. Your solution is efficient. Run on your machine, it took more than one second to compute the solution.'), "red", ["bold"])   
            exit(0)
    TAc.print(LANG.render_feedback("correct-efficient", '# Your solution meets the goal you set: efficient .'), "green",["bold"])
    return

def eval_sub_linear():
    for _ in range(5):
        if not one_test(10000,10000,seed_service,max_queries=None):
            TAc.print(LANG.render_feedback("not-sub_linear", '# No. Your solution is sub linear. Run on your machine, it took more than one second to compute the solution.'), "red", ["bold"])   
            exit(0)
    TAc.print(LANG.render_feedback("correct-sub_linear", '# Your solution meets the goal you set: sub_linear .'), "green",["bold"])
    return

eval_correct()
if ENV['goal'] == "correct":
    exit(0)
eval_polynomial_in_m()
if ENV['goal'] == "polynomial_in_m":
    exit(0)
eval_efficient()
if ENV['goal'] == "efficient":
    exit(0)
eval_sub_linear()

exit(0)











    
"""
    #PARTE CON PROF
    s_rows, s_cols = pl.extract_sol(line, m, n)
    s_rows_comp = [1-x for x in s_rows]
    s_cols_comp = [1-x for x in s_cols]
    
    ok = False
    if s_rows == switches_row:
        if s_cols != switches_col:
            if s_cols_comp == switches_col:
               TAc.print(LANG.render_feedback("wrong-all-1",f"# No! The submitted solution is not correct for the matrix (m={m},n={n},solvable=True,seed={seed}): all the elements in the resultant matrix will be set to 1. Your mission was to bring all them to 0!"), "red", ["bold"])
            else:
               TAc.print(LANG.render_feedback("wrong-first-col",f"# No! The submitted solution of the matrix of seed={seed} is not correct: at least one element of the first column will end up set to 1"), "red", ["bold"])
            exit(0)
    elif s_rows_comp == switches_row:
        if s_cols_comp != switches_col:
            if s_cols == switches_col:
               TAc.print(LANG.render_feedback("wrong-all-1",f"# No! The submitted solution is not correct for the matrix (m={m},n={n},solvable=True,seed={seed}): all the elements in the resultant matrix will be set to 1. Your mission was to bring all them to 0!"), "red", ["bold"])
            else:
               TAc.print(LANG.render_feedback("wrong-first-col",f"# No! The submitted solution of the matrix of seed={seed} is not correct: at least one element of the first column will end up set to 1"), "red", ["bold"])
            exit(0)
    else:
        TAc.print(LANG.render_feedback("wrong-first-row",f"# No! The submitted solution of the matrix of seed={seed} is not correct: at least one element of the first row will end up set to 1"), "red", ["bold"])
        exit(0)
    """
"""
#VECCHIO EVAL_SOL
for i in range(15):
    if ENV['size']=='small':
        m=3
        n=3
    if ENV['size']=='medium':
        m=5
        n=5
    if ENV['size']=='large':
        m=8
        n=8
    pirellone,_,sr,sc=pl.random_pirellone(m, n, solvable=True,s=True)
    print(pirellone)
    sol_togive=pl.solution_irredundant(pirellone,sr,sc)
    a=monotonic()
    sol=input()
    sol_to_ver=[]
    if sol[0] != '#':
        for i in range(len(sol)):
            if sol[i]=='r':
                sol_to_ver.append(f'r{sol[i+1]}')
            if sol[i]=='c':
                sol_to_ver.append(f'c{sol[i+1]}')
    
        b=monotonic() 
        time=b-a
        moff,_=pl.check_off_lights(pirellone,sol_to_ver)
        if not moff:
            TAc.print(LANG.render_feedback("wrong",f"# No! The solution of the matrix of seed={_} is not correct."), "red", ["bold"])
            exit(0)
        if len(sol_to_ver)>len(sol_togive):
            TAc.print(LANG.render_feedback("semi-correct",f"# The solution of the matrix of seed={_} is not minimum."), "yellow", ["bold"])
        if time > 1:
            TAc.print(LANG.render_feedback("not-efficient", '# No. Your solution is not efficient. Run on your machine, it took more than one second to compute the solution.'), "red", ["bold"])        
            exit(0)
        else:
            TAc.print(LANG.render_feedback("efficient", '# ♥ Ok. Your solution is efficient.'), "green")
            if len(sol_to_ver)==len(sol_togive):
                TAc.print(LANG.render_feedback("correct", '# ♥ Your solution is the best one.'), "green",["bold"])
        sol_to_ver.clear()
        sol=''
        pirellone.clear()
    
exit(0)
"""
