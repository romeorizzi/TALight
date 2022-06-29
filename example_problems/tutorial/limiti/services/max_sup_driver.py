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
    ('source',str),
    ('instance_id',int),
    ('seed',int),
    ('download',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
# FUNZIONI
def existence_but_not_correctness_max(max): # il massimo inserito dal ragazzo non è esatto
    user_max=eval(TALinput(str, regex=f"^[-+]?[0-9](.)*$", sep=None, TAc=TAc)[0])
    # print(user_max,max)
    if user_max==max:
        return TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("wrong", random.choice(ll.wrong)), "red", ["bold"])
        existence_but_not_correctness_max(max)

def non_existence_max(sup,min): # il ragazzo afferma che ci sia un massimo ma in realtà non esiste
    TAc.print(LANG.render_feedback("max", f'ah si? scrivimelo:'),  "yellow", ["bold"])
    user_max=eval(TALinput(str, regex=f"^[-+]?[0-9](.)*$", sep=None, TAc=TAc)[0])
    if min !=None and 'pow2' in str(min):
        min_comparison = eval(min[4:])
        user_max_comparison=abs(user_max)
        # print(min, user_max_comparison)
    else:
        user_max_comparison=user_max
        min_comparison=min
    # print('user_max ', user_max, '   sup ',sup)
    if user_max_comparison==sup or user_max_comparison>sup or ((user_max_comparison<min_comparison) if min_comparison!=None else None):
        TAc.print(LANG.render_feedback("max", f'vedi, {user_max} non appartiene all\'insieme, quindi non puo\' essere un massimo'),  "red", ["bold"])
    elif user_max_comparison<sup:
        if sup!=inf:
            TAc.print(LANG.render_feedback("max", f'vedi, {(user_max+sup)/2} e\' maggiore del tuo {user_max} ma e\' nell\'insieme, quindi {user_max} non puo\' essere un massimo'),  "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback("max", f'vedi, {abs(user_max)+random.randint(1,10)} e\' maggiore del tuo {user_max} ma e\' nell\'insieme, quindi non puo\' essere un massimo'),  "red", ["bold"])
    TAc.print(LANG.render_feedback("max", f'sei ancora convinto che esista il massimo per questo insieme? (y/n)'),  "yellow", ["bold"])
    y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
    if y_n=='y':
        non_existence_max(sup,min)
    else:
        return TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])

def check_existence_max(y_n, max): # il massimo esiste ma il ragazzo dice di no
    if y_n=='n':
        return TAc.print(LANG.render_feedback("max", f'e {max} appartiene all\'insieme... quindi e\' un massimo!'),  "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback("max", f'fammi un esempio di un numero maggiore di {max} che stia nell\'insieme:'),  "yellow", ["bold"])
        wrong_max=eval(TALinput(str, regex=f"^[-+]?[0-9](.)*$", sep=None, TAc=TAc)[0])
        if wrong_max<max or wrong_max==max:
            TAc.print(LANG.render_feedback("wrong-max", f'guarda che {wrong_max} <= {max}... sei ancora convinto che esistono numeri nell\'insieme maggiori di {max}? (y/n)'),  "red", ["bold"])
            y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
            check_existence_max(y_n, max)
        else:
            TAc.print(LANG.render_feedback("wrong-max", f'guarda che {wrong_max} non sta nell\'insieme... sei ancora convinto che esistono numeri nell\'insieme maggiori di {max}? (y/n)'),  "red", ["bold"])
            y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
            check_existence_max(y_n, max)

def max_case(max,sup,min):
    TAc.print(LANG.render_feedback("max", f'l\'insieme ha massimo? (y/n)'),  "yellow", ["bold"])
    y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
    if y_n=='y':
        if max!=None: # il massimo esiste e il ragazzo ha risposto giusto, verifichiamo ora il massimo che propone lui
            TAc.print(LANG.render_feedback("max", f'scrivimelo:'),  "yellow", ["bold"])
            existence_but_not_correctness_max(max)
        else: # il massimo non esiste ma il ragazzo ha detto di si
            non_existence_max(sup,min)
    else:
        if max==None: #il massimo non esiste e il ragazzo ha risposto giusto
            TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
        else: # il massimo esiste ma il ragazzo ha detto di no
            TAc.print(LANG.render_feedback("max", f'beh... esistono numeri nell\'insieme maggiori di {max}? (y/n)'),  "yellow", ["bold"])
            y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
            check_existence_max(y_n,max)

def non_existence_max_with_parameter(condition,min): # il ragazzo afferma che ci sia un massimo ma in realtà non esiste
    TAc.print(LANG.render_feedback("max", f'ah si? scrivimelo:'),  "yellow", ["bold"])
    user_max=eval(TALinput(str, regex=f"^[-+]?[0-9](.)*$", sep=None, TAc=TAc)[0])
    min_comparison=int(min[1:]) if min[0]=='x' else eval(condition,{'k':int(min[1:])})
    if user_max<min_comparison:
        TAc.print(LANG.render_feedback("max", f'vedi, {user_max} non appartiene all\'insieme, quindi non puo\' essere un massimo'),  "red", ["bold"])
    else:
        user_k=(user_max-1)/int(condition[0]) if '+' in condition else (user_max)/int(condition[0])
        if not user_k.is_integer():
            TAc.print(LANG.render_feedback("max", f'vedi, {user_max} non appartiene all\'insieme, quindi non puo\' essere un massimo'),  "red", ["bold"])
        else:
            x_proposal=int(eval(condition, {'k':user_k+1}))
            TAc.print(LANG.render_feedback("max", f'vedi, {x_proposal} e\' maggiore del tuo {user_max} ma e\' nell\'insieme, quindi {user_max} non puo\' essere un massimo'),  "red", ["bold"])
    TAc.print(LANG.render_feedback("max", f'sei ancora convinto che esista il massimo per questo insieme? (y/n)'),  "yellow", ["bold"])
    y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
    if y_n=='y':
        non_existence_max_with_parameter(condition,min)
    else:
        return TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])

