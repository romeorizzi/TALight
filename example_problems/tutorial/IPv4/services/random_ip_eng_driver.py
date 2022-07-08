#!/usr/bin/env python3
from sys import stderr, exit
from tkinter.font import BOLD

from typing import Any
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

subnet=subnet_mask()
internet=net_address(subnet)
TAc.print("SUBNET MASK:  ", "green", ["bold"])
TAc.print(subnet, "yellow")
TAc.print("\nINTERNET ADDRESS:  ", "green", ["bold"]), 
TAc.print(internet, "yellow")

TAc.print("\nEnter an ip address belonging to the network address above", "green", ["bold"])

punteggio=0

ip=(ENV['ip_address'], TAc, LANG)
Ip=input_ip() #TALinput(int ,num_tokens=4, regex= f"regex: ^((\d)+)((\.)+)$ ", TAc=TAc ,sep='.')# regex_explained= "un indirizzo ip è un insieme di 4 terzine di numeri; ogni numero può andare da un minimo di 0 ad un massimo di 255")


while punteggio != 10:

  if internet[1] == 0:
    while internet[0]!=Ip[0] or (Ip[1]>255 or Ip[1]<0) or (Ip[2]>255 or Ip[2]<0)  or (Ip[3]>255 or Ip[3]<0) :
      TAc.print("WRONG\nTRY AGAIN\n", "red", ["bold"])
      Ip=input_ip()

    TAc.print("RIGHT\n", "green", ["bold"])
    punteggio+=1 

  elif internet[1] != 0 and internet[2]==0:
    while internet[0]!=Ip[0] or internet[1]!=Ip[1] or (Ip[2]>255 or Ip[2]<0)  or (Ip[3]>255 or Ip[3]<0) :
      TAc.print("WRONG\TRY AGAIN", "red", ["bold"])
      Ip=input_ip()

    TAc.print("RIGHT\n", "green", ["bold"])
    punteggio+=1

  else:
    while internet[0]!=Ip[0] or internet[1]!=Ip[1] or internet[2]!=Ip[2]  or (Ip[3]>255 or Ip[3]<0) :
      TAc.print("WRONG\TRY AGAIN", "red", ["bold"])
      Ip=input_ip()
    
    TAc.print("RIGHT\n", "green", ["bold"])
    punteggio+=1

  subnet=subnet_mask()
  internet=net_address(subnet)
  TAc.print("\nSUBNET MASK:  ", "green", ["bold"])
  TAc.print(subnet, "yellow")
  TAc.print("\nINTERNET ADDRESS:  ", "green", ["bold"]), 
  TAc.print(internet, "yellow")
  Ip=input_ip()


TAc.print("\nCongratulations\n", "green", ["bold"])
TAc.print("Correct answers: 10/10", "green")