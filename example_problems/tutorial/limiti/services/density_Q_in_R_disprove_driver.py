#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
import limiti_lib as ll
from math import *
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('seed',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:

TAc.print(LANG.render_feedback("enunciato", '\nRiusciro` a convincerti che dati x,y due numeri reali, x<y , esiste un numero razionale q tale che x<q<y?'), "white")
TAc.print(LANG.render_feedback("disprove", 'inserisci un qualsiasi valore reale x:'),  "yellow", ["bold"])
user_x=TALinput(str, regex=f"^(\S)+$", sep=None, TAc=TAc)[0]
x_eval=eval(user_x)
TAc.print(LANG.render_feedback("disprove", 'inserisci un valore reale y tale che x<y:'),  "yellow", ["bold"])
user_y=TALinput(str, regex=f"^(\S)+$", sep=None, TAc=TAc)[0]
y_eval=eval(user_y)
# print(x_eval, y_eval)
if x_eval<0 and 0<y_eval:
    TAc.print(LANG.render_feedback("disprove", f'vedi, per q=0 si ha che x={user_x} < 0 < {user_y}=y'),  "yellow", ["bold"])
if not x_eval<y_eval:
    TAc.print(LANG.render_feedback("error", f'hai inserito un valore per y<=x e io te ne avevo chiesto uno maggiore... non posso continuare'), "red", ["bold"])	
    exit(0)
n=ceil(1/(y_eval-x_eval)+0.00000000001)
integer=ceil(n*x_eval+0.00000000001)
# print('n ',n,'integer ',integer)
assert integer < n*y_eval
q=integer/n
# print(q)
assert x_eval<q and q<y_eval
TAc.print(LANG.render_feedback("disprove", f'vedi, per q={integer}/{n}={q} si ha che x={user_x} < {integer}/{n} < {user_y}=y'),  "yellow", ["bold"])
TAc.print(LANG.render_feedback("what-to-do", f'Spero di averti convinto! \nSe vuoi provare ora a dimostrare la densita` di Q in R ti consiglio il servizio \'rtal connect limiti density_Q_in_R_prover\''),  "white", ["bold"])
exit(0)