def max_case_parameter(condition,min,max):
    TAc.print(LANG.render_feedback("max", f'l\'insieme ha massimo? (y/n)'),  "yellow", ["bold"])
    y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
    if y_n=='y':
        if max!=None: # il massimo esiste e il ragazzo ha risposto giusto, verifichiamo ora il massimo che propone lui
            TAc.print(LANG.render_feedback("max", f'scrivimelo:'),  "yellow", ["bold"])
            x_max=ll.find_max_with_parameter(condition,max)
            existence_but_not_correctness_max(x_max)
        else: # il massimo non esiste ma il ragazzo dice di si
            non_existence_max_with_parameter(condition,min)
    else:
        if max==None: #il massimo non esiste e il ragazzo ha risposto giusto
            TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
        else: # il massimo esiste ma il ragazzo ha detto di no
            x_max=ll.find_max_with_parameter(condition,max)
            TAc.print(LANG.render_feedback("max", f'beh... esistono numeri nell\'insieme maggiori di {x_max}? (y/n)'),  "yellow", ["bold"])
            y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
            check_existence_max(y_n,x_max)

def sup_case(sup):
    user_sup=eval(TALinput(str, regex=f"^[-+]?[0-9](.)*|[-+]?[a-z]+$", sep=None, TAc=TAc)[0])
    if user_sup==sup:
        return TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("wrong", random.choice(ll.wrong)), "red", ["bold"])
        sup_case(sup)

def not_limited_set():
    TAc.print(LANG.render_feedback("majorant", f'allora prova a darmi un esempio di maggiorante per questo insieme:'),  "yellow", ["bold"])
    wrong_majorant=float(TALinput(str, regex=f"^[-+]?[0-9](.)*$", sep=None, TAc=TAc)[0])
    TAc.print(LANG.render_feedback("max", f'no, {wrong_majorant} non e\' un maggiorante... guarda che non e\' limitato superiormente questo insieme. \nHai cambiato idea ora?(y/n)'),  "red", ["bold"])
    y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
    return TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"]) if y_n=='y' else not_limited_set()

