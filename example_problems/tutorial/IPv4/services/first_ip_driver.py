#!/usr/bin/env python3
from ipaddress import ip_address
from sys import stderr, exit

import random
from typing import Any
from IPv4_lib import *
from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang
args_list=[
  ("ip_address", str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')


subnet=subnet_mask()
internet=net_address(subnet)
print("SUBNET MASK:  ",subnet)
print("INTERNET ADDRESS:  ",internet)

TAc.print("Inserire il primo indirizzo ip appartenente all'indirizo di rete qui sopra", "red", ["bold"])
ip=(ENV[ip_address], TAc, LANG)
separetedStrings= ip.split(".")
numeriIP=[]
for i in range (len(separetedStrings)) :
  numeriIP.append( int(separetedStrings[i]))
if internet[0] != numeriIP[0] or internet[1]!=numeriIP[1] or internet[2] != numeriIP[2] or internet[3]!=numeriIP[3] :
  TAc.print("ERRORE\nRiprova", "red", ["bold"])
else:
  TAc.print("GIUSTO\n", "grenn", ["bold"])
