#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
from math import *
from numpy import inf
import limiti_lib as ll
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
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
output_filename = f"instance_{ENV['seed']}_inf_set.txt"
seed=ENV["seed"]
TAc.print(LANG.render_feedback("seed", f'# puoi richiamare questa particolare istanza specificando -aseed= {ENV["seed"]}'), "yellow")
parameter,instance, arg_1, arg_2=ll.instance_inf_set(seed)
TAc.print(LANG.render_feedback("instance", f'# Dato l\'insieme \n{instance} \n# determina il massimo (se credi che non lo abbia scrivi "None"):'),  "yellow", ["bold"])
user_max=TALinput(str, regex=f"^(none|None)$|^([+-]?[.\d]*)$", sep=None, TAc=TAc)[0]
user_max=eval(user_max) if user_max!='none' else 'none'
# CASO CON PARAMETRO k
if parameter=='parameter':
    condition=arg_1
    min=arg_2[0]
    max=arg_2[1]
    if max==None: # non esiste il massimo
        if user_max=='none' or user_max==None:
            TAc.print(LANG.render_feedback("correct", f'Sono d\'accordo!'), "green", ["bold"])
            TAc.print(LANG.render_feedback("other-service", f'Se ora vuoi provare a convincermi chiama il servizio `rtal connect limiti max_infinite_set_prover`.'), "white")
        else:
            min_comparison=int(min[1:]) if min[0]=='x' else eval(condition,{'k':int(min[1:])})
            if user_max<min_comparison:
                TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} e` troppo piccolo, non appartiene all\'insieme, quindi non puo\' essere il massimo.'),  "red", ["bold"])
            else:
                user_k=(user_max-1)/int(condition[0]) if '+' in condition else (user_max)/int(condition[0])
                if not user_k.is_integer():
                    TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} non appartiene all\'insieme perche` non rispetta la condizione {condition} per qualche k intero... quindi non puo\' essere il massimo'),  "red", ["bold"])
                else:
                    x_proposal=int(eval(condition, {'k':user_k+random.randint(1,3)}))
                    TAc.print(LANG.render_feedback("error", f'Vedi, {x_proposal} > {user_max}, e {x_proposal} e` nell\'insieme, quindi {user_max} non puo\' essere il massimo'),  "red", ["bold"])
            TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
            exit(0)
    else: # esiste il massimo
        max_value=int(max[1:]) if max[0]=='x' else eval(condition,{'k':int(max[1:])})
        # print(max_value)
        if user_max=='none' or user_max==None:
            TAc.print(LANG.render_feedback("error", f'Invece il massimo c\'e` e vale {max_value}.'),  "red", ["bold"])
            TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
            exit(0)
        else:
            if user_max==max_value:
                TAc.print(LANG.render_feedback("correct", f'Sono d\'accordo!'), "green", ["bold"])
                TAc.print(LANG.render_feedback("other-service", f'Se ora vuoi provare a convincermi chiama il servizio `rtal connect limiti max_infinite_set_prover`.'), "white")
                exit(0)
            else:
                if user_max>max_value:
                    TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} e` troppo grande, non appartiene all\'insieme, quindi non puo\' essere il massimo.'),  "red", ["bold"])
                else:
                    user_k=(user_max-1)/int(condition[0]) if '+' in condition else (user_max)/int(condition[0])
                    if not user_k.is_integer():
                        TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} non appartiene all\'insieme perche` non rispetta la condizione {condition} per qualche k intero... quindi non puo\' essere il massimo'),  "red", ["bold"])
                    else:
                        x_proposal=int(eval(condition, {'k':user_k+1}))
                        TAc.print(LANG.render_feedback("error", f'Vedi, {x_proposal} > {user_max}, e {x_proposal} e` nell\'insieme, quindi {user_max} non puo\' essere il massimo'),  "red", ["bold"])
                TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
                exit(0)
