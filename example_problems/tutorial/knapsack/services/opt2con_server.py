#!/usr/bin/env python3

from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from zaino_lib import *

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('size',str),
    ('goal',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

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
print("#? Oracle: waiting for answer or your instance of the Knapsack problem in its construction form.")
# NON USO TALINPUT IN QUANTO IL DATO IN INGRESSO NON è DEFINITO (PUò ESSERE UN'ALTRA CHAMATA AD ORACOLO O LA RISPOSTA!)
prompt = input()
count = 0
search = prompt.find(' ')

while search != -1:
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
    o_zcon = zcon(int(ps_W), ps_wt, ps_val, int(ps_n))
    count += 1
    print(f"# Output: {o_zcon}")
    prompt = input()
    search = prompt.find(' ')

if ENV['goal'] == "correct":
    if answer == int(prompt):
            TAc.print(LANG.render_feedback("ok-Truecorrect-opt2con", "Corretto!"),"green")
    else:
            TAc.print(LANG.render_feedback("no-Truecorrect-opt2con", "Sbagliato!"),"red")

if ENV['goal'] == "at_most_one_call":
    if answer == int(prompt):
            if count <= 1: 
                TAc.print(LANG.render_feedback("ok-TrueOneCall-opt2con", "Corretto! La tua soluzione è anche ottima, hai usato una sola chiamata a oracolo."),"green")
            if count > 1:
                TAc.print(LANG.render_feedback("no-TrueOneCall-opt2con", "Corretto! Esiste una soluzione più efficiente però che usa una sola chiamata all'oracolo."),"yellow") 
    else:
            TAc.print(LANG.render_feedback("error-TrueOneCall-opt2con", "Sbagliato!"),"red")
 