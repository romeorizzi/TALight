#!/usr/bin/env python3

from sys import stderr, exit, argv

from time import monotonic

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from zaino_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="knapsack"
service="opt2dec"
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
print("#? Oracle: waiting for answer or your instance of the Knapsack problem in its decision form.")
# NON USO TALINPUT IN QUANTO IL DATO IN INGRESSO NON è DEFINITO (PUò ESSERE UN'ALTRA CHAMATA AD ORACOLO O LA RISPOSTA!)
start = monotonic()
prompt = input()
count = 0
search = prompt.find(' ')

while search != -1:
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
    search = prompt.find(' ')

end = monotonic()
time = end - start

if ENV['goal'] == "correct":
    if answer == int(prompt):
            TAc.print(LANG.render_feedback("ok-correct-opt2dec", "Corretto!"),"green")
    else:
            TAc.print(LANG.render_feedback("no-correct-opt2dec", "Sbagliato!"),"red")


if ENV['goal'] == "at_most_opt_calls":
    print("DA FARE")

if ENV['goal'] == "polynomial":
    if answer == int(prompt):
        if time > 1:
            TAc.print(LANG.render_feedback("no-polynomial-opt2dec", f"Corretto! Il tuo algoritmo non è molto efficiente, ci mette {time}s sulla tua macchina."),"yellow")
        else:
            TAc.print(LANG.render_feedback("ok-polynomial-opt2dec", f"Corretto! Il tuo algoritmo è molto efficiente, ci mette {time}s sulla tua macchina."),"green")
    else:
        TAc.print(LANG.render_feedback("error-polynomial-opt2dec", "Sbagliato!"),"red")

