#!/usr/bin/env python3
# -*- coding:latin-1-*-

from datetime import datetime
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

from fractions_lib import *

args_list=[
  ('decimal_digits', int),
  ('whole_number_digits', int),
  ('num_questions', int),
  ('lang', str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:


LANG.print_opening_msg()
for _ in range(ENV['num_questions']):
  
  num=generate_number(ENV['whole_number_digits'], ENV['decimal_digits'])
  TAc.print(LANG.render_feedback("output", f"\nThe decimal number: "+num[0]+","+num[1]), "green", ["bold"])
  TAc.print(LANG.render_feedback("ask_fraction", f"\nEnter the equivalent fraction: "), "green", ["bold"])
  a, b=input_fraction(TAc, LANG)
  
  # finds the equivalent fraction:
  n=num[0]+num[1]
  d1=d=pow(10, len(num[1]))
  n1=int(n)
  c=int(a)/int(b)
  for i in [2, 5]:
    while n1%i==0 and d1%i==0:
      n1/=i
      d1/=i
    
  n1=int(n1)
  d1=int(d1)

  k=int(a)/n1
  h=int(b)/d1
  
  
  if k==h:
    TAc.print(LANG.render_feedback("correct", f"\nCorrect answer!"), "green", ["bold"])
    if int(a)>n1:
        TAc.print(LANG.render_feedback("better answer", f"However, the best solution would be {n1}/{d1} \nRemember to check if numerator and denominator can be divided by the same number."), "cyan", ["bold"])
  elif k>h:
    TAc.print(LANG.render_feedback("too-high", f"\nWrong answer! Indeed {a}/{b} = {c} > "+num[0]+","+num[1]), "red", ["bold"])
    TAc.print(LANG.render_feedback("solution", f"\nThe best answer is {n1}/{d1}"), "yellow", ["bold"])
  elif k<h:
    TAc.print(LANG.render_feedback("too-low", f"\nWrong answer! Indeed {a}/{b} = {c} < "+num[0]+","+num[1]), "red", ["bold"])
  
exit(0)
