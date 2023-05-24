#!/usr/bin/env python3
# -*- coding:latin-1-*-

import random

from TALinputs import TALinput


def input_number(TAc, LANG):
  num=TALinput(str, num_tokens=2, regex="^[0-9]*$", TAc=TAc, sep=',')
  
  end=False
  if len(num[0])>len(str(int(num[0]))):
    TAc.print(LANG.render_feedback("number_starting_with_zero", "\nERROR\nThe integer part of a decimal number cannot start with 0!"), "red", ["bold"])
    end=True
  
  if int(num[1])%10==0:
    TAc.print(LANG.render_feedback("decimal_number_ending_with_zero", "\nERROR\nA decimal number cannot end with 0!"), "red", ["bold"])
    end=True
  
  if end:
    exit(0)
  
  return num[0], num[1]


def input_fraction(TAc, LANG):
  num=TALinput(str, num_tokens=2, regex="^[0-9]*$", TAc=TAc, sep='/')
  
  end=False
  if len(num[0])>len(str(int(num[0]))):
    TAc.print(LANG.render_feedback("numerator_starting_with_zero", "\nERROR\nThe numerator of a fraction cannot start with 0!"), "red", ["bold"])
    end=True
  
  if len(num[1])>len(str(int(num[1]))):
    TAc.print(LANG.render_feedback("denominator_starting_with_zero", "\nERROR\nThe denominator of a fraction cannot start with 0!"), "red", ["bold"])
    end=True
  
  if end:
    exit(0)
    
  return num[0], num[1]


def generate_number(whole_number_digits, decimal_digits):
  n=str(random.randint(0,pow(10, whole_number_digits)-1))
  d=str(random.randint(pow(10, decimal_digits-1), pow(10,decimal_digits)-1))[::-1]
  num=[]
  num.append(n)
  num.append(d)
  return num