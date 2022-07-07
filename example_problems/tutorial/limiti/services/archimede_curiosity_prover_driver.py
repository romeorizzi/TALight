#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
import random
from math import *
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('seed',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
seed=ENV["seed"]
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
        TAc.print(LANG.render_feedback("error", f'no, 1/{user_sol} = {round(proof,5)} e non verifica la condizione |fn-f|<epsilon, ovvero |1/n-0|={round(proof,5)}<{x}... '), "red", ["bold"])
        exit(0)
    assert proof<eval(str(x))
    return TAc.print(LANG.render_feedback("correct", f'Molto bene! Infatti vale |1/n-0| <{epsilon} per ogni n>{user_sol} (ovvero e` verificata la definizione di limite finito di una successione). \nNota ora pero` che vale anche il principio di Archimede per questa particolare successione poiche` tende a 0 ed e` formata da termini positivi, percio` |1/n-0|=1/n e secondo Archimede per ogni reale epsilon>0 esiste un naturale n>0 tale che 1/n<epsilon, e con la epsilon che ti ho dato vale per n={user_sol}.'), "green", ["bold"])

TAc.print(LANG.render_feedback("remember", '\nREMEMBER - per svolgere questo esercizio ti puo` tornare utile la seguente definizione: il limite di una successione fn per n->inf e` finito e vale f se per ogni epsilon>0 esiste n_0>0 naturale tale che n>n_0 => |fn-f|<epsilon.'), "green")

TAc.print(LANG.render_feedback("principio-Archimede-curiosity", 'Il limite di una successione convergente di termini positivi non e` sempre strettamente positivo.'), "white")
TAc.print(LANG.render_feedback("start", f'Consideriamo ad esempio la successione 1/n, n=1,2,3,... qual e` il limite per n -> inf?'), "yellow", ["bold"])
try:
    user_lim=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
except:
    TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto, mi spiace.'), "red", ["bold"])
    exit(0)
if user_lim==0:
    TAc.print(LANG.render_feedback("correct", f'Ottimo!'), "green", ["bold"])
    TAc.print(LANG.render_feedback("start", f'Beh, allora non avrai problemi a dimostrarmelo ;)'), "yellow", ["bold"])
else:
    TAc.print(LANG.render_feedback("error", f'No, non e` corretto.'), "red", ["bold"])
    exit(0)
random.seed(seed)
epsilon=float(format(random.random(),'.3f'))
TAc.print(LANG.render_feedback("start", f'Il mio valore per epsilon e`: \n{epsilon}'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("start", f'Proponi il tuo n_0 (che sia naturale e n_0>0):'), "yellow", ["bold"])
check_user_solution(epsilon)
exit(0)