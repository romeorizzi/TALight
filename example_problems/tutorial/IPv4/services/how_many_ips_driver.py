#!/usr/bin/env python3
# -*- coding:latin-1-*-
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

args_list=[
  ('subnet_mask', str),
  ('with_opening_message',bool),
  ('interactive',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now' if ENV['with_opening_message'] else 'never')

# START CODING YOUR SERVICE:
def print_ips(subnet, TAc):
  if subnet[1]=='0':
    TAc.print(LANG.render_feedback("large","16,777,216 ip addresses can be allocated in this subnet mask"), "green")
  elif subnet[2]=='0':
    TAc.print(LANG.render_feedback("medium","65,535 ip addresses can be allocated in this subnet mask"), "green")
  else:
    TAc.print(LANG.render_feedback("small","256 ip addresses can be allocated in this subnet mask"), "green")


if ENV['interactive']:
  while True:
    TAc.print(LANG.render_feedback("aks_subnet_mask","Enter a subnet mask, to see how many ip addresses it might contain: "), "yellow", ["bold"])
    subnet=(ENV['subnet_mask'], TAc, LANG)
    subnet=[]
    subnet=TALinput(str, num_tokens=4, regex=f"^((\d)+)$", sep='.', TAc=TAc)

    for i in range(4):
      if subnet[i]!='0' and subnet[i]!='255':
        TAc.print(LANG.render_feedback("error_1","\nERROR\n"), "red", ["bold"])
        TAc.print(LANG.render_feedback("error_2","A subnet mask is a set of 4 numbers which can be 0 or 255 "), "red")
        exit(0)
    for i in range (3):
      if subnet[i]=='0' and subnet[i+1]=='255':
        TAc.print(LANG.render_feedback("error_1","\nERRORE\n"), "red", ["bold"])
        TAc.print(LANG.render_feedback("error_3","A subnet mask is a set of 4 numbers which can be 0 or 255 and after a 0 there cannot be a 255"), "red")
        exit(0) 
    if subnet[3]=='255':
      TAc.print(LANG.render_feedback("error_1","\nERRORE\n"), "red", ["bold"])
      TAc.print(LANG.render_feedback("error_4","A subnet mask cannot end with 255"), "red")
      exit(0)
    print_ips(subnet, TAc)

else: 
  subnet=ENV['subnet_mask']
  print_ips(subnet, TAc)