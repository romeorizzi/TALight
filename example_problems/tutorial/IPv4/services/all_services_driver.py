#!/usr/bin/env python3
from sys import stderr, exit

from typing import Any
from IPv4_lib import *
from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

args_list=[]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')

# START CODING YOUR SERVICE:
TAc.print("Questo servizio elenchera tutti i serivizi di questo prblema", "green", ["bold"])
TAc.print("how_many_ips: in questo sotto-problema dovrai inserire una subnet mask per sapere quanti indirizzi ip possono essere configurati sotto tale subnet mask", "green")
#TAc.print("gimme_ip_address: in questo sotto-problema dovrai inserire un indirizzo ip per sapere quali potrebbero essere gli indirizzi di rete che lo contengono", "green")
TAc.print("first_ip: in questo sotto-problema ti viene chiesto di inserire il primo indirizzo ip appartente all'indirizzo di rete","green")
TAc.print("last_ip: in questo sotto-problema ti viene chiesto di inserire l'ultimo indirizzo ip appartenete all'indirizzo di rete", "green")
TAc.print("random_ip: in questo sotto-problema ti viene chiesto di inserire un indirizzo ip appartente all'indirizzo di rete", "green")

