#!/usr/bin/env python3

from sys import stderr, exit, argv
from time import monotonic

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from zaino_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="knapsack"
service="con2dec"
args_list = [
    ('size',str),
    ('seed',str),
    ('goal',str),
    ('ask_for_one_opt_oracle_call', int),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING OF YOUR SERVICE
print("# Instance of the Knapsack problem in its construction form you have to resolve.")
size = ENV['size']
seed = ENV['seed']

a, W, wt, val, n = GenZcon(size, seed)
print(f"\nSeed dell'istanza: {a}")
print(f"{n} {W}")
a_wt = wt.split(",")
a_val = val.split(",")
for x,y in zip(a_wt,a_val):
   print(x+" "+y)
a_wt = [int(i) for i in a_wt]
a_val = [int(i) for i in a_val]
answer = zcon(W, a_wt, a_val, n)
print("\n")
count = 0
start = monotonic()

if ENV['ask_for_one_opt_oracle_call'] == 1:
    print("#? Oracle: waiting for your instance of the Knapsack problem in its optimization form.")
    ps_n, ps_W = TALinput(int, 2, TAc=TAc)
    ps_wt = []
    ps_val = []
    for i in range(ps_n):
        if i == 0:
            PSwt, PSval = TALinput(int, 2, TAc=TAc)
            ps_wt.append(PSwt)
            ps_val.append(PSval)
        else:
            PSwt, PSval = TALinput(int, 2, TAc=TAc)
            ps_wt.append(PSwt)
            ps_val.append(PSval)
    o_zopt = zopt(ps_W, ps_wt, ps_val, ps_n)
    print(f"# Output: {o_zopt}")


print("#? Oracle: waiting for answer or your instance of the Knapsack problem in its decision form.")
# NON USO TALINPUT IN QUANTO IL DATO IN INGRESSO NON è DEFINITO (PUò ESSERE UN'ALTRA CHAMATA AD ORACOLO O LA RISPOSTA!)
prompt = input()
num_space = prompt.count(" ")

while num_space!=n-1:
    ps_n, ps_W, ps_target = prompt.split()
    ps_wt = []
    ps_val = []
    for i in range(int(ps_n)):
        if i == 0:
            PSwt, PSval = TALinput(int, 2, TAc=TAc)
            ps_wt.append(PSwt)
            ps_val.append(PSval)
        else:
            PSwt, PSval = TALinput(int, 2, TAc=TAc)
            ps_wt.append(PSwt)
            ps_val.append(PSval)
    o_zdec = zdec(int(ps_W), ps_wt, ps_val, int(ps_n), int(ps_target))
    count += 1
    print(f"# Output: {o_zdec}")
    prompt = input()
    num_space = prompt.count(" ")

end = monotonic()
time = end - start

if ENV['goal'] == "correct":
    if str(answer) == prompt:
            TAc.print(LANG.render_feedback("ok-correct-con2dec", "Corretto!"),"green")
    else:
            TAc.print(LANG.render_feedback("no-correct-con2dec", "Sbagliato!"),"red")

if ENV['goal'] == "polynomial_dec_calls":
    if str(answer) == prompt:
        if time > 1:
            TAc.print(LANG.render_feedback("no-polynomial-con2dec", f"Corretto! Il tuo algoritmo non è molto efficiente, ci mette {time}s sulla tua macchina."),"yellow")
        else:
            TAc.print(LANG.render_feedback("ok-polynomial-con2dec", f"Corretto! Il tuo algoritmo è molto efficiente, ci mette {time}s sulla tua macchina."),"green")
    else:
        TAc.print(LANG.render_feedback("error-polynomial-con2dec", "Sbagliato!"),"red")

if ENV['goal'] == "at_most_n_dec_calls":
    if str(answer) == prompt:
            if count <= n:
                TAc.print(LANG.render_feedback("yes-most-n-dec-calls-con2dec", "Corretto! La tua soluzione è anche ottima, hai usato massimo n numero di chiamate a oracolo."),"green")
            if count > n:
                TAc.print(LANG.render_feedback("no-most-n-dec-calls-con2dec", "Corretto! Esiste una soluzione più efficiente però che usa massimo n numero di chiamate a oracolo."),"yellow")
    else:
            TAc.print(LANG.render_feedback("error-most-n-dec-calls-con2dec", "Sbagliato!"),"red")




