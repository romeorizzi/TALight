#!/usr/bin/env python3
# -*- coding:latin-1-*-

from sys import stderr, exit

from IPv4_lib_eng import *
from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

args_list=[
  ('ip_address', str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')

# START CODING YOUR SERVICE:

TAc.print("\nEnter an ip address, you will receive the 3 possible internet addresses to which the ip address can be contained", "green", ["bold"])



Ip=(ENV['ip_address'], TAc, LANG)
#ip=TALinput(str, regex= f"regex: //([0-9]{1,3}\.){3}[0-9]{1,3}/gm", TAc=TAc,sep='.')#, regex_explained= "un indirizzo ip è un insieme di 4 terzine di numeri; ogni numero può andare da un minimo di 0 ad un massimo di 255")

Ip=input_ip()


TAc.print("\nThe ip address entered can be contained in the following internet addresses:\n", "green", ["bold"])
TAc.print("1°-->   ", "green", end="")
TAc.print(Ip[0],"green", end="") 
TAc.print(".0.0.0\n", "green")
TAc.print("2°-->   ", "green", end="")
TAc.print(Ip[0],"green", end="")
TAc.print(".", "green", end="")
TAc.print(Ip[1], "green", end="")
TAc.print(".0.0\n", "green")
TAc.print("3°-->   ", "green", end="")
TAc.print(Ip[0],"green", end="")
TAc.print(".", "green", end="")
TAc.print(Ip[1],"green", end="")
TAc.print(".", "green", end="")
TAc.print(Ip[2], "green", end="")
TAc.print(".0\n", "green")