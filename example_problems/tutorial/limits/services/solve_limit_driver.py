#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from math import *
# from TALinputs import TALinput
import limiti_lib as ll
from sympy import *
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('input',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')

# START CODING YOUR SERVICE:
input_instance=ENV["input"]
# INIZIO DEL DIALOGO CON LO STUDENTE
n=Symbol('n')
if input_instance=='terminal':
    TAc.print(LANG.render_feedback("waiting", f'# Mi aspetto ora che tu inserisca una successione. \n# Formato: una riga unica, la successione deve essere nella variabile \'n\'. Puoi inserire anche costanti matematiche e funzioni presenti nella libreria math (se necessario consulta il sito https://docs.python.it/html/lib/module-math.html)\n# Qualsiasi riga che inizia con il carattere "#" viene ignorata.\n# Se preferisci, puoi richiamare il servizio con `rtal connect limits solve_limit -ainput=seed_che_identifica_la_successione` invece di scriverla/copiarla e incollarla tu stesso qui sul terminale.'), "yellow", ["bold"])
    successione=TALinput(str, regex='^[\w */()+-]*$', sep='\n', TAc=TAc)[0]
else:
    seed=int(input_instance)
    successione=ll.inf_seq(seed)
    TAc.print(LANG.render_feedback("this-is-the-succession", f'# Data la successione \n{successione} \n# avente seed={seed}'), "yellow", ["bold"])
succ_limit = limit(successione, n, oo)
# assert type(succ_limit) is not calculus.accumulationbounds.AccumulationBounds
# user_limit=TALinput(str, sep=None, TAc=TAc)[0]
TAc.print(LANG.render_feedback("this-is-the-limit", f'il limite per n -> +oo vale:'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("this-is-the-limit", f'{succ_limit}'), "yellow", ["reverse"])
exit(0)