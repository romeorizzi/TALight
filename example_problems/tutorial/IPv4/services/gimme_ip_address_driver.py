#!/usr/bin/env python3
# -*- coding:latin-1-*-

from sys import stderr, exit
from typing import List

from multilanguage import Env, TALcolors, Lang

from IPv4_lib import input_ip

args_list=[
  ('ip_address', str),
  ('with_opening_message',bool),
  ('interactive',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now' if ENV['with_opening_message'] else 'never')

# START CODING YOUR SERVICE:

def print_info(Ip:List):
    TAc.print(LANG.render_feedback("title_info_table","\n"f"Network addresses that can be guested within the ip address {'.'.join(Ip)}:"), "green", ["bold"])
    TAc.print("1°-->   ", "green", end="")
    TAc.print(Ip[0],"green", end="") 
    TAc.print(".0.0.0\n", "green")
    TAc.print("2°-->   ", "green", end="")
    TAc.print(Ip[0],"green", end="")
    TAc.print(".", "green", end="")
    TAc.print(Ip[1], "green", end="")
    TAc.print(".0.0\n", "green")
    TAc.print("3°-->   ", "green", end="")
    TAc.print(Ip[0],"green", end="")
    TAc.print(".", "green", end="")
    TAc.print(Ip[1],"green", end="")
    TAc.print(".", "green", end="")
    TAc.print(Ip[2], "green", end="")
    TAc.print(".0\n", "green")    

if ENV['interactive']:
    while True:
        TAc.print(LANG.render_feedback("prompt_ip_address","\nEnter your ip address: "), "yellow", ["bold"])
        Ip=input_ip(TAc,LANG)
        print_info(Ip)
else:
    print_info(ENV['ip_address'].split('.'))



