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

subnet=subnet_mask()
internet=net_address(subnet)
TAc.print("SUBNET MASK:  ", "green")
TAc.print(subnet, "green")
TAc.print("\nINTERNET ADDRESS:  ", "green")
TAc.print(internet, "green")

TAc.print("\nInserire l'ultimo indirizzo ip appartenente all'indirizo di rete qui sopra", "green", ["bold"])

ip=[]

ip=(ENV['ip_address'], TAc, LANG)
ip=TALinput(str, regex= f"regex: //([0-9]{1,3}\.){3}[0-9]{1,3}/gm", TAc=TAc,sep='.')#, regex_explained= "un indirizzo ip è un insieme di 4 terzine di numeri; ogni numero può andare da un minimo di 0 ad un massimo di 255")

#TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)
#ip=input()
#separetedStrings= ip.split(".")
Ip=[]
for i in range (4) :
  Ip.append( int(ip[i]))
  
if internet[1] == 0:
  if internet[0]!=Ip[0] or Ip[1]!=255 or Ip[2]!=255  or Ip[3]!=255 :
    TAc.print("ERRORE\nRiprova", "red", ["bold"])
  else:
      TAc.print("GIUSTO\n", "green", ["bold"]) 
elif internet[1] != 0 and internet[2]==0:
  if internet[0]!=Ip[0] or internet[1]!=Ip[1] or Ip[2]!=255  or Ip[3]!=255 :
    TAc.print("ERRORE\nRiprova", "red", ["bold"])
  else:
      TAc.print("GIUSTO\n", "green", ["bold"])
else:
  if internet[0]!=Ip[0] or internet[1]!=Ip[1] or internet[2]!=Ip[2]  or Ip[3]!=255 :
    TAc.print("ERRORE\nRiprova", "red", ["bold"])
  else:
      TAc.print("GIUSTO\n", "green", ["bold"])




  



