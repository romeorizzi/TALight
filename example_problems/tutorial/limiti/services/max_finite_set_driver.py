#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
import limiti_lib as ll
from numpy import array, sign
# METADATA OF THIS TAL_SERVICE:
args_list = [
    # ('source',str),
    ('numbers_type',str),
    # ('instance_id',int),
    ('seed',int),
    ('cardinality',int),
    ('verbose',bool),
    ('silent',bool),
    ('download',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
if ENV['silent']:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')
else:
    LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
reference_set=ENV["numbers_type"]
# source=ENV["source"]
seed=ENV["seed"]
set_cardinality=ENV["cardinality"]

instance=array(ll.instance_randgen(set_cardinality,reference_set,seed),dtype='str')
set_values='\n'.join(instance)
TAc.print(LANG.render_feedback("seed", f'# puoi richiamarmi attraverso il comando -aseed= {ENV["seed"]}'), "yellow")
TAc.print(LANG.render_feedback("start", f'# Dati i seguenti numeri: \n{set_values}'), "yellow", ["bold"])
output_filename = f"instance_{seed}_max_fin_set.txt"
if ENV["download"]:
    TALf.str2output_file(set_values,output_filename)
instance=ll.instance_to_number(instance)
max_value=max(instance)
# print(instance_str[max_value])
TAc.print(LANG.render_feedback("max", f'# inserisci il massimo:'), "yellow", ["bold"])
user_max=eval(TALinput(str, regex=f"^([+-]?[.\d]*)$", sep=None, TAc=TAc)[0])
# controllare soluzione studente
if user_max==max_value:
    TAc.print(LANG.render_feedback("correct", f'Ottimo! Confermo che {max_value} e` il massimo in quanto: \n1) {max_value} appartiene all\'insieme, \n2) nell\'insieme non sono presenti numeri maggiori di {max_value}.'), "green", ["bold"])
elif user_max not in instance:
    TAc.print(LANG.render_feedback("wrong", f'No, {user_max} non e` nell\'insieme quindi non puo` essere il massimo!'), "red", ["bold"])
    exit(0)
else:
    elem=instance[0]
    grater_numbers=[]
    for i in range(set_cardinality):
        if instance[i]>user_max:
            grater_numbers.append(instance[i])
    grater_numbers.sort()
    grater_number=grater_numbers[(len(grater_numbers)-1)//2]
    TAc.print(LANG.render_feedback("wrong", f'No, infatti {grater_number} > {user_max}, e {grater_number} appartiene all\'insieme, quindi {user_max} non puo` essere il massimo!'), "red", ["bold"])
    exit(0)
if ENV["verbose"]:
    TAc.print(LANG.render_feedback("proof", f'Infatti'), "green", ["bold"])
    for i in range(len(instance)):
        current_number=instance[i]
        sign='<' if current_number<max_value else '='
        TAc.print(LANG.render_feedback("proof", f'{current_number} {sign} {max_value}'), "green", ["bold"])
    exit(0)
else:
    exit(0)