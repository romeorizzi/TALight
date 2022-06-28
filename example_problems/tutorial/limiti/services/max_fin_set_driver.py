#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
from math import *
import limiti_lib as ll
import random
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('instance_id',int),
    ('seed',int),
    ('set_cardinality',int),
    ('download',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
# FUNZIONI
def soluzione(instance_str,max_position):
    sol=TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)
    # controllare soluzione studente
    if sol[0]==instance_str[max_position]: # capire se mantenere così o valutare l'input dell'utente: 
        # LATO POSITIVO: se si mantiene tutto così c'è maggior precisione nello scrivere costanti/simboli matematici (perchè se si decide di valutare l'input ad esempio 'pi' può essere scritto in modo equivalente come un float con 15 cifre significative...)
        # LATO NEGATIVO: mantenendo così però scrivendo 5/2 e 2.5 verrebbe generato un errore (così come anche 20.10 e 20.1)
        return TAc.print(LANG.render_feedback("correct", random.choice(ll.correct)), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("wrong", random.choice(ll.wrong)), "red", ["bold"])
        soluzione(instance_str,max_position)

def new_set(seed,source):
    if source=='catalogue':
        set_values = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension='fin_set.txt')
        TAc.print(LANG.render_feedback("instance", f'Dato l\'insieme (avente instance_id={ENV["instance_id"]}):\n'+'{'+set_values+'}'),  "yellow", ["bold"])
        instance_str=ll.instance_to_array(set_values)
        output_filename = f"instance_catalogue_{ENV['instance_id']}.fin_set.txt"
    else:
        assert source=='randgen'
        instance_str=ll.instance_randgen(ENV["set_cardinality"],seed)
        set_values=', '.join(instance_str)
        TAc.print(LANG.render_feedback("instance", f'Dato l\'insieme (avente seed={seed}):\n'+'{'+set_values+'}'),  "yellow", ["bold"])
        output_filename = f"instance_{seed}.txt"
    if ENV["download"]:
        TALf.str2output_file(set_values,output_filename)
    return instance_str

def new_match(seed,source):
    instance_str=new_set(seed,source)
    instance=ll.instance_to_number(instance_str)
    max_position=instance.index(max(instance))
    print(instance_str[max_position])
    TAc.print(LANG.render_feedback("max", f'determina il massimo:'), "yellow", ["bold"])
    soluzione(instance_str,max_position)

def what_to_do():
    TAc.print(LANG.render_feedback("what-to-do", 'Vuoi fermarti qui, fare un\'altra partita oppure ti senti pronto a passare ad un livello successivo? (stop/another_match/next_level)'),  "yellow", ["bold"])
    answer_what_to_do=TALinput(str, regex=f"([a-zA-Z])\w+", sep=None, TAc=TAc)
    if answer_what_to_do[0]=='stop':
        TAc.print(LANG.render_feedback("end", random.choice(ll.end)), "green", ["bold"])
        exit(0)
    elif answer_what_to_do[0]=='another_match':
        seed=random.randint(100000,999999)
        new_match(seed,'randgen')
        what_to_do()
    else:
        assert answer_what_to_do[0]=='next_level'
        TAc.print(LANG.render_feedback("algorithm", 'Ok! Ecco una proposta per il livello successivo: \nProva a scrivere (qui su terminale o immettendo un bot) una funzione ricorsiva che calcoli per te il massimo di un insieme finito'),  "yellow", ["bold"])
        # path=TALinput(str, sep=None, TAc=TAc)[0]
        # answer=TALf.get_file_str_from_path(path)
        # print(answer)
        exit(0)
TAc.print(LANG.render_feedback("start", 'Proviamo a vedere se in un insieme finito e non vuoto di numeri reali riusciamo a trovare sempre un massimo.'), "white")
new_match(ENV["seed"],ENV["source"])
what_to_do()