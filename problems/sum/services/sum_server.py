#!/usr/bin/env python3

from os import environ
import yaml
from termcolor import colored, cprint
from sys import exit
from random import randrange

ENV_lang = environ["TAL_lang"]
ENV_numbers = environ["TAL_numbers"]
ENV_obj = environ["TAL_obj"]
ENV_num_questions = int(environ["TAL_num_questions"])
ENV_colored_feedback = (environ["TAL_colored_feedback"] == "yes")

with open("sum_server." + ENV_lang + ".yaml", 'r') as stream:
    try:
        messages_book = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


def print_lang(*args,**kwargs):
  message1, *other_messages = args
  msg1_code, *msg1_colors = message1
  msg1_str=eval(f"f'{messages_book[msg1_code]}'")
  msg1_code, *msg1_rendering = message1
  msg1_attrs = []
  if type(msg1_rendering[-1]) == list:
      msg1_attrs = msg1_rendering[-1]
      msg1_colors = msg1_rendering[:-1]
  else:
      msg1_colors = msg1_rendering      
  if len(other_messages)==0:
    if ENV_colored_feedback:
      cprint(msg1_str, *msg1_colors, attrs=msg1_attrs, **kwargs)
    else:
      print(msg1_str, **kwargs)
  else:
    if ENV_colored_feedback:
      cprint(msg1_str, *msg1_colors, attrs=msg1_attrs, end="")
    else:
      print(msg1_str, end="")  
    print_lang(*other_messages, **kwargs)

        
print_lang(["open-channel", "magenta", "on_blue"])        
#English: print(f"# I will serve: problem=sum, service=sum, numbers={ENV_numbers}, obj={ENV_obj}, num_questions={ENV_num_questions}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}.")

gen_new_s = True    
for _ in range(ENV_num_questions):
    if gen_new_s:
        if ENV_numbers == "onedigit":
            s = randrange(10)
        elif ENV_numbers == "twodigits":
            s = randrange(100)
        else:
            s = randrange(2**64)
    cprint(f"? {s}", "yellow", "on_blue", ["bold"])
    spoon = input().strip()
    while spoon[0] == '#':
        cprint(spoon, 'magenta', 'on_blue')
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_s = False
    if a+b > s:
       print_lang(["no_answ", "red", "on_blue", ["blink"]], ["too-much", "yellow", "on_blue", ["underline"]])        
       #English: print(f"No! indeed, {a}+{b}={a+b} > {s}.")
    elif a+b < s:    
       print_lang(["no_answ", "red", "on_blue", ["blink"]], ["too-little", "yellow", "on_blue", ["underline"]])        
       #English: print(f"No! indeed, {a}+{b}={a+b} < {s}.")
    else: # a + b == n
        if ENV_obj == "max_product":
            if a < b:
                a,b = b,a
            if a-b > 1:
                print_lang(["no_answ", "red", "on_blue", ["blink"]], ["not-balanced", "yellow", "on_blue", ["underline"]])        
                #English: print(f"No! indeed, {a-1}+{b+1}={s} and {a-1}*{b+1}={(a-1)*(b+1)} > {a*b}={a}*{b}.")
            else:
                gen_new_s = True
                print_lang(["ok_answ", "green", "on_blue"], ["max-product", "grey", "on_blue"])        
                #English: print(f"OK! indeed, x={a} and y={b} have maximum product among the integer numbers with x+y={s}. Do you know why? Do you have a proof for your intuition?")
        else:
            print_lang(["ok_answ", "green", "on_blue"], ["right-sum", "grey", "on_blue"])        
            #English: print(f"OK! indeed, {a}+{b}={s}")
            gen_new_s = True
            
print_lang(["got-bored", "magenta", "on_blue"])        
#English: print("! (I got bored)")
exit(0)
