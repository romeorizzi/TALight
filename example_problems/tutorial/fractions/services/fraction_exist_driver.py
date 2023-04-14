#!/usr/bin/env python3
# -*- coding:latin-1-*-

from datetime import datetime
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

from fractions_lib import *

args_list=[
  ('num_questions', int),
  ('lang', str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:


LANG.print_opening_msg()
for _ in range(ENV['num_questions']):
      
  TAc.print(LANG.render_feedback("ask_decimal_number", "\nEnter a decimal number: "), "green", ["bold"])
  a, b=input_number(TAc, LANG)
  n=a+b
  d=pow(10, len(b))

  TAc.print(LANG.render_feedback("solution", f"\nAn equivalent fraction of the number {a},{b} is {n}/{d}."), "yellow", ["bold"])
  
  #Some reduction of the fraction for big inputs
  n1=int(n)
  for i in [2, 5]:
    while n1%i==0 and d%i==0:
      n1/=i
      d/=i
  
  n1=int(n1)
  d=int(d)
  if int(n)!=n1:
    TAc.print(LANG.render_feedback("better_solution", f"\nAnother equivalent fraction is {n1}/{d}."), "yellow", ["bold"])
  
exit(0)
