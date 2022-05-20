#!/usr/bin/env python3
from sys import stderr
from fractions import Fraction
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import math
import numpy as np
import os
import limiti_lib as ll
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('instance_id',int),
    ('instance_format',str),
    ('download',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
def c_infinito():
    for x in intervallo:
        f_x=eval(function)
        if c==float('inf'): # caso in cui c= +inf
            if f_x < N:
                TAc.print(LANG.render_feedback("wrong-M", f'No, non hai inserito un buon valore per M... per x = {x} ad esempio si ha f({x})={f_x} < {N}\n'), "red", ["bold"])
                exit(0)
        else:
            if f_x > -N: # caso in cui c= -inf
                TAc.print(LANG.render_feedback("wrong-M", f'No, non hai inserito un buon valore per M... per x = {x} ad esempio si ha f({x})={f_x} > {-N}\n'), "red", ["bold"])
                exit(0)

def c_finito():
    for x in intervallo:
        f_x=eval(function)
        if abs(f_x-c)>epsilon:
            TAc.print(LANG.render_feedback("wrong-input", f'No... Per x = {x} ad esempio si ha |f(x)-{c}|={abs(f_x-c)} > {epsilon}\n'), "red", ["bold"])
            exit(0)
# DATI
percorso=os.path.join(ENV.META_DIR,'gen','instances_hardcoded',f'instance_{str(ENV["instance_id"]).zfill(3)}.txt')
instance_str = ll.get_file_str_from_path(path=percorso)
function,x_0,c=ll.get_instance_from_txt(instance_str)

# function='(2*x+1)/(3*x-1)'
# c='2/3'
# x_0=np.inf
epsilon=0.1
N=10

# f_x_0=eval(function, {"x":x_0}) # oppure nella riga sopra si mette x=2 e qui si richiama solo eval(function) senza il secondo argomento
# TAc.print(f'f(x): {f_x_0}', "white")     # che corrisponde alla variabile c

# INIZIO DEL DIALOGO CON LO STUDENTE
TAc.print(LANG.render_feedback("this-is-the-limit", 'Verifica il seguente limite:'), "white")
TAc.print('lim '+ function +" = "+ c, "white")
TAc.print('x->'+ str(x_0), "white")
function=ll.alfabeto(function)
# ora trasformo in float x_0 e c
c=float(c) if 'inf' in c else eval(c)
x_0=float(x_0) if 'inf' in x_0 else eval(x_0)

if not math.isinf(c): # limiti finiti
    TAc.print(LANG.render_feedback("this-is-the-epsilon", f'\nViene proposto come epsilon: {epsilon}'), "white")
    if not math.isinf(x_0): # lim finito per x che tende ad un numero finito
# DEFINIZIONE: per ogni epsilon>0 esiste delta>0 t.c. 0<|x-x_0|<delta => |f(x)-c|<epsilon
        delta, intervallo = ll.x_0_finito(x_0,epsilon)
        c_finito()
        TAc.print(LANG.render_feedback("correct-delta", f'Corretto! \ndelta={delta} verifica il limite proposto. \n'), "green",["bold"])
        exit(0)
    else: # lim finito per x che tende all'infinito
# DEFINIZIONE: per ogni epsilon>0 esiste M>0 t.c. x>M => |f(x)-c|<epsilon
#                                 (se x-> -inf)  x<-M
        M, intervallo= ll.x_0_infinito(x_0,epsilon)
        c_finito()
        TAc.print(LANG.render_feedback("correct-M", f'Corretto! \nM={M} verifica il limite proposto. \n'), "green",["bold"])
        exit(0)
else: # limiti infiniti
    TAc.print(LANG.render_feedback("this-is-the-N", f'\nViene proposto come N: {N}'), "white")
    if not math.isinf(x_0): # lim infinito per x che tende ad un numero finito
# DEFINIZIONE: per ogni N>0 esiste delta>0 t.c. 0<|x-x_0|<delta => f(x)>N
#                                                                  f(x)<-N  (se c=-inf)
        delta, intervallo = ll.x_0_finito(x_0,N)
        c_infinito()
        TAc.print(LANG.render_feedback("correct-delta", f'Corretto! \ndelta={delta} verifica il limite proposto. \n'), "green",["bold"])
        exit(0)
    else: # lim infinito per x che tende all'infinito
# DEFINIZIONE: per ogni N>0 esiste M>0 t.c. x>M => f(x)>N
#                                                  f(x)<-N  (se c=-inf)
#                           (se x-> -inf)  x<-M
        M,intervallo= ll.x_0_infinito(x_0,N)
        c_infinito()
        TAc.print(LANG.render_feedback("correct-M", f'Corretto! \nM={M} verifica il limite proposto. \n'), "green",["bold"])
        exit(0)