#!/usr/bin/env python3
from sys import stderr, exit

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

TAc.print("\nInserire un indirizzo ip, riceverai i 3 possibili indirizzi internet a cui l'indirizzo ip può essere contenuto", "green")



ip=(ENV['ip_address'], TAc, LANG)
#ip=TALinput(str, regex= f"regex: //([0-9]{1,3}\.){3}[0-9]{1,3}/gm", TAc=TAc,sep='.')#, regex_explained= "un indirizzo ip è un insieme di 4 terzine di numeri; ogni numero può andare da un minimo di 0 ad un massimo di 255")

ip=TALinput(str, regex=f"^((\S)+)$", TAc=TAc, sep=".")

#separetedStrings= ip.split(".")
Ip=[]
for i in range (4) :
  #Ip.append( int(separetedStrings[i]))
  Ip.append( int(ip[i]))
  
TAc.print("\nL'indirizzo ip inserito può essere contenuto nei seguenti indirizzi internet:\n", "grenn", ["bold"])
TAc.print(Ip[0],"green", "0.0.0")