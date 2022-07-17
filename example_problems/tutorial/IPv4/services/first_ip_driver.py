#!/usr/bin/env python3
# -*- coding:latin-1-*-

from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

from IPv4_lib import *

args_list=[
  ('subnet_Mask', str),
  ('net_address', str),
  ('ip_address', str),
  ('with_opening_message',bool),
  ('interactive', bool)
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now' if ENV['with_opening_message'] else 'never')

# START CODING YOUR SERVICE:


if ENV['interactive']:
  subnet=subnet_mask()
  internet=net_address(subnet)
  TAc.print("SUBNET MASK:  ", "green", ["bold"])
  TAc.print(subnet, "green")
  TAc.print("\nINTERNET ADDRESS:  ", "green", ["bold"]), 
  TAc.print(f"{'.'.join(internet)}", "green")
  
  TAc.print(LANG.render_feedback("ask_ip", "\nEnter the first IP address belonging to the network address above:\n"), "yellow", ["bold"])

  Ip=input_ip(TAc, LANG)
  punteggio=1
  while punteggio<10:

    while int(internet[0]) != int(Ip[0]) or int(internet[1])!=int(Ip[1]) or int(internet[2]) != int(Ip[2]) or int(internet[3])!=int(Ip[3]) :
      TAc.print(LANG.render_feedback("wrong_input","WRONG\nTRY AGAIN"), "red", ["bold"])
      Ip=[]
      Ip=input_ip(TAc, LANG)

    TAc.print(LANG.render_feedback("right","RIGHT\n"), "green", ["bold"])
    punteggio+=1
    
    if punteggio < 10:
      subnet=subnet_mask()
      internet=net_address(subnet)
      TAc.print("SUBNET MASK:  ", "green", ["bold"])
      TAc.print(subnet, "green")
      TAc.print("\nINTERNET ADDRESS:  ", "green", ["bold"]), 
      TAc.print(f"{'.'.join(internet)}", "green")
      Ip=input_ip(TAc, LANG)

  TAc.print(LANG.render_feedback("final_message","\nCongratulations\n"), "green", ["bold"])
  TAc.print(LANG.render_feedback("point","Correct answers: 10/10"), "green")
    
else :
  TAc.print("SUBNET MASK:  ", "green", ["bold"])
  TAc.print(ENV['subnet_Mask'], "green")
  TAc.print("\nINTERNET ADDRESS:  ", "green", ["bold"]), 
  TAc.print(ENV['net_address'], "green")
  TAc.print("\nFirst IP address", "green", ["bold"])
  TAc.print(ENV['ip_address'], "white")
  
