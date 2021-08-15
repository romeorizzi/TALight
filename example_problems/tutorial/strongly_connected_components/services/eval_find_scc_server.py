#!/usr/bin/env python3

from sys import stderr, exit

import collections

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from scc_lib import *

# aggiorna meta.yaml
# METADATA OF THIS TAL_SERVICE:
problem="strongly_connected_components"
service="eval_find_scc"
args_list = [
    ('code_lang',str),
    ('goal',str),
    ('lang',str),
    ('seed',str),
]


ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

seed = ENV['seed']
g, graph, edges , m,a = GenerateGraph(seed)
TAc.print(f"\nSeed dell'istanza: {a}\n", "yellow")
TAc.print(f"{graph}", "yellow")
cfc = g.printSCCs().strip()
ps = input()

l1 = len(cfc)
l2 = len(ps)
sp1=contaspazi(cfc)
sp2=contaspazi(ps)
if (l1 != l2 or sp1 != sp2):
    TAc.print(f"Certificato SBAGLIATO:{cfc}", "green")
    exit(0)
for i in cfc.split(' '):
    a=permuta(i)
    ris=False
    for j in ps.split(' '):
        b=permuta(j)
        if a == b:
            ris=True
    if ris == False:
        TAc.print(f"Certificato SBAGLIATO:{cfc}", "green")
        exit(0)
    if ris==True:
        TAc.print("\nCertificato ESATTO.", "green")
        exit(0)