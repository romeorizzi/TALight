#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
import limiti_lib as ll
import random
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
def check_user_solution(x):
    user_sol=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
    if user_sol<=0 or int(user_sol)!=user_sol:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' naturale positivo, riprova:'), "red", ["bold"])
        return check_user_solution(x)
    proof=1/user_sol
    if not proof<eval(str(x)):
        error_answer=random.choice([f'no, 1/{user_sol} = {round(proof,5)} e come noterai {round(proof,5)} >= {x}=y-x, riprova:', f'mmm ho paura che tu abbia sbagliato, infatti 1/{user_sol} = {round(proof,5)} e come noterai {round(proof,5)} >= {x}=y-x, ritenta:'])
        TAc.print(LANG.render_feedback("error", error_answer), "red", ["bold"])
        return check_user_solution(x)
    assert proof<eval(str(x))
    TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
    return user_sol

def check_int_in_interval(nx,ny):
    user_int=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
    if int(user_int)!=user_int:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' intero, riprova:'), "red", ["bold"])
        return check_int_in_interval(nx,ny)
    if user_int<nx:
        TAc.print(LANG.render_feedback("error", f'guarda che {user_int}<{nx}, riprova:'), "red", ["bold"])
        return check_int_in_interval(nx,ny)
    if user_int>ny:
        TAc.print(LANG.render_feedback("error", f'guarda che {user_int}>{ny}, ritenta:'), "red", ["bold"])
        return check_int_in_interval(nx,ny)
    TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
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
        TAc.print(LANG.render_feedback("error", f'mmmm ci sei quasi! il numero razionale che hai inserito e\' compreso tra x ed y ma puoi fare di meglio: utilizza una relazione tra l\'intero che hai scelto (ovvero {user_int}) ed n={n} per creare un intero della forma \'a/b\', riprova:'), "yellow", ["bold"])
        return check_q(x,y,n,user_int)
    return TAc.print(LANG.render_feedback("correct", f'Ben fatto! Abbiamo trovato la q che cercavamo, infatti {q} = {eval(q)} e\' compresa tra x={x} ed y={y}.'), "green", ["bold"])

def new_match(seed):
    TAc.print(LANG.render_feedback("seed", f'(seed: {seed})'), "yellow", ["bold"])
    x,y=ll.instance_density(seed)
    # print('y-x ',y-x)
    TAc.print(LANG.render_feedback("proposal", f'Le mie proposte sono:'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("proposal", f'x={x} \ny={y} '), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("proposal", f'scrivi un numero naturale n > 0 che soddisfi il principio di Archimede (con argomento y-x): \n(se non ricordi questo principio ti consiglio l\'esercizio -> rtal connect limiti archimede_prover)'), "yellow", ["bold"])
    n=check_user_solution(y-x)
    nx=n*x
    ny=n*y
    TAc.print(LANG.render_feedback("next-step", f'Nota ora che {n}*x vale {nx} e {n}*y vale {ny} \ndimmi un intero in ({nx} , {ny}):'), "yellow", ["bold"])
    user_int=check_int_in_interval(nx,ny)
    TAc.print(LANG.render_feedback("next-step", f'Utilizzando questo intero e la n che mi hai proposto prima, riusciresti a trovare un numero razionale (nella forma a/b) compreso tra x={x} e y={y}? scrivilo:'), "yellow", ["bold"])
    check_q(x,y,n,user_int)

def what_to_do():
    TAc.print(LANG.render_feedback("what-to-do", 'Vuoi fermarti qui, fare un\'altra partita o passare ad un livello successivo? (stop/nuova_partita/livello_successivo)'),  "yellow", ["bold"])
    answer_what_to_do=TALinput(str, regex=f"([a-zA-Z])\w+", sep=None, TAc=TAc)[0]
    if answer_what_to_do=='stop':
        TAc.print(LANG.render_feedback("end", random.choice(ll.end)), "green", ["bold"])
        exit(0)
    elif answer_what_to_do=='nuova_partita':
        seed=random.randint(100000,999999)
        new_match(seed)
        what_to_do()
    else:
        assert answer_what_to_do=='livello_successivo'
        TAc.print(LANG.render_feedback("algorithm", 'Ok! Ecco una proposta per il livello successivo: \nProva a scrivere (qui su terminale o immettendo un file) un algoritmo che dati x e y trovi q seguendo la traccia di quello che abbiamo appena dimostrato insieme: se ci riuscirai avrai dimostrato la densita\' di Q in R! ;)'),  "yellow", ["bold"])

def disprove():
    TAc.print(LANG.render_feedback("disprove", 'inserisci un qualsiasi valore reale x:'),  "yellow", ["bold"])
    user_x=TALinput(str, regex=f"^(\S)+$", sep=None, TAc=TAc)[0]
    x_eval=eval(user_x)
    TAc.print(LANG.render_feedback("disprove", 'inserisci un valore reale y tale che x<y:'),  "yellow", ["bold"])
    user_y=TALinput(str, regex=f"^(\S)+$", sep=None, TAc=TAc)[0]
    y_eval=eval(user_y)
    print(x_eval, y_eval)
    if x_eval<0 and 0<y_eval:
        return TAc.print(LANG.render_feedback("disprove", f'vedi, per q=0 si ha che x={user_x} < 0 < {user_y}=y'),  "yellow", ["bold"])
    if not x_eval<y_eval:
        TAc.print(LANG.render_feedback("error", f'hai inserito un valore per y<=x e io te ne avevo chiesto uno maggiore... ricominciamo:'), "red", ["bold"])	
        return disprove()
    n=ceil(1/(y_eval-x_eval)+0.00000000001)
    integer=ceil(n*x_eval+0.00000000001)
    print('n ',n,'integer ',integer)
    assert integer < n*y_eval
    q=integer/n
    print(q)
    assert x_eval<q and q<y_eval
    return TAc.print(LANG.render_feedback("disprove", f'vedi, per q={integer}/{n}={q} si ha che x={user_x} < {q} < {user_y}=y'),  "yellow", ["bold"])

def no_case():
        TAc.print(LANG.render_feedback("disprove", 'Oh ok, proviamo a vedere se la tua intuizione e\' giusta: '),  "yellow", ["bold"])
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
                new_match(ENV['seed'])
                what_to_do()
        else:
            assert y_n=='n'
            no_case()

TAc.print(LANG.render_feedback("enunciato", '\nSaresti propenso/a a credere che dati x,y due numeri reali, x < y , esiste q razionale tale che  x < q < y ? (y/n)'), "white")
y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
if y_n=='y':
    TAc.print(LANG.render_feedback("proof", 'Bene, sei pronto/a a dimostrarmi la densita\' di Q in R? Cominciamo subito!'), "yellow", ["bold"])
    new_match(ENV['seed'])
    what_to_do()
else:
    assert y_n=='n'
    no_case()
    exit(0)

# for i in range(20):
#     seed=random.randint(100000,999999)
#     x,y=ll.instance_density(seed)
#     print(x, y, y-x,'\n')
# exit(0)