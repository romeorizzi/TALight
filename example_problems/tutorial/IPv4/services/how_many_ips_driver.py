#!/usr/bin/env python3
from sys import stderr, exit

from typing import Any
from IPv4_lib import *
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
subnet=TALinput(str, regex=f"^((\S)+)$", sep='.', TAc=TAc)

if subnet[1]=='0':
  TAc.print("In qusta subnet mask possono essere allocati 16.581.475 indirizzi ip", "green")
elif subnet[2]=='0':
  TAc.print("In questa subnet mask possono essere allocati 65.025 indirizzi ip", "green")
else:
  TAc.print("In questa subnet mask possono essere collocati 255 indirizzi ip", "green")
