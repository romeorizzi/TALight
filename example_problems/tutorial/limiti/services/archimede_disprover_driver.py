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
def disprove():
    x=TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0]
    try:
        x_eval=eval(x)
    except:
        TAc.print(LANG.render_feedback("error", f'non capisco cos\'hai scritto, mi spiace'), "red", ["bold"])
        exit(0)
    if x_eval<=0:
        TAc.print(LANG.render_feedback("error", f'hai inserito un valore per x<=0... dammene un altro:'), "red", ["bold"])
        disprove()
    else:
        if x_eval>1:
            TAc.print(LANG.render_feedback("disprove", f'n=1'),  "yellow", ["reverse"])
            return TAc.print(LANG.render_feedback("disprove", f'infatti, per n=1 vale 1/n=1 < {x}=x.'),  "yellow", ["bold"])
        n=ceil(1/x_eval+0.00000000001)
        n_reciprocal=1/n
        TAc.print(LANG.render_feedback("disprove", f'n={n}'),  "yellow", ["reverse"])
        return TAc.print(LANG.render_feedback("disprove", f'infatti, per n={n} vale 1/n= {n_reciprocal} < {x}=x.'),  "yellow", ["bold"])

TAc.print(LANG.render_feedback("principio-Archimede", '\nProvero` a convincerti che per ogni numero reale x>0 esiste un numero naturale n>0 tale che 1/n < x.'), "white")
TAc.print(LANG.render_feedback("disprove", 'Inserisci un qualsiasi valore reale x>0:'),  "yellow", ["bold"])
disprove()
TAc.print(LANG.render_feedback("what-to-do", f'\nSe ora vuoi provare a convincermi tu, invertendo i ruoli, ti consiglio il servizio `rtal connect limiti archimede_prover`'),  "white", ["bold"])