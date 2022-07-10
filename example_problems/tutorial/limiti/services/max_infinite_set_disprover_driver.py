#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
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

## START CODING YOUR SERVICE:
seed=ENV["seed"]
TAc.print(LANG.render_feedback("seed", f'seed: {seed}'), "yellow", ["bold"])
parameter,instance,arg_1,arg_2=ll.instance_inf_set(seed)
TAc.print(LANG.render_feedback("instance", f'# Dato l\'insieme \n{instance}'),  "yellow", ["bold"])
# for i in range (20):
#     seed=random.randint(100000,999999)
#     parameter,instance, arg_1, arg_2=ll.instance_inf_set(seed)
#     # condition=arg_1
#     # min_value=arg_2[0]
#     # max_value=arg_2[1]
#     power=int(parameter[17])
#     # print(f'power {power}')
#     max_value=arg_1
#     inf_sup=arg_2
#     if isinstance(inf_sup,list):
#         min_value=inf_sup[0]
#         sup_value=inf_sup[1]
#     else:
#         sup_value=inf_sup
#         min_value=None
#     print(instance, min_value, max_value,sup_value)
if parameter=='parameter':
    condition=arg_1
    min_val=arg_2[0]
    max_val=arg_2[1]
    if max_val==None: # non esiste il massimo
        TAc.print(LANG.render_feedback("instance", f'# riusciresti a convincermi che non ha massimo? Secondo me ce l\'ha e vale'),  "yellow", ["bold"])
        min_value=int(min_val[1:]) if min_val[0]=='x' else eval(condition,{'k':int(min_val[1:])})
        propose=ll.majorant(min_value)
        TAc.print(LANG.render_feedback("propose", f'{propose}'),  "yellow", ["reverse"])
        TAc.print(LANG.render_feedback("instance", f'# Se pensi che nell\'insieme esista un numero maggiore del mio prova a scriverlo:'),  "yellow", ["bold"])
        answer=eval(TALinput(str, regex=f"^([+-]?[.\d]*)$", sep=None, TAc=TAc)[0])
        if answer<min_value:
            TAc.print(LANG.render_feedback("error", f'{answer} e` troppo piccolo, non appartiene all\'insieme, quindi non mi hai ancora smentito.'),  "red", ["bold"])
            exit(0)
        elif answer<propose:
            TAc.print(LANG.render_feedback("error", f'{answer}<{propose}, quindi non mi hai ancora smentito.'),  "red", ["bold"])
            exit(0)
        else:
            user_k=(answer-1)/int(condition[0]) if '+' in condition else (answer)/int(condition[0])
            if not user_k.is_integer():
                TAc.print(LANG.render_feedback("error", f'Vedi, {answer} non appartiene all\'insieme perche` non rispetta la condizione {condition} per qualche k intero... quindi non mi hai ancora smentito.'),  "red", ["bold"])
                exit(0)
        TAc.print(LANG.render_feedback("instance", f'Ben fatto! Mi hai convinto ;)'),  "green", ["bold"])
        exit(0)
    else: # esiste il massimo
        max_value=int(max_val[1:]) if max_val[0]=='x' else eval(condition,{'k':int(max_val[1:])})
        TAc.print(LANG.render_feedback("instance", f'# convincimi che il massimo esiste \n# Il numero che ti propongo e`:'),  "yellow", ["bold"])
        propose_type=random.choice(['maggiorante','non_appartiene','not_max_but_in_set'])
        if propose_type=='maggiorante':
            propose=ll.majorant(max_value)
        elif propose_type=='non_appartiene':
            propose=ll.not_in_set_parameter(condition,max_value)
        else:
            propose=ll.not_max_but_in_set_parameter(condition,max_value)
        TAc.print(LANG.render_feedback("propose", f'{propose}'),  "yellow", ["reverse"])
        TAc.print(LANG.render_feedback("instance", f'# prova a smentirmi dicendomi se \n- e` un maggiorante \n- non e` un maggiorante e non appartiene all\'insieme \n- appartiene all\'insieme ma non e` il massimo (in tal caso proponimi tu un numero maggiore appartenente all\'insieme) \nOpzioni di risposta: "maggiorante"/"non_appartiene"/ un numero intero'),  "yellow", ["bold"])
        answer=TALinput(str, regex=f"^(maggiorante|non_appartiene)$|^([+-]?[.\d]*)$", sep=None, TAc=TAc)[0]
        if (propose_type=='maggiorante' and answer==propose_type) or (propose_type=='non_appartiene' and answer==propose_type):
            TAc.print(LANG.render_feedback("instance", f'Ben fatto! Mi hai convinto ;)'),  "green", ["bold"])
            exit(0)
        elif propose_type!='maggiorante' and answer=='maggiorante':
            TAc.print(LANG.render_feedback("instance", f'Vedi, {propose} non e` un maggiorante e quindi non mi hai smentito'),  "red", ["bold"])
            exit(0)
        elif propose_type!='non_appartiene' and answer=='non_appartiene' and propose_type!='maggiorante':
            TAc.print(LANG.render_feedback("instance", f'Vedi, {propose} appartiene all\'insieme, quindi non mi hai smentito'),  "red", ["bold"])
            exit(0)
        else:
            answer=eval(answer)
            if answer>max_value:
                TAc.print(LANG.render_feedback("error", f'Beh, nemmeno {answer} appartiene all\'insieme, quindi non mi hai ancora smentito.'),  "red", ["bold"])
                exit(0)
            else:
                user_k=(answer-1)/int(condition[0]) if '+' in condition else (answer)/int(condition[0])
                if not user_k.is_integer():
                    TAc.print(LANG.render_feedback("error", f'Vedi, nemmeno {answer} appartiene all\'insieme perche` non rispetta la condizione {condition} per qualche k intero... quindi non mi hai ancora smentito.'),  "red", ["bold"])
                    exit(0)
            TAc.print(LANG.render_feedback("instance", f'Ben fatto! Mi hai convinto ;)'),  "green", ["bold"])
            exit(0)