else: # CASO SENZA PARAMETRO k
    power=int(parameter[17])
    # print(f'power {power}')
    max_value=arg_1
    inf_sup=arg_2
    if isinstance(inf_sup,list):
        min=inf_sup[0]
        sup=inf_sup[1]
    else:
        sup=inf_sup
        min=None
    if sup==inf: # l'insieme non è limitato superiormente
        if user_max=='none' or user_max==None:
            TAc.print(LANG.render_feedback("correct", f'Sono d\'accordo!'), "green", ["bold"])
            TAc.print(LANG.render_feedback("other-service", f'Se ora vuoi provare a convincermi chiama il servizio `rtal connect limiti max_infinite_set_prover`.'), "white")
            exit(0)
        else:
            TAc.print(LANG.render_feedback("error", f'No, questo insieme non ammette massimo.'),  "red", ["bold"])
            TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
            exit(0)
    else: # l'insieme è limitato superiormente
        if max_value==None: # non esiste il massimo
            if user_max=='none' or user_max==None: # l'utente risponde giusto
                TAc.print(LANG.render_feedback("correct", f'Sono d\'accordo! Per questo insieme non esiste il massimo.'), "green", ["bold"])
                TAc.print(LANG.render_feedback("other-service", f'Se ora vuoi provare a convincermi chiama il servizio `rtal connect limiti max_infinite_set_prover`.'), "white")
                exit(0)
            else: # l'utente inserisce un numero
                user_max_comparison=abs(user_max) if power==2 else user_max
                # print('user_max ', user_max, '   sup ',sup)
                if user_max_comparison==sup or user_max_comparison>sup or ((user_max_comparison<min) if min!=None else None):
                    TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} non appartiene all\'insieme, quindi non puo\' essere il massimo.'),  "red", ["bold"])
                elif user_max_comparison<sup:
                    x_proposal=(user_max+sup)/2
                    TAc.print(LANG.render_feedback("error", f'Vedi, {x_proposal} > {user_max}, e {x_proposal} e` nell\'insieme... quindi {user_max} non puo\' essere il massimo.'),  "red", ["bold"])
                TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
                exit(0)
        else: # eiste il massimo
            if user_max=='none' or user_max==None: # l'utente dice che non esiste il massimo
                TAc.print(LANG.render_feedback("error", f'Invece il massimo c\'e` e vale {max_value}.'),  "red", ["bold"])
                TAc.print(LANG.render_feedback("other-service", f'Se ora ti sei convinto dell\' esistenza del massimo e vuoi provare a dimostrarmelo chiama il servizio `rtal connect limiti max_infinite_set_prover`.'), "white")  
                exit(0)
            else:
                # print(f'min {min}, user max {user_max}, max {max}')
                if user_max==max_value:
                    TAc.print(LANG.render_feedback("correct", f'Sono d\'accordo!'), "green", ["bold"])
                    TAc.print(LANG.render_feedback("other-service", f'Se ora vuoi provare a convincermi chiama il servizio `rtal connect limiti max_infinite_set_prover`.'), "white")
                    exit(0)
                else:
                    user_max_comparison=abs(user_max) if power==2 else user_max
                    if (min!=None and user_max_comparison<min) or user_max_comparison>max_value:
                        if power!=1:
                            TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} non appartiene all\'insieme (perche` {user_max}^{power}={user_max**power}), quindi non puo\' essere il massimo.'),  "red", ["bold"])
                        else:
                            TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} non appartiene all\'insieme, quindi non puo\' essere il massimo.'),  "red", ["bold"])
                    else:
                        x_proposal=(user_max-min)/2 if power==2 and user_max<0 else (user_max_comparison+max_value)/2
                        TAc.print(LANG.render_feedback("error", f'Vedi, {x_proposal} > {user_max}, e {x_proposal} e` nell\'insieme... quindi {user_max} non puo\' essere il massimo.'),  "red", ["bold"])
                    TAc.print(LANG.render_feedback("other-service", f'Prova a richiamarmi utilizzando il flag relativo al seed per rispondere nel modo corretto.'), "white")
                    exit(0)
exit(0)