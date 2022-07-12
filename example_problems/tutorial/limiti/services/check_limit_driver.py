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
    ('silent',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
if ENV['silent']:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')
else:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')

# START CODING YOUR SERVICE:
seed=ENV["seed"]
# INIZIO DEL DIALOGO CON LO STUDENTE
TAc.print(LANG.render_feedback("seed", f'seed: {seed}'), "yellow", ["bold"])
successione=ll.inf_seq(seed)
TAc.print(LANG.render_feedback("this-is-the-succession", f'Data la successione \n{successione} \nqual e` il suo limite per n -> +oo? (se pensi che non esista scrivi "None", se credi che sia infinito scrivi "oo")'), "yellow", ["bold"])
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
    exit(0)
if eval_limit!=eval(str(succ_limit)):
    TAc.print(LANG.render_feedback("wrong", f'Secondo me invece vale {succ_limit}.'), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("correct", f'Corretto!'), "green", ["bold"])
TAc.print(LANG.render_feedback("next-step", f'Allora non avrai problemi a dimostrarmelo ;)'), "yellow", ["bold"])
if succ_limit!=oo:
    epsilon_value=random.randint(1,9)/10
    TAc.print(LANG.render_feedback("epsilon", f'Il mio valore per epsilon e`: \n{epsilon_value}'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("give-me-n_0", f'dammi un numero naturale N > 0 tale che |{successione}-{succ_limit}|<{epsilon_value} per ogni n>N:'), "yellow", ["bold"])
    def input_N():
        try:
            user_N=eval(TALinput(str, sep=None, TAc=TAc)[0])
        except:
            TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto, inserisci un altro numero:'), "red", ["bold"])
            input_N()
        if user_N<=0 or int(user_N)!=user_N:
            TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' naturale e positivo, inserisci un altro numero:'), "red", ["bold"])
            input_N()
        else: 
            return int(user_N)
    user_N=input_N()
    for i in range (user_N+1,user_N+1000,):
        if abs(successione.subs(n,i)-succ_limit)>=epsilon_value:
            TAc.print(LANG.render_feedback("error", f'vedi, per n={i} vale |{successione}-{succ_limit}|={abs(successione.subs(n,i)-succ_limit)}>={epsilon_value}.'), "red", ["bold"])
            exit(0)
    TAc.print(LANG.render_feedback("correct-n_0", f'Molto bene! In effetti non sono riuscito a trovare nessun valore per n>{user_N} che smentisca la condizione |{successione}-{succ_limit}|<{epsilon_value}'), "green",["bold"])
    exit(0)
else:
    M_value=random.randint(5,15)
    TAc.print(LANG.render_feedback("M", f'Il mio valore per M e`: \n{M_value}'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("give-me-N", f'dammi un numero naturale N > 0 tale che {successione}>{M_value} per ogni n>N:'), "yellow", ["bold"])
    def input_N():
        try:
            user_N=eval(TALinput(str, sep=None, TAc=TAc)[0])
        except:
            TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto, inserisci un altro numero:'), "red", ["bold"])
            input_N()
        if user_N<=0 or int(user_N)!=user_N:
            TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' naturale e positivo, inserisci un altro numero:'), "red", ["bold"])
            input_N()
        else: 
            return int(user_N)
    user_N=input_N()
    for i in range (user_N+1,user_N+1000,):
        if successione.subs(n,i)<=M_value:
            TAc.print(LANG.render_feedback("error", f'vedi, per n={i} vale {successione}={successione.subs(n,i)}<={M_value}.'), "red", ["bold"])
            exit(0)
    TAc.print(LANG.render_feedback("correct-n_0", f'Molto bene! In effetti non sono riuscito a trovare nessun valore per n>{user_N} che smentisca la condizione {successione}>{M_value}'), "green",["bold"])
    exit(0)