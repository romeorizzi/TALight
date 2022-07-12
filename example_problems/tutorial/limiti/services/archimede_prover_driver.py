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
def check_user_solution(x):
    try:
        user_sol=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
    except:
        TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto, mi spiace.'), "red", ["bold"])
        exit(0)
    if user_sol<=0 or int(user_sol)!=user_sol:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' naturale e positivo, riprova:'), "red", ["bold"])
        return check_user_solution(x)
    proof=1/user_sol
    if not proof<eval(str(x)):
        TAc.print(LANG.render_feedback("error", f'no, 1/{user_sol} = {round(proof,5)} e come noterai {round(proof,5)} >= {x}, riprova:'), "red", ["bold"])
        return check_user_solution(x)
    assert proof<eval(str(x))
    return TAc.print(LANG.render_feedback("correct", f'Bene! Infatti 1/{user_sol} = {round(proof,5)} < {x} = {eval(x)}'), "green", ["bold"])

def new_match(seed,counter):
    counter+=1
    TAc.print(LANG.render_feedback("seed", f'(seed: {seed})'), "yellow", ["bold"])
    x=ll.instance_archimede(seed)
    TAc.print(LANG.render_feedback("proposal", f'La mia proposta per x e\': {x} \ndammi un numero naturale n tale che 1/n < x:'), "yellow", ["bold"])
    check_user_solution(x)
    if counter<2:
        TAc.print(LANG.render_feedback("ok", f'Mi stai iniziando a convincere, voglio provare solo un\'altra volta:\n'), "yellow", ["bold"])
        seed=random.randint(100000,999999)
        new_match(seed,counter)
    else:
        return TAc.print(LANG.render_feedback("correct", f'Mi hai convinto, ben fatto! ;)'), "green", ["bold"])

TAc.print(LANG.render_feedback("principio-Archimede", '\nPrincipio di Archimede: per ogni numero reale x>0 esiste un numero naturale n>0 tale che 1/n < x'), "white")
TAc.print(LANG.render_feedback("proof", 'Sei pronto/a a dimostrarmi il principio di Archimede? Cominciamo subito!'), "white")
counter=0
new_match(ENV['seed'], counter)
exit(0)