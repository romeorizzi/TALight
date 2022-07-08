#!/usr/bin/env python3
# -*- coding:latin-1-*-

from sys import stderr, exit
from typing import Any

from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

from IPv4_lib_eng import *

args_list=[
  ('ip_address', str),
  ('with_opening_message',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now' if ENV['with_opening_message'] else 'never')

# START CODING YOUR SERVICE:

subnet=subnet_mask()
internet=net_address(subnet)
TAc.print("SUBNET MASK:  ", "green", ["bold"])
TAc.print(subnet, "yellow")
TAc.print("\nINTERNET ADDRESS:  ", "green", ["bold"]), 
TAc.print(internet, "yellow")


TAc.print("\nEnter the first IP address belonging to the network address above", "green", ["bold"])

Ip=[]
ip=(ENV['ip_address'], TAc, LANG)
Ip=input_ip()
punteggio=1
while punteggio<10:

  while internet[0] != Ip[0] or internet[1]!=Ip[1] or internet[2] != Ip[2] or internet[3]!=Ip[3] :
    TAc.print("WRONG\nTRY AGAIN", "red", ["bold"])
    Ip=[]
    Ip=input_ip()

  TAc.print("RIGHT\n", "green", ["bold"])
  punteggio+=1
  subnet=subnet_mask()
  internet=net_address(subnet)
  TAc.print("\nSUBNET MASK:  ", "green", ["bold"])
  TAc.print(subnet, "yellow")
  TAc.print("\nINTERNET ADDRESS:  ", "green", ["bold"])
  TAc.print(internet, "yellow")
  Ip=input_ip()

TAc.print("\nCongratulations\n", "green", ["bold"])
TAc.print("Correct answers: 10/10", "green")
  
