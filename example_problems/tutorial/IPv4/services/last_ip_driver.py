#!/usr/bin/env python3
# -*- coding:latin-1-*-

from sys import intern, stderr, exit

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

  TAc.print(LANG.render_feedback("ask_ip","\nEnter the last ip address belonging to the offered network address"), "yellow", ["bold"])

  punteggio=0

  ip=(ENV['ip_address'], TAc, LANG)
  Ip=input_ip(TAc, LANG) 

  while punteggio != 10:

    if internet[1] == '0':
      while internet[0]!=Ip[0] or (Ip[1]!='255') or (Ip[2]!='255')  or (Ip[3]!='255') :
        TAc.print(LANG.render_feedback("wrong_input","WRONG\nTRY AGAIN"), "red", ["bold"])
        Ip=input_ip(TAc, LANG)

      TAc.print(LANG.render_feedback("right","RIGHT\n"), "green", ["bold"])
      punteggio+=1 

    elif internet[1] != '0' and internet[2]=='0':
      while internet[0]!=Ip[0] or internet[1]!=Ip[1] or (Ip[2]!='255')  or (Ip[3]!='255') :
        TAc.print(LANG.render_feedback("wrong_input","WRONG\nTRY AGAIN"), "red", ["bold"])
        Ip=input_ip(TAc, LANG)

      TAc.print(LANG.render_feedback("right","RIGHT\n"), "green", ["bold"])
      punteggio+=1

    else:
      while internet[0]!=Ip[0] or internet[1]!=Ip[1] or internet[2]!=Ip[2]  or (Ip[3]!='255') :
        TAc.print(LANG.render_feedback("wrong_input","WRONG\nTRY AGAIN"), "red", ["bold"])
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

else:
  TAc.print("SUBNET MASK:  ", "green", ["bold"])
  TAc.print(ENV['subnet_Mask'], "green")
  TAc.print("\nINTERNET ADDRESS:  ", "green", ["bold"]), 
  TAc.print(ENV['net_address'], "green")
  TAc.print("\nLat ip address", "green", ["bold"])
  TAc.print(ENV['ip_address'], "white")
  