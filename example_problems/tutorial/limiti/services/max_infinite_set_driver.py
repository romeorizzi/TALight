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
    # ('source',str),
    # ('instance_id',int),
    ('seed',int),
    ('download',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
# TAc.print(LANG.render_feedback("start", 'Per risolvere l\'esercizio ti potrebbero tornare utili i seguenti concetti: \n1) Se un insieme non e` finito potrebbe non ammettere massimo. \n2) Un insieme limitato (superiormente/inferiormente/entrambi) non sempre ammette massimo.\n3) Un numero k in X (dove X e` un insieme totalmente ordinato) e` un maggiorante di Y, Y sottoinsieme di X, se k >= x per ogni x in Y. \n4) L\'estremo superiore di Y e` il minimo dei maggioranti. \n5) Ogni sottoinsieme Y di X non vuoto e limitato superiormente possiede estremo superiore.'), "white")
# if ENV["source"]!='catalogue':
#     assert ENV["source"]=='randgen'
#     output_filename = f"instance_{ENV['seed']}_inf_set.txt"
#     seed=ENV["seed"]
#     TAc.print(LANG.render_feedback("seed", f'seed: {seed}'), "yellow", ["bold"])
# else:
#     input = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension='txt')
#     instance=input.split('\n')[0]
#     seed=int(input.split('\n')[1])
#     output_filename = f"instance_catalogue_{ENV['instance_id']}_inf_set.txt"
#     TAc.print(LANG.render_feedback("seed", f'instance_id: {ENV["instance_id"]}'), "yellow", ["bold"])
output_filename = f"instance_{ENV['seed']}_inf_set.txt"
seed=ENV["seed"]
TAc.print(LANG.render_feedback("seed", f'seed: {seed}'), "yellow", ["bold"])
contatore=0 # mi serve per generare numeri casuali in modo indipendente dal seed (nel caso di "insieme limitato ma il ragazzo dice di no")
parameter,instance, arg_1, arg_2=ll.instance_inf_set(seed)
TAc.print(LANG.render_feedback("instance", f'# Dato l\'insieme \n{instance} \n# determina il massimo (se credi che non lo abbia scrivi "None"):'),  "yellow", ["bold"])
user_max=TALinput(str, regex=f"^(none|None)$|^([+-]?[.\d]*)$", sep=None, TAc=TAc)[0]
user_max=eval(user_max) if user_max!='none' else 'none'
# CASO CON PARAMETRO k
if parameter=='parameter':
    condition=arg_1
    min=arg_2
    # print('condition: ',condition,'- min: ',min)
    if user_max=='none' or user_max==None:
        TAc.print(LANG.render_feedback("correct", f'Ottimo! Questo insieme e` illimitato superiormente quindi non ha massimo.'), "green", ["bold"])
    else:
        min_comparison=int(min[1:]) if min[0]=='x' else eval(condition,{'k':int(min[1:])})
        if user_max<min_comparison:
            TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} e` troppo piccolo, non appartiene all\'insieme, quindi non puo\' essere il massimo.'),  "red", ["bold"])
            exit(0)
        else:
            user_k=(user_max-1)/int(condition[0]) if '+' in condition else (user_max)/int(condition[0])
            if not user_k.is_integer():
                TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} non appartiene all\'insieme perche` non rispetta la condizione {condition} per qualche k naturale... quindi non puo\' essere il massimo'),  "red", ["bold"])
                exit(0)
            else:
                x_proposal=int(eval(condition, {'k':user_k+random.randint(1,3)}))
                TAc.print(LANG.render_feedback("error", f'Vedi, {x_proposal} > {user_max}, e {x_proposal} e` nell\'insieme, quindi {user_max} non puo\' essere il massimo'),  "red", ["bold"])
                exit(0)
else: # CASO SENZA PARAMETRO k
    power=int(parameter[17])
    # print(f'power {power}')
    max=arg_1
    inf_sup=arg_2
    if isinstance(inf_sup,list):
        min=inf_sup[0]
        sup=inf_sup[1]
    else:
        sup=inf_sup
        min=None
    if sup==inf: # l'insieme non è limitato superiormente
        if user_max=='none' or user_max==None:
            TAc.print(LANG.render_feedback("correct", f'Ottimo! Infatti questo insieme e` illimitato superiormente, quindi non ha massimo.'), "green", ["bold"])
            exit(0)
        else:
            TAc.print(LANG.render_feedback("error", f'No, questo insieme e` illimitato superiormente... quindi non ammette massimo.'),  "red", ["bold"])
            exit(0)
    else: # l'insieme è limitato superiormente
        if max==None: # non esiste il massimo
            if user_max=='none' or user_max==None: # l'utente risponde giusto
                TAc.print(LANG.render_feedback("correct", f'Ottimo! Questo insieme e` limitato superiormente, ma {sup} non e` compreso nell\'insieme, quindi non esiste il massimo.'), "green", ["bold"])
                exit(0)
            else: # l'utente inserisce un numero
                user_max_comparison=abs(user_max) if power==2 else user_max
                # print('user_max ', user_max, '   sup ',sup)
                if user_max_comparison==sup or user_max_comparison>sup or ((user_max_comparison<min) if min!=None else None):
                    TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} non appartiene all\'insieme, quindi non puo\' essere il massimo.'),  "red", ["bold"])
                    exit(0)
                elif user_max_comparison<sup:
                    x_proposal=(user_max+sup)/2
                    TAc.print(LANG.render_feedback("error", f'Vedi, {x_proposal} > {user_max}, e {x_proposal} e` nell\'insieme... quindi {user_max} non puo\' essere il massimo.'),  "red", ["bold"])
                    exit(0)
        else: # eiste il massimo
            if user_max=='none' or user_max==None: # l'utente dice che non esiste il massimo
                TAc.print(LANG.render_feedback("error", f'Vedi, il massimo per questo insieme e` {max}, infatti: \n1) {max} appartiene all\'insieme, \n2) non esistono altri numeri maggiori di lui'),  "red", ["bold"])
                exit(0)
            else:
                # print(f'min {min}, user max {user_max}, max {max}')
                if user_max==max:
                    TAc.print(LANG.render_feedback("correct", f'Ottimo! Confermo che {max} e` il massimo, infatti: \n1) {max} appartiene all\'insieme \n2) non ci sono altri numeri maggiori di lui.'), "green", ["bold"])
                    exit(0)
                else:
                    user_max_comparison=abs(user_max) if power==2 else user_max
                    if (min!=None and user_max_comparison<min) or user_max_comparison>max:
                        if power!=1:
                            TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} non appartiene all\'insieme (perche` {user_max}^{power}={user_max**power}), quindi non puo\' essere il massimo.'),  "red", ["bold"])
                        else:
                            TAc.print(LANG.render_feedback("error", f'Vedi, {user_max} non appartiene all\'insieme, quindi non puo\' essere il massimo.'),  "red", ["bold"])
                        exit(0)
                    else:
                        x_proposal=(user_max-min)/2 if power==2 and user_max<0 else (user_max_comparison+max)/2
                        TAc.print(LANG.render_feedback("error", f'Vedi, {x_proposal} > {user_max}, e {x_proposal} e` nell\'insieme... quindi {user_max} non puo\' essere il massimo.'),  "red", ["bold"])
                        exit(0)

if ENV["download"]:
    output=instance+'\n'+str(seed)
    TALf.str2output_file(output,output_filename)
exit(0)