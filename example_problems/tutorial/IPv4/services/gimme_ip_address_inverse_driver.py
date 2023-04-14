#!/usr/bin/env python3
# -*- coding:latin-1-*-

from sys import stderr, exit

from multilanguage import Env, TALcolors, Lang

from IPv4_lib import input_ip, net_address
from services.TALinputs import TALinput

#dai subito in out-put un indirizzo internet e dai un indirizzo ip e guardi se è giusto oppure no
args_list=[
  ('yes_no', str),
  ('with_opening_message',bool),
  ('interactive',bool),
  ('loop', bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now' if ENV['with_opening_message'] else 'never')

# START CODING YOUR SERVICE
#
#

