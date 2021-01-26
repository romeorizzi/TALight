#!/usr/bin/env python3

from os import environ
import yaml
from sys import exit
from random import randrange

ENV_lang = environ["TAL_lang"]
ENV_numbers = environ["TAL_numbers"]
ENV_num_questions = int(environ["TAL_num_questions"])

with open("sum_and_product_server." + ENV_lang + ".yaml", 'r') as stream:
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
#English: print(f"# I will serve: problem=sum, service=sum_and_product, numbers={ENV_numbers}, num_questions={ENV_num_questions}, colored_feedback={ENV_colored_feedback}, lang={ENV_lang}.")

gen_new_pair = True    
for _ in range(ENV_num_questions):
    if gen_new_pair:
        if ENV_numbers == "onedigit":
            x = randrange(10)
            y = randrange(10)
        elif ENV_numbers == "twodigits":
            x = randrange(100)
            y = randrange(100)
        else:
            x = randrange(2**32)
            y = randrange(2**32)
    cprint("? {x+y} {x*y}", "yellow", "on_blue", ["bold"])
    spoon = input().strip()
    while spoon[0] == '#':
        cprint(spoon, 'magenta', 'on_blue')
        spoon = input().strip()
    a, b = map(int, spoon.split(" "))
    gen_new_pair = False
    if a+b > x+y:
       print_lang(["no_answ", "red", "on_blue", ["blink"]], ["over-sum", "yellow", "on_blue", ["underline"]])        
       #English: print(f"No! indeed, {a}+{b}={a+b} > {x+y}.")
    elif a+b < x+y:    
       print_lang(["no_answ", "red", "on_blue", ["blink"]], ["under-sum", "yellow", "on_blue", ["underline"]])        
       #English: print(f"No! indeed, {a}+{b}={a+b} < {x+y}.")
    elif a*b > x*y:    
       print_lang(["no_answ", "red", "on_blue", ["blink"]], ["over-product", "yellow", "on_blue", ["underline"]])        
       #English: print(f"No! indeed, {a}*{b}={a*b} > {x*y}.")
    elif a*b < x*y:    
       print_lang(["no_answ", "red", "on_blue", ["blink"]], ["under-product", "yellow", "on_blue", ["underline"]])        
       #English: print(f"No! indeed, {a}*{b}={a*b} < {x*y}.")
    else:
        assert (a + b == x+y) and (a * b == x*y)
        print_lang(["ok_answ", "green", "on_blue"], ["ok", "grey", "on_blue"])        
        #English: print(f"OK! indeed, {a}+{b}={x+y} and {a}*{b}={x*y}.")
        gen_new_pair = True

print_lang(["got-bored", "magenta", "on_blue"])        
#English: print("! (I got bored)")
exit(0)
