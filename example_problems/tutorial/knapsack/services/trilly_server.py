#!/usr/bin/env python3

from sys import stderr, exit

from time import monotonic

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from zaino_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="knapsack"
service="trilly"
args_list = [
    ('size',str),
    ('seed',str),
    ('goal',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

print("# Instance of the Knapsack problem in its optimization form you have to resolve.")
size = ENV['size']
seed = ENV['seed']

a, W, wt, val, n = GenZopt(size, seed)
print(f"\nSeed dell'istanza: {a}")
print(f"{n} {W}")
a_wt = wt.split(",")
a_val = val.split(",")
for x,y in zip(a_wt,a_val):
   TAc.print(x+" "+y,"yellow")
a_wt = [int(i) for i in a_wt]
a_val = [int(i) for i in a_val]
answer = zopt(W, a_wt, a_val, n)
print("\n")
print("#? Oracle: waiting for answer or your instance of the Knapsack problem in its optimization form.")
# NON USO TALINPUT IN QUANTO IL DATO IN INGRESSO NON è DEFINITO (PUò ESSERE UN'ALTRA CHAMATA AD ORACOLO O LA RISPOSTA!)
start = monotonic()
prompt = input()
count = 0
search = prompt.find(' ')

while search != -1:
    ps_n, ps_W = prompt.split()
    if int(ps_n) >= n:
        print ("Le chiamate ad oracolo devono essere di istanze al massimo di n-1 elementi")
        exit(0)
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
    o_zopt = zopt(int(ps_W), ps_wt, ps_val, int(ps_n))
    count += 1
    print(f"# Output: {o_zopt}")
    prompt = input()
    search = prompt.find(' ')

end = monotonic()
time = end - start

if ENV['goal'] == "correct":
    if str(answer) == prompt:
            TAc.print(LANG.render_feedback("ok-correct-trilly", "Corretto!"),"green")
    else:
            TAc.print(LANG.render_feedback("no-correct-trilly", "Sbagliato!"),"red")

if ENV['goal'] == "polynomial":
    if str(answer) == prompt:
        if time > 1:
            TAc.print(LANG.render_feedback("no-polynomial-trilly", f"Corretto! Il tuo algoritmo non è molto efficiente, ci mette {time}s sulla tua macchina."),"yellow")
        else:
            TAc.print(LANG.render_feedback("ok-polynomial-trilly", f"Corretto! Il tuo algoritmo è molto efficiente, ci mette {time}s sulla tua macchina."),"green")
    else:
        TAc.print(LANG.render_feedback("error-polynomial-trilly", "Sbagliato!"),"red")

if ENV['goal'] == "at_most_n_opt_calls":
    if str(answer) == prompt:
            if count <= n:
                TAc.print(LANG.render_feedback("ok-at-most-n-opt-trilly","Corretto! La tua soluzione è anche ottima, hai usato massimo n chiamate a oracolo."), "green")
            if count > n:
                TAc.print(LANG.render_feedback("no-at-most-n-opt-trilly","Corretto! Esiste una soluzione più efficiente però che usa massimo n chiamate a oracolo."), "yellow")
    else:
            TAc.print(LANG.render_feedback("error-at-most-n-opt-trilly", "Sbagliato!"),"red")

if ENV['goal'] == "at_most_2_opt_calls":   
    if str(answer) == prompt:
            if count <= 2:
                TAc.print(LANG.render_feedback("ok-at-most-2-opt-trilly","Corretto! La tua soluzione è anche ottima, hai usato massimo 2 chiamate a oracolo."), "green")
            if count > 2:
                TAc.print(LANG.render_feedback("no-at-most-2-opt-trilly","Corretto! Esiste una soluzione più efficiente però che usa massimo 2 chiamate a oracolo."), "yellow")
    else:
            TAc.print(LANG.render_feedback("error-at-most-2-opt-trilly", "Sbagliato!"),"red")



