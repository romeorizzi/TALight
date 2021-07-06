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

size = ENV['size']
seed = ENV['seed']

a, W, wt, val, n = GenZopt(size, seed)

TAc.print(f"\nSeed dell'istanza: {a}\n", "yellow")
TAc.print(f"{n} {W}", "yellow")
a_wt = wt.split(",")
a_val = val.split(",")
for x,y in zip(a_wt,a_val):
   TAc.print(x+" "+y,"yellow")
a_wt = [int(i) for i in a_wt]
a_val = [int(i) for i in a_val]
answer = zopt(W, a_wt, a_val, n)
print("\n")
start = monotonic()
prompt = input()
count = 0
search = prompt.find(' ')

while search != -1:
    ps_n, ps_W, ps_target = prompt.split()
    ps_wt = ""
    ps_val = ""
    for i in range(int(ps_n)):
        if i == 0:
            PSwt, PSval = input().split()
            ps_wt = PSwt
            ps_val = PSval
        else:
            PSwt, PSval = input().split()
            ps_wt = ps_wt+","+PSwt
            ps_val = ps_val+","+PSval           
    a_ps_wt = ps_wt.split(",")
    a_ps_val = ps_val.split(",")
    a_ps_wt = [int(i) for i in a_ps_wt]
    a_ps_val = [int(i) for i in a_ps_val]
    o_zdec = zdec(int(ps_W), a_ps_wt, a_ps_val, int(ps_n), int(ps_target))
    count += 1
    TAc.print(o_zdec, "yellow")
    prompt = input()
    search = prompt.find(' ')

end = monotonic()
time = end - start

if ENV['goal'] == "correct":
    if str(answer) == prompt:
            TAc.print("\nCORRETTO!", "green")
    else:
            TAc.print("\nSBAGLIATO!", "red")


if ENV['goal'] == "at_most_opt_calls":
    print("DA FARE")


if ENV['goal'] == "polynomial":
    if str(answer) == prompt:
        if time > 1:
            TAc.print("\nCORRETTO! Il tuo algoritmo non è molto efficiente.\n", "yellow")
        else:
            TAc.print("\CORRETTO! Il tuo algoritmo è anche efficiente, hai raggiunto l'obiettivo!\n", "green")
    else:
        TAc.print("\nSBAGLIATO!", "red")
