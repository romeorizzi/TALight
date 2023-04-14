#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
from math import *
# METADATA OF THIS TAL_SERVICE:
args_list = [
    # ('silent',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:

TAc.print(LANG.render_feedback("principio-Archimede-curiosity", '# Provero` a convincerti che il limite di una successione convergente di termini positivi non e` sempre strettamente positivo.'), "white")
TAc.print(LANG.render_feedback("start", f'# Consideriamo infatti la successione 1/n, n=1,2,3,... \n# la mia affermazione e` che il limite per n -> inf e` 0.'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("epsilon", f'# Prova a confutare la mia affermazione proponendo un numero reale epsilon > 0:'), "yellow", ["bold"])
try:
    user_epsilon=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
except:
    TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto'), "red", ["bold"])
    exit(0)
if user_epsilon<=0:
    TAc.print(LANG.render_feedback("error", f'no, {user_epsilon} <= 0'), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("N", f'Ecco il mio N:'), "yellow", ["bold"])
if user_epsilon>1:
    TAc.print(LANG.render_feedback("disprove", f'N = 1'),  "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("disprove", f'infatti, vale |1/n-0| < {user_epsilon} per ogni n > 1 (ovvero e` verificata la definizione di limite finito di una successione). \nNota ora che vale anche il principio di Archimede per questa particolare successione poiche` tende a 0 ed e` formata da termini positivi, percio` |1/n-0| = 1/n e secondo Archimede per ogni reale epsilon > 0 esiste un naturale n > 0 tale che 1/n < epsilon, e con la epsilon che mi hai dato vale per n = 1.'),  "yellow", ["bold"])
    exit(0)
else:
    n=ceil(1/user_epsilon+0.00000000001)
    TAc.print(LANG.render_feedback("disprove", f'N = {n}'),  "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("disprove", f'vedi, vale |1/n-0| < {user_epsilon} per ogni n > {n} (ovvero e` verificata la definizione di limite finito di una successione). \nNota ora che vale anche il principio di Archimede per questa particolare successione poiche` tende a 0 ed e` formata da termini positivi, percio` |1/n-0| = 1/n e secondo Archimede per ogni reale epsilon > 0 esiste un naturale n > 0 tale che 1/n < epsilon, e con la epsilon che mi hai dato vale per n = {n}.'),  "yellow", ["bold"])
    exit(0)