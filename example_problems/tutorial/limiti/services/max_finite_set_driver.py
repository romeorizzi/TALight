#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
import limiti_lib as ll
from numpy import array
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('reference_set',str),
    ('instance_id',int),
    ('seed',int),
    ('cardinality',int),
    ('download',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
reference_set=ENV["reference_set"]
source=ENV["source"]
seed=ENV["seed"]
set_cardinality=ENV["cardinality"]

if source=='catalogue':
    set_values = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension='txt')
    TAc.print(LANG.render_feedback("instance", f'# instance_id: {ENV["instance_id"]} \n# Dati i seguenti numeri: \n{set_values}'),  "yellow", ["bold"])
    instance=ll.instance_to_array(set_values)
    output_filename = f"instance_catalogue_{ENV['instance_id']}_max_fin_set.txt"
else:
    assert source=='randgen'
    instance=array(ll.instance_randgen(set_cardinality,reference_set,seed),dtype='str')
    set_values='\n'.join(instance)
    TAc.print(LANG.render_feedback("start", f'# seed: {ENV["seed"]} \n# Dati i seguenti numeri: \n{set_values}'), "yellow", ["bold"])
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
    TAc.print(LANG.render_feedback("correct", f'Ottimo! Confermo che {max_value} e` il massimo in quanto: \n1) appartiene all\'insieme, \n2) non ci sono numeri maggiori di lui.'), "green", ["bold"])
    exit(0)
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
    TAc.print(LANG.render_feedback("wrong", f'No, infatti {grater_number} > {user_max}, inoltre {grater_number} appartiene all\'insieme, quindi {user_max} non puo` essere il massimo!'), "red", ["bold"])
    exit(0)