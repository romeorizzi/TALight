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
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
def check_user_solution(x):
    user_sol=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
    if user_sol<=0 or int(user_sol)!=user_sol:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' naturale positivo, riprova:'), "red", ["bold"])
        return check_user_solution()
    proof=1/user_sol
    if not proof<eval(str(x)):
        error_answer=random.choice([f'no, 1/{user_sol} = {round(proof,5)} e come noterai {round(proof,5)} >= {x}, riprova:', f'mmm ho paura che tu abbia sbagliato, infatti 1/{user_sol} = {round(proof,5)} e come noterai {round(proof,5)} >= {x}, ritenta:'])
        TAc.print(LANG.render_feedback("error", error_answer), "red", ["bold"])
        return check_user_solution(x)
    assert proof<eval(str(x))
    return TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])

def prove_0_convergence():
    TAc.print(LANG.render_feedback("start", f'Stabilisci un numero reale epsilon > 0:'), "yellow", ["bold"])
    epsilon=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
    if epsilon<=0:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' positivo...'), "red", ["bold"])
        return prove_0_convergence()
    else:
        n=1 if epsilon>1 else ceil(1/epsilon+0.00000000001)
        TAc.print(LANG.render_feedback("n_0", f'Ecco il mio n_0: {n}'), "yellow", ["bold"])
        return n

def verify_n(n_0):
    user_n=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
    if user_n<=n_0:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' > {n_0}, riprova:'), "red", ["bold"])
        return check_user_solution()
def new_match(seed):
    TAc.print(LANG.render_feedback("start", f'Consideriamo la successione 1/n, n=1,2,3,... questa successione e\' composta da termini positivi? (y/n)'), "yellow", ["bold"])
    y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
    if y_n=='y':
        TAc.print(LANG.render_feedback("start", f'Converge ad un numero strettamente positivo? (y/n)'), "yellow", ["bold"])
        y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
        if y_n=='y':
            TAc.print(LANG.render_feedback("start", f'Quale? Scrivimelo:'), "yellow", ["bold"])
        else:
            TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
            TAc.print(LANG.render_feedback("start", f'Converge a 0! Sei d\'accordo con me? (y/n)'), "yellow", ["bold"])
            y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
            if y_n=='n':
                n_0=prove_0_convergence()
                TAc.print(LANG.render_feedback("x", f'Proponi un tuo n>{n_0}'), "yellow", ["bold"])
                verify_n(n_0)
    TAc.print(LANG.render_feedback("seed", f'(seed: {seed})'), "yellow", ["bold"])
    x=ll.instance_archimede(seed)
    TAc.print(LANG.render_feedback("proposal", f'La mia proposta per x e\': {x} \ndammi un numero naturale n tale che 1/n < x:'), "yellow", ["bold"])
    check_user_solution(x)

def what_to_do():
    TAc.print(LANG.render_feedback("what-to-do", 'Vuoi fermarti qui, fare un\'altra partita o passare ad un livello successivo? (stop/another_match/next_level)'),  "yellow", ["bold"])
    answer_what_to_do=TALinput(str, regex=f"([a-zA-Z])\w+", sep=None, TAc=TAc)[0]
    if answer_what_to_do=='stop':
        TAc.print(LANG.render_feedback("end", random.choice(ll.end)), "green", ["bold"])
        exit(0)
    elif answer_what_to_do=='another_match':
        counter=0
        seed=random.randint(100000,999999)
        new_match(seed,counter)
        what_to_do()
    else:
        assert answer_what_to_do=='next_level'
        TAc.print(LANG.render_feedback("algorithm", 'Ok! Ecco una proposta per il livello successivo: \nProva a scrivere (qui su terminale o immettendo un file) un algoritmo che, dato x, calcoli per te un valore di n che soddisfi il principio di Archimede:'),  "yellow", ["bold"])

def disprove():
    x=TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0]
    x_eval=eval(x)
    if x_eval<=0:
        TAc.print(LANG.render_feedback("error", f'hai inserito un valore per x non positivo... dammene un altro:'), "red", ["bold"])
        disprove()
    else:
        if x_eval>1:
            return TAc.print(LANG.render_feedback("disprove", f'vedi, per n=1 vale 1/n=1 che e\' < {x}=x.'),  "yellow", ["bold"])
        n=ceil(1/x_eval+0.00000000001)
        n_reciprocal=1/n
        return TAc.print(LANG.render_feedback("disprove", f'vedi, per n= {n} vale 1/n= {n_reciprocal} che e\' < {x}=x.'),  "yellow", ["bold"])

def no_case():
        TAc.print(LANG.render_feedback("disprove", 'Ah no? Proviamo! Inserisci un qualsiasi valore reale x > 0:'),  "yellow", ["bold"])
        disprove()
        TAc.print(LANG.render_feedback("change-idea", f'hai cambiato idea? (y/n)'),  "yellow", ["bold"])
        y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
        if y_n=='y':
            TAc.print(LANG.render_feedback("what-to-do", f'Bene! Vuoi provare a convincermi tu ora, invertendo i ruoli, oppure preferisci salutarmi e fermarti qui? (inverti_ruoli/stop)'),  "yellow", ["bold"])
            answer_what_to_do=TALinput(str, regex=f"([a-zA-Z])\w+", sep=None, TAc=TAc)[0]
            if answer_what_to_do=='stop':
                TAc.print(LANG.render_feedback("end", random.choice(ll.end)), "green", ["bold"])
                exit(0)
            else:
                assert answer_what_to_do=='inverti_ruoli'
                TAc.print(LANG.render_feedback("proof", 'Bene, sei pronto/a a dimostrarmi il principio di Archimede? Cominciamo subito!'), "white")
                counter=0
                new_match(ENV['seed'], counter)
                what_to_do()
        else:
            assert y_n=='n'
            no_case()

TAc.print(LANG.render_feedback("remember", 'REMEMBER - per svolgere questo esercizio ti possono tornare utili le seguenti definizioni: \n- il limite di una successione fn per n->inf e\' finito e vale f se per ogni epsilon > 0 esiste n_0 > 0 naturale tale che n > n_0 => |fn-f| < epsilon \n- per ogni numero reale x > 0 esiste un numero naturale n > 0 tale che 1/n < x (principio di Archimede)'), "white")

TAc.print(LANG.render_feedback("principio-Archimede-curiosity", '\nIl limite di una successione convergente di termini positivi non è sempre strettamente positivo sei d\'accordo con me? (y/n)'), "white")
y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
if y_n=='y':
    TAc.print(LANG.render_feedback("proof", 'Fantastico! Allora non avrai problemi a rispondere a qualche mia domada ;)'), "white")
    new_match(ENV['seed'])
    what_to_do()
else:
    assert y_n=='n'
    no_case()
# for i in range (40):
#     seed=random.randint(100000,999999)
#     print(ll.instance_archimede(seed))