#!/usr/bin/env python3
from sys import stderr, exit

import random
from IPv4_lib import *
from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang
args_list=[
  ("subnet_Mask", str),
  ("net_address", str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')


subnet=subnet_mask()
internet=net_address(subnet)
print("SUBNET MASK:  ",subnet)
print("INTERNET ADDRESS:  ",internet)
first_ip(internet)