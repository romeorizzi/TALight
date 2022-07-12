#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
import limiti_lib as ll
import random
from math import *
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('silent',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
if ENV['silent']:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')
else:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
def evaluate_epsilon():
    try:
        user_epsilon=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
    except:
        TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto, scrivi un altro valore per epsilon:'), "red", ["bold"])
        evaluate_epsilon()
    if user_epsilon<=0:
        TAc.print(LANG.render_feedback("error", f'no, la epsilon che mi hai dato non e` positiva, dammene un\'altra:'), "red", ["bold"])
        evaluate_epsilon()
    return user_epsilon
TAc.print(LANG.render_feedback("remember", '\nREMEMBER - per svolgere questo esercizio ti puo` tornare utile la seguente definizione: il limite di una successione fn per n->inf e` finito e vale f se per ogni epsilon>0 esiste n_0>0 naturale tale che n>n_0 => |fn-f|<epsilon.'), "green")

TAc.print(LANG.render_feedback("principio-Archimede-curiosity", 'Provero` a convincerti che il limite di una successione convergente di termini positivi non e` sempre strettamente positivo.'), "white")
TAc.print(LANG.render_feedback("start", f'Prendero` come esempio la successione 1/n, n=1,2,3,... il cui limite per n -> inf e` 0 e ora te lo dimostro:'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("epsilon", f'Stabilisci un numero reale epsilon>0:'), "yellow", ["bold"])
user_epsilon=evaluate_epsilon()
TAc.print(LANG.render_feedback("n_0", f'Ecco il mio n_0:'), "yellow", ["bold"])
if user_epsilon>1:
    TAc.print(LANG.render_feedback("disprove", f'n_0=1'),  "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("disprove", f'infatti, prendendo n_0=1 vale |1/n-0| <{user_epsilon} per ogni n>1 (ovvero e` verificata la definizione di limite finito di una successione). \nNota ora pero` che vale anche il principio di Archimede per questa particolare successione poiche` tende a 0 ed e` formata da termini positivi, percio` |1/n-0|=1/n e secondo Archimede per ogni reale epsilon>0 esiste un naturale n>0 tale che 1/n<epsilon, e con la epsilon che mi hai dato vale per n=1.'),  "yellow", ["bold"])
    exit(0)
else:
    n=ceil(1/user_epsilon+0.00000000001)
    TAc.print(LANG.render_feedback("disprove", f'n={n}'),  "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("disprove", f'vedi, prendendo n_0={n} vale |1/n-0| <{user_epsilon} per ogni n>{n} (ovvero e` verificata la definizione di limite finito di una successione). \nNota ora pero` che vale anche il principio di Archimede per questa particolare successione poiche` tende a 0 ed e` formata da termini positivi, percio` |1/n-0|=1/n e secondo Archimede per ogni reale epsilon>0 esiste un naturale n>0 tale che 1/n<epsilon, e con la epsilon che mi hai dato vale per n={n}.'),  "yellow", ["bold"])
    exit(0)