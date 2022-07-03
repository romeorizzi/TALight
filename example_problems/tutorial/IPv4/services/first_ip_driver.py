#!/usr/bin/env python3
#from asyncore import write
from sys import stderr, exit

import string
import random
from typing import Any
from IPv4_lib import *
from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

args_list=[
  ('ip_address', str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')

# START CODING YOUR SERVICE:

subnet=subnet_mask()
internet=net_address(subnet)
TAc.print("SUBNET MASK:  ", "green")
TAc.print(subnet, "green")
TAc.print("\nINTERNET ADDRESS:  ", "green")
TAc.print(internet, "green")

TAc.print("\nInserire il primo indirizzo ip appartenente all'indirizo di rete qui sopra", "green", ["bold"])

ip=""

ip=(ENV['ip_address'], TAc, LANG)
ip=TALinput(str, regex= f"^((\d)+\.){3}(\d)+$", sep=".", TAc=TAc)#,regex_explained= "un indirizzo ip è un insieme di 4 terzine di numeri; ogni numero può andare da un minimo di 0 ad un massimo di 255")

#TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)

#separetedStrings= ip.split(".")
#numeriIP=[]
#for i in range (len(separetedStrings)) :
#  numeriIP.append( int(separetedStrings[i]))
  
#if internet[0] != numeriIP[0] or internet[1]!=numeriIP[1] or internet[2] != numeriIP[2] or internet[3]!=numeriIP[3] :
if internet[0]!=ip[0] or internet[1]!=ip[1] or internet[2]!=ip[2]  or internet[3]!=ip[3] :
  TAc.print("ERRORE\nRiprova", "red", ["bold"])
else:
  TAc.print("GIUSTO\n", "green", ["bold"])
