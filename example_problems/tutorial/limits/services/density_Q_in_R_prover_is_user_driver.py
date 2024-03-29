#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import exit
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
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')
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

TAc.print(LANG.render_feedback("proof", '# Dimostriamo insieme che dati x,y due numeri reali, x<y , esiste un numero razionale q tale che x<q<y, ovvero Q e` denso in R. \nCominciamo subito!'), "white", ["bold"])
TAc.print(LANG.render_feedback("seed", f'# (seed: {seed})'), "yellow")
x,y=ll.instance_density(seed)
# print('y-x ',y-x)
TAc.print(LANG.render_feedback("x-proposal", f'# La mia proposta per x e`:'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("x-proposal", f'{x}'), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("y-proposal", f'# La mia proposta per y e`:'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("y-proposal", f'{y}'), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("find-N-step1", f'# PASSO 1: trovare un numero naturale N, N>0, tale che Nx ed Ny distino almeno di 1:'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("find-N-step1.2", f'#      1.1) calcola y-x:'), "yellow", ["bold"])
difference=eval(str(y-x))
user_difference=eval(TALinput(str, regex=f"^([+-]?[.\d]*)$", sep=None, TAc=TAc)[0])
if user_difference!=difference:
    TAc.print(LANG.render_feedback("error", f'no, y-x e` diverso da {user_difference}'), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("correct", 'Ok!'), "green", ["bold"])
TAc.print(LANG.render_feedback("find-N", f'#      1.2) proponi un numero naturale N>0 che soddisfi il principio di Archimede con argomento y-x={y-x}, ovvero tale che 1/N < {user_difference}: \n# (se non ricordi questo principio ti consiglio l\'esercizio -> rtal connect limits archimede_prover_is_user)'), "yellow", ["bold"])
N=check_user_solution(user_difference)
TAc.print(LANG.render_feedback("find-N", f'# PASSO 2: trovare un qualsiasi intero m nell\'intervallo (Nx,Ny)=({x*N},{y*N}) (almeno uno deve esistere, avendo costruito N tale che Nx-Ny>1):'), "yellow", ["bold"])
user_int=check_int_in_interval(N*x,N*y)
TAc.print(LANG.render_feedback("next-step", f'# PASSO 3: produrre il numero razionale q tale che x={x}<q<{y}=y.\n# Suggerimento: utilizza l\'intero m ed il naturale positivo N ottenuti sopra per produrre un tale q (nella forma a/b):'), "yellow", ["bold"])
check_q(x,y,N,user_int)
exit(0)