def new_match(seed,contatore,output_filename):
    parameter,instance, arg_1, arg_2=ll.instance_randgen_1(seed)
    TAc.print(LANG.render_feedback("instance", f'L\'insieme {instance} e\' limitato(superiormente)? (y/n)'),  "yellow", ["bold"])
    y_n=TALinput(str, regex=f"^(y|n)$", sep=None, TAc=TAc)[0]
    # CASO CON PARAMETRO k
    if parameter=='parameter':
        condition=arg_1
        min_max=arg_2
        min=min_max[0]
        max=min_max[1]
        # print('condition: ',condition,'- min: ',min,'- max: ',max)
        if y_n=='y':
            if max!=None: # l'insieme è limitato superiormente e il ragazzo ha risposto correttamente
                TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])  
                max_case_parameter(condition,min,max)
            else: # l'insieme non è limitato superiormente ma il ragazzo ha risposto di si
                not_limited_set()
                max_case_parameter(condition,min,max)
        else:
            assert y_n=='n'
            if max==None: # l'insieme non è limitato superiormente e il ragazzo ha risposto correttamente
                TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
                max_case_parameter(condition,min,max)
            else: # l'insieme è limitato superiormente ma il ragazzo ha detto di no
                contatore += 5
                random.seed(seed+contatore)
                x_max=ll.find_max_with_parameter(condition,max)
                majorant=eval(condition,{'k':random.randint(1,6)})
                TAc.print(LANG.render_feedback("max", f'Guarda che e\' limitato... ad esempio {x_max+majorant} e\' un maggiorante.'),  "red", ["bold"])
                TAc.print(LANG.render_feedback("max", f'Ti ho convinto?'),  "yellow", ["bold"])
                return new_match(seed, contatore,output_filename)
        if max!=None:
            sup=int(max[1:]) if max[0]=='x' else int(eval(condition,{'k':int(max[1:])}))
        else:
            sup=inf
    else: # CASO SENZA PARAMETRO k
        max=arg_1
        inf_sup=arg_2
        if isinstance(inf_sup,list):
            min=inf_sup[0]
            sup=inf_sup[1]
        else:
            sup=inf_sup
            min=None
        if y_n=='y':
            if sup!=inf: # l'insieme è limitato superiormente e il ragazzo ha risposto correttamente
                TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
                max_case(max,sup,min)
            else: # l'insieme non è limitato superiormente ma il ragazzo ha risposto di si
                not_limited_set()
                max_case(max,sup,min)
        else:
            assert y_n=='n'
            if sup==inf: # l'insieme non è limitato superiormente e il ragazzo ha risposto correttamente
                TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
                max_case(max,sup,min)
            else: # l'insieme è limitato superiormente ma il ragazzo ha detto di no
                contatore += 5
                random.seed(seed+contatore)
                TAc.print(LANG.render_feedback("max", f'Guarda che e\' limitato... ad esempio {sup+random.randint(1,10)} e\' un maggiorante.'),  "red", ["bold"])
                TAc.print(LANG.render_feedback("max", f'Ti ho convinto?'),  "yellow", ["bold"])
                return new_match(seed, contatore,output_filename)
    TAc.print(LANG.render_feedback("sup", f'dammi ora l\'estremo superiore:'),  "yellow", ["bold"])
    if ENV["download"]:
        output=instance+'\n'+str(seed)
        TALf.str2output_file(output,output_filename)
    return sup_case(sup)

def what_to_do():
    TAc.print(LANG.render_feedback("what-to-do", 'Vuoi fermarti qui o fare un\'altra partita? (stop/another_match)'),  "yellow", ["bold"])
    answer_what_to_do=TALinput(str, regex=f"([a-zA-Z])\w+", sep=None, TAc=TAc)
    if answer_what_to_do[0]=='stop':
        TAc.print(LANG.render_feedback("end", random.choice(ll.end)), "green", ["bold"])
        exit(0)
    else:
        assert answer_what_to_do[0]=='another_match'
        seed=random.randint(100000,999999)
        TAc.print(LANG.render_feedback("seed", f'seed: {seed}'), "yellow", ["bold"])
        output_filename = f"instance_{seed}.max_sup.txt"
        new_match(seed,contatore,output_filename)
        what_to_do()

TAc.print(LANG.render_feedback("start", 'Per risolvere l\'esercizio ti potrebbero tornare utili i seguenti concetti: \n1) Se un insieme non e\' finito potrebbe non ammettere massimo. \n2) Un insieme limitato (superiormente/inferiormente/entrambi) non sempre ammette massimo.\n3) Un numero k in X (dove X e\' un insieme totalmente ordinato) e\' un maggiorante di Y, Y sottoinsieme di X, se k >= x per ogni x in Y. \n4) L\'estremo superiore di Y e\' il minimo dei maggioranti. \n5) Ogni sottoinsieme Y di X non vuoto e limitato superiormente possiede estremo superiore.'), "white")
if ENV["source"]!='catalogue':
    assert ENV["source"]=='randgen'
    output_filename = f"instance_{ENV['seed']}.max_sup.txt"
    seed=ENV["seed"]
    TAc.print(LANG.render_feedback("seed", f'seed: {seed}'), "yellow", ["bold"])
else:
    input = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension='txt')
    instance=input.split('\n')[0]
    seed=int(input.split('\n')[1])
    output_filename = f"instance_catalogue_{ENV['instance_id']}.max_sup.txt"
    TAc.print(LANG.render_feedback("seed", f'instance_id: {ENV["instance_id"]}'), "yellow", ["bold"])

contatore=0 # mi serve per generare numeri casuali in modo indipendente dal seed (nel caso di "insieme limitato ma il ragazzo dice di no")
new_match(seed,contatore,output_filename)
what_to_do()
exit(0)