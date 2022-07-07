#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
import limiti_lib as ll
from numpy import array
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('reference_set',str),
    ('cardinality',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
reference_set=ENV["reference_set"]
set_cardinality=ENV["cardinality"]
tipo_insieme='naturali' if reference_set=='natural' else 'decimali'
if TALf.exists_input_file('instance'):
    instance=TALf.input_file_as_str('instance')
    instance_array = ll.get_instance_from_txt(instance)
    TAc.print(LANG.render_feedback("successful-load", 'Il file che hai associato al gestore di file `instance` e` stato caricato con successo.'), "white", ["bold"])
    TAc.print(LANG.render_feedback("this-is-the-instance", f'L\'insieme che mi hai sottoposto e`: \n{instance} \n\ned il massimo e`'), "yellow", ["bold"])
    max_elem=max(instance_array)
    TAc.print(LANG.render_feedback("this-is-the-max", f'{max_elem}'), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("correct", f'in quanto: \n1) appartiene all\'insieme, \n2) non ci sono numeri maggiori di lui.'), "yellow", ["bold"])
    exit(0)
else:
    TAc.print(LANG.render_feedback("waiting", f'In attesa dell\' insieme di {set_cardinality} numeri {tipo_insieme}. \nFormato: un numero per riga.\nQualsiasi riga che inizia con il carattere "#" viene ignorata.\nSe preferisci, puoi richiamare il servizio con `rtal connect limiti solve_max_finite_set -finstance=percorso_del_file_contenente_la_tua_istanza` e prederemo direttamente noi l\'insieme invece di agire copiandolo e incollandolo te stesso qui sul terminale.'), "yellow")
    TAc.print(LANG.render_feedback("waiting", f'Scrivi '), "yellow", ["bold"])
    instance = []
    for i in range (set_cardinality):
        if reference_set=='natural':
            instance.append(TALinput(int, regex=f"^\d+$", sep=' ', TAc=TAc)[0])
        else:
            instance.append(TALinput(float, regex=f"^[+-]?\d(.)?\d*$", sep=' ', TAc=TAc)[0])
    max_elem=max(instance)
    TAc.print(LANG.render_feedback("this-is-the-instance", f'Il massimo e`'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("this-is-the-max", f'{max_elem}'), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("correct", f'in quanto: \n1) appartiene all\'insieme, \n2) non ci sono numeri maggiori di lui.'), "yellow", ["bold"])
    exit(0)