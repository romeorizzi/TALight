#!/usr/bin/env python3

from sys import stderr, exit, argv

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
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

g, graph, edges , m = GenerateGraph()
TAc.print(f"{graph}", "yellow")
cfc = g.printSCCs().strip()
ps = input()

l1 = len(cfc)
print(l1)
l2 = len(ps)
print(l2)
sp1=contaspazi(cfc)
print(sp1)
sp2=contaspazi(ps)
print(sp2)
if (l1 != l2 or sp1 != sp2):
    TAc.print(f"1Certificato SBAGLIATO:{cfc}", "green")
    exit(0)
for i in cfc.split(' '):
    a=permuta(i)
    ris=False
    for j in ps.split(' '):
        b=permuta(j)
        if a == b:
            ris=True
    if ris == False:
        TAc.print(f"2Certificato SBAGLIATO:{cfc}", "green")
        exit(0)
    if ris==True:
        TAc.print("/nCertificato ESATTO.", "green")