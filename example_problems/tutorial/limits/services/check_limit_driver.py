#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from math import *
from TALinputs import TALinput
import limiti_lib as ll
from sympy import *
import random
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('seed',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')

# START CODING YOUR SERVICE:
seed=ENV["seed"]
# INIZIO DEL DIALOGO CON LO STUDENTE
TAc.print(LANG.render_feedback("seed", f'# puoi richiamare questa particolare istanza specificando -aseed= {ENV["seed"]}'), "yellow")
successione=ll.inf_seq(seed)
TAc.print(LANG.render_feedback("this-is-the-succession", f'# Data la successione \n{successione} \n# qual e` il suo limite per n -> +oo? (se pensi che non esista scrivi "None", se credi che sia infinito scrivi "oo")'), "yellow", ["bold"])
n=Symbol('n')
# pprint(successione)
# epsilon=Symbol('epsilon')
succ_limit = limit(successione, n, oo)
# assert type(succ_limit) is not calculus.accumulationbounds.AccumulationBounds
user_limit=TALinput(str, sep=None, TAc=TAc)[0]
try:
    eval_limit=eval(user_limit)
except:
    TAc.print(LANG.render_feedback("do-not-understand", f'non riesco a decifrare quello che mi hai scritto, mi spiace.'), "red", ["bold"])
    TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
    exit(0)
if eval_limit!=eval(str(succ_limit)):
    TAc.print(LANG.render_feedback("wrong", f'Secondo me la risposta e` sbagliata, se la vuoi conoscere chiama il servizio rtal `connect limits solve_limit -aseed={seed}`, altrimenti richiamami utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("correct", f'Corretto! Ma se vuoi convincermi chiama il servizio `rtal connect limits limit_prover_is_user -aseed={seed}`'), "green", ["bold"])
exit(0)