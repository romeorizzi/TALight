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
TAc.print(LANG.render_feedback("principio-Archimede", '\nPer ogni x reale, x>0, esiste un numero naturale n tale che 1/n < x. \nSei pronto a dimostrarmelo? Cominciamo subito!'), "white")

def check_user_solution(x):
    user_sol=eval(TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0])
    if user_sol<0 or int(user_sol)!=user_sol:
        TAc.print(LANG.render_feedback("error", f'no, il numero che hai inserito non e\' naturale, riprova:'), "red", ["bold"])
        return check_user_solution()
    proof=1/user_sol
    if not proof<eval(str(x)):
        error_answer=random.choice([f'no, 1/{user_sol} = {round(proof,5)} e come noterai {round(proof,5)} >= {x}, riprova:', f'mmm ho paura che tu abbia abagliato, infatti 1/{user_sol} = {round(proof,5)} e come noterai {round(proof,5)} >= {x}, ritenta:'])
        TAc.print(LANG.render_feedback("error", error_answer), "red", ["bold"])
        return check_user_solution(x)
    assert proof<eval(str(x))
    return TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])

def new_match(seed,counter):
    counter+=1
    TAc.print(LANG.render_feedback("seed", f'(seed: {seed})'), "yellow", ["bold"])
    x=ll.instance_archimede(seed)
    TAc.print(LANG.render_feedback("proposal", f'La mia proposta per x e\': {x} \ndammi un numero naturale n tale che 1/n < x:'), "yellow", ["bold"])
    check_user_solution(x)
    if counter<2:
        TAc.print(LANG.render_feedback("ok", f'Mi stai iniziando a convincere, voglio riprovare \n'), "yellow", ["bold"])
        seed=random.randint(100000,999999)
        new_match(seed,counter)
    else:
        return TAc.print(LANG.render_feedback("correct", f'Mi hai convinto! ben fatto!'), "green", ["bold"])

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

counter=0
new_match(ENV['seed'], counter)
what_to_do()
# if ENV["source"]!='catalogue':
#     assert ENV["source"]=='randgen'
#     output_filename = f"instance_{ENV['seed']}.max_sup.txt"
#     seed=ENV["seed"]
#     TAc.print(LANG.render_feedback("seed", f'seed: {seed}'), "yellow", ["bold"])
# else:
#     input = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension='txt')
#     instance=input.split('\n')[0]
#     seed=int(input.split('\n')[1])
#     output_filename = f"instance_catalogue_{ENV['instance_id']}.max_sup.txt"
#     TAc.print(LANG.render_feedback("seed", f'instance_id: {ENV["instance_id"]}'), "yellow", ["bold"])