else: # CASO SENZA PARAMETRO k
    power=int(parameter[17])
    # print(f'power {power}')
    max_value=arg_1
    inf_sup=arg_2
    if isinstance(inf_sup,list):
        min_value=inf_sup[0]
        sup_value=inf_sup[1]
    else:
        sup_value=inf_sup
        min_value=None
    propose=ll.propose_without_parameter_inf_set(power,min_value,sup_value)
    if max_value==None: # non esiste il massimo
        TAc.print(LANG.render_feedback("instance", f'# provero` a dimostrarti che il massimo non esiste.'),  "yellow", ["bold"])
        TAc.print(LANG.render_feedback("max", f'prova a darmi un maggiorante per questo insieme:'),  "yellow", ["bold"])
        user_max=eval(TALinput(str, sep=None, TAc=TAc)[0])
        try:
            user_max=eval(user_max)
        except:
            TAc.print(LANG.render_feedback("error", f'non riesco a decifrare quello che hai scritto'),  "red", ["bold"])
            exit(0)
        if min_value !=None and power==2:
            min_comparison = eval(min_value[1:])
            user_max_comparison=abs(user_max)
            # print(min, user_max_comparison)
        else:
            user_max_comparison=user_max
            min_comparison=min_value
        # print('user_max ', user_max, '   sup ',sup)
        if user_max_comparison==sup or user_max_comparison>sup or ((user_max_comparison<min_comparison) if min_comparison!=None else None):
            TAc.print(LANG.render_feedback("max", f'vedi, {user_max} non appartiene all\'insieme, quindi non puo\' essere un massimo'),  "red", ["bold"])
        elif user_max_comparison<sup:
            if sup!=inf:
                TAc.print(LANG.render_feedback("max", f'vedi, {(user_max+sup)/2} e\' maggiore del tuo {user_max} ma e\' nell\'insieme, quindi {user_max} non puo\' essere un massimo'),  "red", ["bold"])
            else:
                TAc.print(LANG.render_feedback("max", f'vedi, {abs(user_max)+random.randint(1,10)} e\' maggiore del tuo {user_max} ma e\' nell\'insieme, quindi non puo\' essere un massimo'),  "red", ["bold"])

    else: # eiste il massimo
        TAc.print(LANG.render_feedback("instance", f'# convincimi che il massimo esiste \n# Il numero che ti propongo per il massimo e`:'),  "yellow", ["bold"])
        propose_type=random.choice(['maggiorante','not_max_but_in_set'])
        if propose_type=='maggiorante':
            propose=ll.majorant(max_value)
        else:
            propose=ll.propose_without_parameter_inf_set(power,min_value,sup_value)
        TAc.print(LANG.render_feedback("propose", f'{propose}'),  "yellow", ["reverse"])
        TAc.print(LANG.render_feedback("instance", f'# prova a smentirmi dicendomi se \n- e` un maggiorante \n- appartiene all\'insieme ma non e` il massimo (in tal caso proponimi tu un numero maggiore appartenente all\'insieme) \nOpzioni di risposta: "maggiorante" / un numero'),  "yellow", ["bold"])
        answer=TALinput(str, regex=f"^(maggiorante)|([+-]?[.\d]*)$", sep=None, TAc=TAc)[0]
        if propose_type=='maggiorante' and answer==propose_type:
            TAc.print(LANG.render_feedback("instance", f'Ben fatto! Mi hai convinto ;)'),  "green", ["bold"])
            exit(0)
        elif propose_type=='maggiorante' and answer!='maggiorante':
            TAc.print(LANG.render_feedback("instance", f'Vedi, {propose} appartiene all\'insieme, quindi non e` un maggiorante e non mi hai smentito'),  "red", ["bold"])
            exit(0)
        else:
            try:
                answer=eval(answer)
            except:
                TAc.print(LANG.render_feedback("instance", f'Vedi, {propose} appartiene all\'insieme, quindi non e` un maggiorante e non mi hai smentito'),  "red", ["bold"])
                exit(0)
            if answer<propose:
                TAc.print(LANG.render_feedback("error", f'{answer}<{propose}, quindi non mi hai smentito.'),  "red", ["bold"])
                exit(0)
            user_max_comparison=abs(answer) if power==2 else answer
            if (min_value!=None and user_max_comparison<min_value) or user_max_comparison>max_value:
                if power!=1:
                    TAc.print(LANG.render_feedback("error", f'Vedi, {answer} non appartiene all\'insieme (perche` {answer}^{power}={answer**power}), quindi non mi hai smentito.'),  "red", ["bold"])
                    exit(0)
                else:
                    TAc.print(LANG.render_feedback("error", f'Vedi, {answer} non appartiene all\'insieme, quindi non mi hai smentito.'),  "red", ["bold"])
                    exit(0)
            TAc.print(LANG.render_feedback("instance", f'Ben fatto! Mi hai convinto ;)'),  "green", ["bold"])
            exit(0)
