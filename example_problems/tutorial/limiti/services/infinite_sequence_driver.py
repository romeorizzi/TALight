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
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')

# START CODING YOUR SERVICE:
seed=ENV["seed"]
# INIZIO DEL DIALOGO CON LO STUDENTE
TAc.print(LANG.render_feedback("this-is-the-succession", f'Verifica se la successione che ti propongo e` limitata oppure no.'), "white", ["bold"])
TAc.print(LANG.render_feedback("seed", f'seed: {seed}'), "yellow", ["bold"])
successione=ll.inf_seq(seed)
TAc.print(LANG.render_feedback("this-is-the-succession", f'Data la successione \n{successione} \nqual e` il suo limite per n -> +oo? (se pensi che non esista scrivi "None", se credi che sia infinito scrivi "oo")'), "yellow", ["bold"])
n=Symbol('n')
# pprint(successione)
epsilon=Symbol('epsilon')
succ_limit = limit(successione, n, oo)
# assert type(succ_limit) is not calculus.accumulationbounds.AccumulationBounds
user_limit=TALinput(str, sep=None, TAc=TAc)[0]
try:
    eval_limit=eval(user_limit)
except:
    TAc.print(LANG.render_feedback("do-not-understand", f'non riesco a decifrare quello che mi hai scritto, mi spiace.'), "red", ["bold"])
    exit(0)
if eval_limit!=eval(str(succ_limit)):
    TAc.print(LANG.render_feedback("wrong", f'No, e` sbagliato.'), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("correct", f'Corretto!'), "green", ["bold"])
if succ_limit==oo:
    TAc.print(LANG.render_feedback("limited", f'Quindi la successione e` limitata? (y/n)'), "yellow", ["bold"])
    y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
    if y_n=='n':
        TAc.print(LANG.render_feedback("correct", f'Esatto, infatti una successione e` limitata se il limite per n -> +oo e` finito, e questa ha limite oo.'), "green", ["bold"])
        exit(0)
    else:
        TAc.print(LANG.render_feedback("wrong", f'No, infatti una successione e` limitata se il limite per n -> +oo e` finito, e questa ha limite oo.'), "red", ["bold"])
        exit(0)
TAc.print(LANG.render_feedback("next-step", f'Allora non avrai problemi a dimostrarmelo ;)'), "yellow", ["bold"])
epsilon_value=random.randint(1,9)/10
TAc.print(LANG.render_feedback("epsilon", f'Il mio valore per epsilon e`: \n{epsilon_value}'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("give-me-n_0", f'dammi un valore per n_0 naturale, n_0 > 0 tale che |{successione}-{succ_limit}|<{epsilon_value} per ogni n>n_0:'), "yellow", ["bold"])
try:
    user_n_0=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
except:
    TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto'), "red", ["bold"])
    exit(0)
if user_n_0<=0 or int(user_n_0)!=user_n_0:
    TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' naturale e positivo.'), "red", ["bold"])
    exit(0)
user_n_0=int(user_n_0)
for i in range (user_n_0+1,user_n_0+1000,10):
    if abs(successione.subs(n,i)-succ_limit)>=epsilon_value:
        TAc.print(LANG.render_feedback("error", f'vedi, per n={i} vale |{successione}-{succ_limit}|={abs(successione.subs(n,i)-succ_limit)}>={epsilon_value}.'), "red", ["bold"])
        exit(0)
TAc.print(LANG.render_feedback("correct-n_0", f'Perfetto! Vale |{successione}-{succ_limit}| < {epsilon_value} per tutti i valori di n > {user_n_0} che ho utilizzato per verificare la tua proposta.'), "green",["bold"])
TAc.print(LANG.render_feedback("limited", f'Quindi la successione e` limitata? (y/n)'), "yellow", ["bold"])
y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
if y_n=='y':
    TAc.print(LANG.render_feedback("correct", f'Esatto, infatti una successione e` limitata se il limite per n -> +oo e` finito, e qui vale {succ_limit}.'), "green", ["bold"])
    exit(0)
else:
    TAc.print(LANG.render_feedback("wrong", f'Si che e` limitata, infatti il limite per n -> +oo e` finito, e qui vale {succ_limit}.'), "red", ["bold"])
    exit(0)
