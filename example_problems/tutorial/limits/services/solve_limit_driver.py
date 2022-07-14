#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from math import *
# from TALinputs import TALinput
import limiti_lib as ll
from sympy import *
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
successione=ll.inf_seq(seed)
TAc.print(LANG.render_feedback("this-is-the-succession", f'# Data la successione \n{successione} \n# avente seed={seed}, il limite per n -> +oo vale:'), "yellow", ["bold"])
n=Symbol('n')
succ_limit = limit(successione, n, oo)
# assert type(succ_limit) is not calculus.accumulationbounds.AccumulationBounds
# user_limit=TALinput(str, sep=None, TAc=TAc)[0]
TAc.print(LANG.render_feedback("this-is-the-limit", f'{succ_limit}'), "yellow", ["reverse"])
exit(0)