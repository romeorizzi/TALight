#!/usr/bin/env python3
# -*- coding:latin-1-*-
from sys import stderr, exit

from IPv4_lib_ita import *
from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

args_list=[
  ('subnet_mask', str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')

# START CODING YOUR SERVICE:

TAc.print("Enter a subnet mask, to see how many ip addresses it might contain", "green", ["bold"])
subnet=(ENV['subnet_mask'], TAc, LANG)
subnet=[]
subnet=TALinput(str, num_tokens=4, regex=f"^((\d)+)$", sep='.', TAc=TAc)

for i in range(4):
  if subnet[i]!='0' and subnet[i]!='255':
    TAc.print("\nERRORE\n", "red", ["bold"])
    TAc.print("A subnet mask is a set of 4 numbers which can be 0 or 255 ", "red")
    exit(0)
for i in range (3):
  if subnet[i]=='0' and subnet[i+1]=='255':
    TAc.print("\nERRORE\n", "red", ["bold"])
    TAc.print("A subnet mask is a set of 4 numbers which can be 0 or 255 and after a 0 there cannot be a 255", "red")
    exit(0) 
if subnet[3]=='255':
  TAc.print("\nERRORE\n", "red", ["bold"])
  TAc.print("A subnet mask cannot end with 255", "red")
  exit(0)
if subnet[1]=='0':
  TAc.print("16,581,475 ip addresses can be allocated in this subnet mask", "green")
elif subnet[2]=='0':
  TAc.print("65,025 ip addresses can be allocated in this subnet mask", "green")
else:
  TAc.print("255 ip addresses can be allocated in this subnet mask", "green")
