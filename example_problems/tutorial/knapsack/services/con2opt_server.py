#!/usr/bin/env python3

from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from zaino_lib import *

# METADATA OF THIS TAL_SERVICE:
problem="knapsack"
service="con2opt"
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
print("#? Oracle: waiting for answer or your instance of the Knapsack problem in its optimization form.")

# NON USO TALINPUT IN QUANTO IL DATO IN INGRESSO NON è DEFINITO (PUò ESSERE UN'ALTRA CHAMATA AD ORACOLO O LA RISPOSTA!)
prompt = input()
num_space = prompt.count(" ")

while num_space!=n-1:
    ps_n, ps_W = prompt.split()
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
    print(f"# Output: {o_zopt}")
    prompt = input()
    num_space = prompt.count(" ")

if ENV['goal'] == "correct":
    if str(answer) == prompt:
            TAc.print(LANG.render_feedback("ok-correct-con2opt", "Corretto!"),"green")
    else:
            TAc.print(LANG.render_feedback("no-correct-con2opt", "Sbagliato!"),"red")

if ENV['goal'] == "number_of_calls_linear_in_n":
    if str(answer) == prompt:
            if count <= n+1:
                TAc.print(LANG.render_feedback("ok-number-calls-linear-con2opt","Corretto! La tua soluzione è anche ottima, hai usato un numero lienare di chiamate a oracolo."), "green")
            if count > n+1:
                TAc.print(LANG.render_feedback("no-number-calls-linear-con2opt","Corretto! Esiste una soluzione più efficiente però che usa un numero lienare di chiamate all'oracolo."), "yellow")
    else:
            TAc.print(LANG.render_feedback("error-number-calls-linear-con2opt", "Sbagliato!"),"red")