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
    ('seed',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
def check_user_solution(x):
    try:
        user_sol=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
    except:
        TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto, mi spiace.'), "red", ["bold"])
        exit(0)
    if user_sol<=0 or int(user_sol)!=user_sol:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' naturale e positivo'), "red", ["bold"])
        TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
        exit(0)
    proof=1/user_sol
    if not proof<eval(str(x)):
        TAc.print(LANG.render_feedback("error", f'no, 1/{user_sol} = {round(proof,5)} e come noterai {round(proof,5)} >= {x}'), "red", ["bold"])
        TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
        exit(0)
    assert proof<eval(str(x))
    return TAc.print(LANG.render_feedback("correct", f'Ok! Infatti 1/{user_sol} = {round(proof,5)} < {x} = {round(eval(str(x)),4)}'), "green", ["bold"])

def new_match(seed):
    TAc.print(LANG.render_feedback("seed", f'# puoi richiamare questa particolare istanza specificando -aseed={ENV["seed"]}'), "yellow")
    x=ll.instance_archimede(seed)
    TAc.print(LANG.render_feedback("proposal", f'# Proposto x: \n{x} \n# che vale circa {round(eval(str(x)),4)}\n# dammi un numero naturale n tale che 1/n < x:'), "yellow", ["bold"])
    check_user_solution(x)
    return TAc.print(LANG.render_feedback("correct", f'Mi hai convinto, ben fatto! ;)'), "green", ["bold"])

TAc.print(LANG.render_feedback("principio-Archimede", '\n# Convincimi che per ogni numero reale x>0 esiste un numero naturale n>0 tale che 1/n < x.'), "white")
new_match(ENV['seed'])
exit(0)