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
def input_N():
    try:
        user_N=eval(TALinput(str, sep=None, TAc=TAc)[0])
    except:
        TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto'), "red", ["bold"])
        exit(0)
    if user_N<=0 or int(user_N)!=user_N:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e` naturale e positivo'), "red", ["bold"])
        TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
        exit(0)
    else: 
        return int(user_N)

TAc.print(LANG.render_feedback("seed", f'# puoi richiamare questa particolare istanza specificando -aseed={ENV["seed"]}'), "yellow")
successione=ll.inf_seq(seed)
n=Symbol('n')
succ_limit = limit(successione, n, oo)
# assert type(succ_limit) is not calculus.accumulationbounds.AccumulationBounds
TAc.print(LANG.render_feedback("this-is-the-succession", f'# Data la successione \n{successione} \n# convincimi che il limite per n -> +oo esiste e vale {succ_limit}'), "yellow", ["bold"])
if succ_limit!=oo:
    epsilon_value=random.randint(1,9)/10
    TAc.print(LANG.render_feedback("epsilon", f'# Il mio valore per epsilon e`: \n{epsilon_value}'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("give-me-n_0", f'# dammi un numero naturale N > 0 tale che |{successione} - {succ_limit}| < {epsilon_value} per ogni n > N:'), "yellow", ["bold"])
    user_N=input_N()
    if user_N<=0 or int(user_N)!=user_N:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e` naturale e positivo'), "red", ["bold"])
        TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
        exit(0)
    for i in range (user_N+1,user_N+1000,):
        if abs(successione.subs(n,i)-succ_limit)>=epsilon_value:
            TAc.print(LANG.render_feedback("error", f'vedi, per n = {i} vale |{successione} - {succ_limit}|={abs(successione.subs(n,i)-succ_limit)} >= {epsilon_value}.'), "red", ["bold"])
            TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
            exit(0)
    TAc.print(LANG.render_feedback("correct-n_0", f'Molto bene! Non ho trovato nessun numero naturale n, n > {user_N}, tale che |{successione} - {succ_limit}| >= {epsilon_value}'), "green",["bold"])
    exit(0)
else:
    M_value=random.randint(5,15)
    TAc.print(LANG.render_feedback("M", f'# Il mio valore per M e`: \n{M_value}'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("give-me-N", f'# dammi un numero naturale N > 0 tale che {successione} > {M_value} per ogni n > N:'), "yellow", ["bold"]) 
    user_N=input_N()
    for i in range (user_N+1,user_N+1000,):
        if successione.subs(n,i)<=M_value:
            TAc.print(LANG.render_feedback("error", f'vedi, per n = {i} vale {successione} = {successione.subs(n,i)} <= {M_value}.'), "red", ["bold"])
            exit(0)
    TAc.print(LANG.render_feedback("correct-n_0", f'Molto bene! Non ho trovato nessun numero naturale n, n > {user_N}, tale che {successione} <= {M_value}'), "green",["bold"])
    exit(0)