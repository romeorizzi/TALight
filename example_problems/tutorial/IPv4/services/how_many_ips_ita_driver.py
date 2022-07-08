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

TAc.print("Inserire una subnet Mask, per vedere quanti indirizi ip potrebbero essere contenuti", "green", ["bold"])
subnet=(ENV['subnet_mask'], TAc, LANG)
subnet=[]
subnet=TALinput(str, num_tokens=4, regex=f"^((\d)+)$", sep='.', TAc=TAc)

for i in range(4):
  if subnet[i]!='0' and subnet[i]!='255':
    TAc.print("\nERRORE\n", "red", ["bold"])
    TAc.print("Una subnet mask è un insieme di 4 numeri che posso essere 0 o 255 e nessun alto numeri", "red")
    exit(0)
for i in range (3):
  if subnet[i]=='0' and subnet[i+1]=='255':
    TAc.print("\nERRORE\n", "red", ["bold"])
    TAc.print("Una subnet mask è un insieme di 4 numeri che posso essere 0 o 255 e dopo uno 0 non ci può essere un 255", "red")
    exit(0) 
if subnet[3]=='255':
  TAc.print("\nERRORE\n", "red", ["bold"])
  TAc.print("Una subnet mask non può terminare con 255", "red")
  exit(0)
if subnet[1]=='0':
  TAc.print("In qusta subnet mask possono essere allocati 16.581.475 indirizzi ip", "green")
elif subnet[2]=='0':
  TAc.print("In questa subnet mask possono essere allocati 65.025 indirizzi ip", "green")
else:
  TAc.print("In questa subnet mask possono essere collocati 255 indirizzi ip", "green")
