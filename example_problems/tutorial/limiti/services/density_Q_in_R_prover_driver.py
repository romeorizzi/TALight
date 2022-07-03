#!/usr/bin/env python3
from sys import exit

from numpy import diff
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
import limiti_lib as ll
from math import *
import re
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
    user_sol=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
    if user_sol<=0 or int(user_sol)!=user_sol:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e` naturale positivo, riprova:'), "red", ["bold"])
        return check_user_solution(x)
    proof=1/user_sol
    if not proof<eval(str(x)):
        TAc.print(LANG.render_feedback("error", f'no, 1/{user_sol} = {round(proof,5)} e come noterai {round(proof,5)} >= {x}=y-x, riprova:'), "red", ["bold"])
        return check_user_solution(x)
    assert proof<eval(str(x))
    TAc.print(LANG.render_feedback("correct", ll.correct), "green", ["bold"])
    return user_sol

def check_int_in_interval(nx,ny):
    user_int=eval(TALinput(str, regex=f"^[+-]?\d*$", sep=None, TAc=TAc)[0])
    if user_int<=nx:
        TAc.print(LANG.render_feedback("error", f'guarda che {user_int}<={nx}, riprova:'), "red", ["bold"])
        return check_int_in_interval(nx,ny)
    if user_int>=ny:
        TAc.print(LANG.render_feedback("error", f'guarda che {user_int}>={ny}, ritenta:'), "red", ["bold"])
        return check_int_in_interval(nx,ny)
    TAc.print(LANG.render_feedback("correct", ll.correct), "green", ["bold"])
    return user_int

def check_q(x,y,n,user_int):
    q=TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0]
    regex = '^[-+*()\d]+(/)[-+*()\d]+$'
    result = re.match(regex, q)
    if not result:
        TAc.print(LANG.render_feedback("error", f'non hai inserito un numero razionale nella forma da me indicata (ovvero a/b)... riprova:'), "red", ["bold"])	
        return check_q(x,y,n,user_int)
    elif eval(q)<x:
        TAc.print(LANG.render_feedback("error", f'guarda che {q}<{x}, riprova:'), "red", ["bold"])
        return check_q(x,y,n,user_int)
    elif eval(q)>y:
        TAc.print(LANG.render_feedback("error", f'guarda che {q}>{y}, riprova:'), "red", ["bold"])
        return check_q(x,y,n,user_int)
    correct_q=user_int/n
    if eval(q)!=correct_q:
        TAc.print(LANG.render_feedback("error", f'ci sei quasi! il numero razionale che hai inserito e` compreso tra x ed y ma puoi fare di meglio: utilizza una relazione tra l\'intero che hai scelto (ovvero {user_int}) ed n={n} per creare un intero della forma \'a/b\', riprova:'), "yellow", ["bold"])
        return check_q(x,y,n,user_int)
    return TAc.print(LANG.render_feedback("correct", f'Ben fatto! Abbiamo trovato la q che cercavamo, infatti {q} = {eval(q)} e` compresa tra x={x} ed y={y}.'), "green", ["bold"])

def user_nx(n,x):
    user_nx=eval(TALinput(str, regex=f"^([+-]?[.\d]*)$", sep=None, TAc=TAc)[0])
    nx=eval(str(round(n*x,2)))
    if user_nx!=nx:
        TAc.print(LANG.render_feedback("error", f'no, nx e` diverso da {user_nx}, ricalcola:'), "red", ["bold"])
        return user_nx()
    return nx
def user_ny(n,y):
    user_ny=eval(TALinput(str, regex=f"^([+-]?[.\d]*)$", sep=None, TAc=TAc)[0])
    ny=eval(str(round(n*y,2)))
    if user_ny!=ny:
        TAc.print(LANG.render_feedback("error", f'no, ny e` diverso da {user_ny}, ricalcola:'), "red", ["bold"])
        return user_ny(n,y)
    return user_ny

TAc.print(LANG.render_feedback("proof", '# Dimostriamo insieme che dati x,y due numeri reali, x<y , esiste un numero razionale q tale che x<q<y, ovvero Q e` denso in R. \nCominciamo subito!'), "white", ["bold"])
TAc.print(LANG.render_feedback("seed", f'# (seed: {seed})'), "yellow", ["bold"])
x,y=ll.instance_density(seed)
# print('y-x ',y-x)
TAc.print(LANG.render_feedback("x-proposal", f'# La mia proposta per x e`:'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("x-proposal", f'{x}'), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("y-proposal", f'# La mia proposta per y e`:'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("y-proposal", f'{y}'), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("find-n", f'# PASSO 1: trovare un numero n naturale, n>0, tale che nx ed ny distino almeno di 1; costruiamo insieme questa n: \n# 1.1) calcola y-x:'), "yellow", ["bold"])
difference=eval(str(y-x))
user_difference=eval(TALinput(str, regex=f"^([+-]?[.\d]*)$", sep=None, TAc=TAc)[0])
if user_difference!=difference:
    TAc.print(LANG.render_feedback("error", f'no, y-x e` diverso da {user_difference}'), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("find-n", f'# 1.2) scrivi un numero naturale n>0 che soddisfi il principio di Archimede con argomento y-x, ovvero {user_difference}: \n# (se non ricordi questo principio ti consiglio l\'esercizio -> rtal connect limiti archimede_prover)'), "yellow", ["bold"])
n=check_user_solution(user_difference)
TAc.print(LANG.render_feedback("find-n", f'# PASSO 2: trovare un intero nell\'intervallo (nx,ny), che sappiamo esistere poiche` abbiamo costruito n tale che nx-ny>1: \n# 2.1) calcola nx (arrotonda a 2 cifre decimali se necessario):'), "yellow", ["bold"])
user_nx=user_nx(n,x)
TAc.print(LANG.render_feedback("find-n", f'# 2.2) calcola ny (arrotonda a 2 cifre decimali se necessario):'), "yellow", ["bold"])
user_ny=user_ny(n,y)
TAc.print(LANG.render_feedback("find-n", f'# 2.3) dammi un intero nell\'intervallo ({user_nx} , {user_ny}):'), "yellow", ["bold"])
user_int=check_int_in_interval(user_nx,user_ny)
TAc.print(LANG.render_feedback("next-step", f'# PASSO 3: trovare la q che secondo l\'enunciato e` tale che x<q<y. \n# Utilizzando l\'intero {user_int} e la n che mi hai proposto prima, riusciresti a trovare un numero razionale (nella forma a/b) compreso tra x={x} e y={y}? scrivilo:'), "yellow", ["bold"])
check_q(x,y,n,user_int)

TAc.print(LANG.render_feedback("algorithm", '\nSe te la senti potresti provare a scrivere (richiamando un bot) un algoritmo che dati x e y trovi q seguendo la traccia di quello che abbiamo appena dimostrato insieme: se ci riuscirai avrai dimostrato la densita\' di Q in R! ;)'),  "white", ["bold"])
exit(0)