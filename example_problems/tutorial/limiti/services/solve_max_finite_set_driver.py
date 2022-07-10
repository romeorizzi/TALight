#!/usr/bin/env python3
from gettext import find
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
import limiti_lib as ll
from math import *
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('verbose',bool),
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
if TALf.exists_input_file('instance'):
    instance_input=TALf.input_file_as_str('instance')
    instance_str= ll.get_instance_from_txt(instance_input)
    TAc.print(LANG.render_feedback("this-is-the-instance", f'L\'insieme che mi hai sottoposto e`: \n{instance_input}'), "yellow", ["bold"])
else:
    TAc.print(LANG.render_feedback("waiting", f'Ci attendiamo ora che tu inserisca un insieme di numeri. \nFormato: un numero per riga. \nTipo di numero: naturali, interi, razionali, reali, espressioni numeriche. Ti e` consentito inserire costanti matematiche e funzioni presenti nella libreria math (se necessario consulta il sito https://docs.python.it/html/lib/module-math.html)\nPer terminare: scrivi in una nuova riga "end". \nQualsiasi riga che inizia con il carattere "#" viene ignorata.\nSe preferisci, puoi richiamare il servizio con `rtal connect limiti solve_max_finite_set -finstance=percorso_del_file_contenente_la_tua_istanza` e prenderemo direttamente noi l\'insieme invece di scriverlo/copiarlo e incollarlo tu stesso qui sul terminale.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("waiting", f'Inizia ad inserire riga per riga i numeri dell\'insieme:'), "yellow", ["bold"])
    instance_str = []
    elem=(TALinput(str, sep=' ', TAc=TAc)[0])
    while elem !='end':
        instance_str.append(elem)
        elem=TALinput(str, sep=' ', TAc=TAc)[0]
instance=ll.instance_to_number(instance_str)
max_elem=max(instance)
posiz_max=instance.index(max_elem)
max_str=instance_str[posiz_max]
TAc.print(LANG.render_feedback("this-is-the-instance", f'Il massimo e`'), "yellow", ["bold"])
TAc.print(LANG.render_feedback("this-is-the-max", f'{max_str}'), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("correct", f'in quanto: \n1) {max_str} appartiene all\'insieme, \n2) nell\'insieme non sono presenti numeri maggiori di {max_str}.'), "yellow", ["bold"])
if ENV["verbose"]:
    TAc.print(LANG.render_feedback("proof", f'Infatti'), "green", ["bold"])
    for i in range(len(instance)):
        current_number=instance[i]
        sign='<' if current_number<max_elem else '='
        TAc.print(LANG.render_feedback("proof", f'{instance_str[i]} {sign} {max_str}'), "green", ["bold"])
    exit(0)
else:
    exit(0)