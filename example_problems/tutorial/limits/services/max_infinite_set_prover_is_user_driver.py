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
]
ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')

## START CODING YOUR SERVICE:
seed=ENV["seed"]
TAc.print(LANG.render_feedback("seed", f'# puoi richiamare questa particolare istanza specificando -aseed={ENV["seed"]}'), "yellow")
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
        TAc.print(LANG.render_feedback("instance", f'# come classificheresti la seguente affermazione: il massimo esiste e vale:'),  "yellow", ["bold"])
        min_value=int(min_val[1:]) if min_val[0]=='x' else eval(condition,{'k':int(min_val[1:])})
        propose_type=random.choice(['non_appartiene','appartiene_ma_non_maggiorante','non_appartiene_e_non_maggiorante'])
        # print(f'propose type {propose_type}')
        if propose_type=='non_appartiene':
            propose=ll.not_in_set_parameter(condition,min_value)
        elif propose_type=='appartiene_ma_non_maggiorante':
            propose=ll.appartiene_ma_non_maggiorante(condition,min_value)
        else:
            propose=ll.non_appartiene_e_non_maggiorante(condition,min_value)
        TAc.print(LANG.render_feedback("propose", f'{propose}'),  "yellow", ["reverse"])
        TAc.print(LANG.render_feedback("instance", f'# 1. vera \n# 2. falsa in quanto {propose} non appartiene all\'insieme \n# 3. falsa in quanto {propose} non e` un maggiorante dell\'insieme \n# rispondere 1, 2 o 3 (la risposta corretta potrebbe essere piu` di una):'),  "yellow", ["bold"])
        answer=eval(TALinput(str, regex=f"^\d+$", sep=None, TAc=TAc)[0])
        if not answer in [1,2,3]:
            TAc.print(LANG.render_feedback("instance", f'Mi aspettavo un numero da 1 a 3 come risposta.'),  "red", ["bold"])
            exit(0)
        if answer==1:
            TAc.print(LANG.render_feedback("instance", f'No, non e` vera, ricontrolla e prova a richiamarmi per dare la risposta corretta.'),  "red", ["bold"])
            exit(0)
        elif answer==2:
            if propose_type=='non_appartiene_e_non_maggiorante' or propose_type=='non_appartiene':
                TAc.print(LANG.render_feedback("instance", f'In effetti hai ragione, mi hai convinto!'),  "green", ["bold"])
                exit(0)
            else:
                TAc.print(LANG.render_feedback("instance", f'No, guarda che {propose} appartiene all\'insieme.'),  "red", ["bold"])
                exit(0)
        else:
            TAc.print(LANG.render_feedback("disprove", f'# forniscimi allora un valore appartenente all\'insieme > {propose}:'),  "yellow", ["bold"])
            try:
                answer=eval(TALinput(str, sep=None, TAc=TAc)[0])
            except:
                TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto'),  "red", ["bold"])
                exit(0)
            if answer<propose:
                TAc.print(LANG.render_feedback("error", f'{answer}<{propose}, quindi non mi hai fornito un valore maggiore che appartenga all\'insieme.'),  "red", ["bold"])
                exit(0)
            elif answer<min_value:
                TAc.print(LANG.render_feedback("error", f'{answer} e` troppo piccolo, non appartiene all\'insieme, quindi non hai ancora confutato la mia affermazione.'),  "red", ["bold"])
                exit(0)
            else:
                user_k=(answer-1)/int(condition[0]) if '+' in condition else (answer)/int(condition[0])
                if not user_k.is_integer():
                    TAc.print(LANG.render_feedback("error", f'Vedi, {answer} non appartiene all\'insieme perche` non rispetta la condizione {condition} per qualche k intero... quindi non hai ancora confutato la mia affermazione.'),  "red", ["bold"])
                    exit(0)
                TAc.print(LANG.render_feedback("instance", f'Ben fatto! Mi hai convinto ;)'),  "green", ["bold"])
                exit(0)
    else: # esiste il massimo
        max_value=int(max_val[1:]) if max_val[0]=='x' else eval(condition,{'k':int(max_val[1:])})
        TAc.print(LANG.render_feedback("instance", f'# come classificheresti la seguente affermazione: il massimo esiste e vale:'),  "yellow", ["bold"])
        propose_type=random.choice(['maggiorante','non_appartiene','not_max_but_in_set'])
        # print(f'propose type {propose_type}')
        if propose_type=='maggiorante':
            propose=ll.majorant(max_value)
        elif propose_type=='non_appartiene':
            propose=ll.not_in_set_parameter(condition,max_value)
        else:
            propose=ll.not_max_but_in_set_parameter(condition,max_value)
        TAc.print(LANG.render_feedback("propose", f'{propose}'),  "yellow", ["reverse"])
        TAc.print(LANG.render_feedback("instance", f'# 1. vera \n# 2. falsa in quanto {propose} non appartiene all\'insieme \n# 3. falsa in quanto {propose} non e` un maggiorante dell\'insieme \n# rispondere 1, 2 o 3 (la risposta corretta potrebbe essere piu` di una):'),  "yellow", ["bold"])
        answer=eval(TALinput(str, regex=f"^\d+$", sep=None, TAc=TAc)[0])
        if not answer in [1,2,3]:
            TAc.print(LANG.render_feedback("instance", f'Mi aspettavo un numero da 1 a 3 come risposta.'),  "red", ["bold"])
            exit(0)
        if answer==1:
            TAc.print(LANG.render_feedback("instance", f'No, non e` vera, ricontrolla e prova a richiamarmi per dare la risposta corretta.'),  "red", ["bold"])
            exit(0)
        elif answer==2:
            if propose_type=='maggiorante' or propose_type=='non_appartiene':
                TAc.print(LANG.render_feedback("instance", f'In effetti hai ragione, mi hai convinto!'),  "green", ["bold"])
                exit(0)
            else:
                TAc.print(LANG.render_feedback("instance", f'No, guarda che {propose} appartiene all\'insieme.'),  "red", ["bold"])
                exit(0)
        else:
            if propose_type=='not_max_but_in_set' or propose_type=='non_appartiene':
                TAc.print(LANG.render_feedback("disprove", f'# forniscimi allora un valore appartenente all\'insieme > {propose}:'),  "yellow", ["bold"])
            else:
                TAc.print(LANG.render_feedback("instance", f'No, guarda che {propose} e` un maggiorante dell\'insieme.'),  "red", ["bold"])
                exit(0)
            answer=eval(answer)
            if answer<propose:
                TAc.print(LANG.render_feedback("error", f'{answer} < {propose}, quindi non mi hai fornito un valore maggiore che appartenga all\'insieme.'),  "red", ["bold"])
                exit(0)
            elif answer>max_value:
                TAc.print(LANG.render_feedback("error", f'Beh, nemmeno {answer} appartiene all\'insieme, quindi non mi hai fornito un valore maggiore che appartenga all\'insieme.'),  "red", ["bold"])
                exit(0)
            else:
                user_k=(answer-1)/int(condition[0]) if '+' in condition else (answer)/int(condition[0])
                if not user_k.is_integer():
                    TAc.print(LANG.render_feedback("error", f'Vedi, nemmeno {answer} appartiene all\'insieme perche` non rispetta la condizione {condition} per qualche k intero... quindi non mi hai fornito un valore maggiore che appartenga all\'insieme..'),  "red", ["bold"])
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
    if max_value==None: # non esiste il massimo
        TAc.print(LANG.render_feedback("instance", f'# come classificheresti la seguente affermazione: il massimo esiste e vale:'),  "yellow", ["bold"])
        propose_type=random.choice(['non_appartiene','appartiene_ma_non_maggiorante'])
        # print(f'propose type {propose_type}')
        if propose_type=='non_appartiene':
            propose=ll.not_in_set_without_parameter_min(power,min_value,sup_value)
        elif propose_type=='appartiene_ma_non_maggiorante':
            propose=ll.appartiene_ma_non_maggiorante_without_parameter(power,min_value,sup_value)
        TAc.print(LANG.render_feedback("propose", f'{propose}'),  "yellow", ["reverse"])
        TAc.print(LANG.render_feedback("instance", f'# 1. vera \n# 2. falsa in quanto {propose} non appartiene all\'insieme \n# 3. falsa in quanto {propose} non e` un maggiorante dell\'insieme \n# rispondere 1, 2 o 3 (la risposta corretta potrebbe essere piu` di una):'),  "yellow", ["bold"])
        answer=eval(TALinput(str, regex=f"^\d+$", sep=None, TAc=TAc)[0])
        if not answer in [1,2,3]:
            TAc.print(LANG.render_feedback("instance", f'Mi aspettavo un numero da 1 a 3 come risposta.'),  "red", ["bold"])
            exit(0)
        if answer==1:
            TAc.print(LANG.render_feedback("instance", f'No, non e` vera, ricontrolla e prova a richiamarmi per dare la risposta corretta.'),  "red", ["bold"])
            exit(0)
        elif answer==2:
            if propose_type=='non_appartiene':
                TAc.print(LANG.render_feedback("instance", f'In effetti hai ragione, mi hai convinto!'),  "green", ["bold"])
                exit(0)
            else:
                TAc.print(LANG.render_feedback("instance", f'No, guarda che {propose} appartiene all\'insieme.'),  "red", ["bold"])
                exit(0)
        else:
            TAc.print(LANG.render_feedback("disprove", f'# forniscimi allora un valore appartenente all\'insieme > {propose}:'),  "yellow", ["bold"])
            answer=TALinput(str, sep=None, TAc=TAc)[0]
            try:
                answer=eval(answer)
            except:
                TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto'),  "red", ["bold"])
                exit(0)
            if answer<propose:
                TAc.print(LANG.render_feedback("error", f'{answer}<{propose}, quindi non hai ancora confutato la mia affermazione.'),  "red", ["bold"])
                exit(0)
            user_max_comparison=abs(answer) if power==2 else answer
            # print('answer ', answer, '   sup ',sup)
            if user_max_comparison==sup_value or user_max_comparison>sup_value or ((user_max_comparison<min_value) if min_value!=None else None):
                TAc.print(LANG.render_feedback("error", f'Vedi, {answer} non appartiene all\'insieme, quindi non hai ancora confutato la mia affermazione.'),  "red", ["bold"])
                exit(0)
            TAc.print(LANG.render_feedback("instance", f'Ben fatto! Mi hai convinto ;)'),  "green", ["bold"])
            exit(0)
    else: # eiste il massimo
        TAc.print(LANG.render_feedback("instance", f'# come classificheresti la seguente affermazione: il massimo esiste e vale:'),  "yellow", ["bold"])
        propose_type=random.choice(['non_appartiene','appartiene_ma_non_maggiorante'])
        # print(f'propose type {propose_type}')
        if propose_type=='appartiene_ma_non_maggiorante':
            propose=ll.appartiene_ma_non_maggiorante_without_parameter(power,min_value,sup_value)
        else:
            propose=ll.not_in_set_without_parameter_max(power,min_value,sup_value)
        TAc.print(LANG.render_feedback("propose", f'{propose}'),  "yellow", ["reverse"])
        TAc.print(LANG.render_feedback("instance", f'# 1. vera \n# 2. falsa in quanto {propose} non appartiene all\'insieme \n# 3. falsa in quanto {propose} non e` un maggiorante dell\'insieme \n# rispondere 1, 2 o 3 (la risposta corretta potrebbe essere piu` di una):'),  "yellow", ["bold"])
        answer=eval(TALinput(str, regex=f"^\d+$", sep=None, TAc=TAc)[0])
        if not answer in [1,2,3]:
            TAc.print(LANG.render_feedback("instance", f'Mi aspettavo un numero da 1 a 3 come risposta.'),  "red", ["bold"])
            exit(0)
        if answer==1:
            TAc.print(LANG.render_feedback("instance", f'No, non e` vera, ricontrolla e prova a richiamarmi per dare la risposta corretta.'),  "red", ["bold"])
            exit(0)
        elif answer==2:
            if propose_type=='non_appartiene':
                TAc.print(LANG.render_feedback("instance", f'In effetti hai ragione, mi hai convinto!'),  "green", ["bold"])
                exit(0)
            else:
                TAc.print(LANG.render_feedback("instance", f'No, guarda che {propose} appartiene all\'insieme.'),  "red", ["bold"])
                exit(0)
        else:
            TAc.print(LANG.render_feedback("disprove", f'# forniscimi allora un valore appartenente all\'insieme > {propose}:'),  "yellow", ["bold"])
            answer=TALinput(str, sep=None, TAc=TAc)[0]
            try:
                answer=eval(answer)
            except:
                TAc.print(LANG.render_feedback("error", f'non riesco a decifrare cos\'hai scritto'),  "red", ["bold"])
                exit(0)
            if answer<propose:
                TAc.print(LANG.render_feedback("error", f'{answer}<{propose}, quindi non mi hai smentito.'),  "red", ["bold"])
                exit(0)
            user_max_comparison=abs(answer) if power==2 else answer
            if (min_value!=None and user_max_comparison<min_value) or user_max_comparison>max_value:
                if power!=1:
                    TAc.print(LANG.render_feedback("error", f'Vedi, {answer} non appartiene all\'insieme (perche` {answer}^{power}={answer**power}), quindi non mi hai fornito un valore maggiore che appartenga all\'insieme.'),  "red", ["bold"])
                    exit(0)
                else:
                    TAc.print(LANG.render_feedback("error", f'Vedi, {answer} non appartiene all\'insieme, quindi non mi hai fornito un valore maggiore che appartenga all\'insieme.'),  "red", ["bold"])
                    exit(0)
            TAc.print(LANG.render_feedback("instance", f'Ben fatto! Mi hai convinto ;)'),  "green", ["bold"])
            exit(0)
