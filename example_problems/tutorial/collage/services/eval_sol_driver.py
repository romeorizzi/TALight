#!/usr/bin/env python3
from sys import stderr, exit

import random
import math
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import collage_lib as cl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('code_lang',str),
    ('lang',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

# INSTANCES FOR GOAL = correct
goals = ['correct']

instances = {}
seq_len = 7
num_col = 3
NUM_INSTANCES = 5
scaling_factor = 2
mod = random.choice([1,2])

instances['correct'] = cl.instances_generator(NUM_INSTANCES, scaling_factor, seq_len, num_col, mod)

# INSTANCES FOR GOAL = 2^n o n^2        
#if ENV["goal"] == 'time_at_most_2_exp_n' or ENV["goal"] =='time_at_most_n_exp_2':
if ENV["goal"] == 'time_at_most_2_exp_n':
  goals.append('time_at_most_2_exp_n')
  seq_len = 20  # could still be 2^{\choose(n,2)}
  num_col = 15
    
  if ENV["code_lang"] == "compiled":
    # MAX_N = 18
    pass

  NUM_INSTANCES = 7
  scaling_factor = 1.8

  instances['time_at_most_2_exp_n'] = cl.instances_generator(NUM_INSTANCES, scaling_factor, seq_len, num_col, mod)

# INSTANCES FOR GOAL = n^2
if ENV["goal"] == 'time_at_most_n_exp_2':
  goals.append('time_at_most_n_exp_2')
  instances['time_at_most_n_exp_2'] = []
  seq_len = 30  # could still be 2^n
  num_col = 20
    
  if ENV["code_lang"] == "compiled":
    seq_len = 40  # could still be 2^n
    num_col = 30

  # MAX_N = 50  # we intend to evaluate positively only the linear O(n^2) solutions
  
  if ENV["code_lang"] == "compiled":
    # MAX_N = 100
    pass
    
  NUM_INSTANCES = 5
  scaling_factor = 1.6

  instances['time_at_most_n_exp_2'] = cl.instances_generator(NUM_INSTANCES, scaling_factor, seq_len, num_col, mod)
           
MAX_TIME = 2

# FUNCTION TESTING ONE SINGLE TESTCASE: 
def test(instance):
    rainbow = instance['rainbow']
    seq_len = instance['seq_len']
    num_col = instance['num_col']

    TAc.print(LANG.render_feedback("rainbow-size",'# We have this number of stripes in the rainbow: '), "white", ["bold"], end='')
    TAc.print(seq_len, "yellow", ["bold"])
    TAc.print(LANG.render_feedback("rainbow-colors",'# Rainbow is made of this number of colors: '), "white", ["bold"], end='')
    TAc.print(num_col, "yellow", ["bold"])
    TAc.print(LANG.render_feedback("print-rainbow", f'\n# The sequence is:\n'), "white", ["bold"])

    cl.print_rainbow(rainbow)

    TAc.print(LANG.render_feedback("best-sol-question", f'\n# Which is the minimum number of sheets for this collage?'), "white", ["bold"])
    start = monotonic()
    answer = TALinput(int, line_recognizer=lambda val,TAc,LANG:True, TAc=TAc, LANG=LANG)[0]
    end = monotonic()
    instance['measured_time'] = end-start

    sheets = cl.calculate_sheets(rainbow)
        
    if answer == sheets:
      instance['answer_correct'] = True
    else:
      instance['answer_correct'] = False

# MAIN: TEST ALL TESTCASES: 
out_of_time = 0

for goal in goals:
  for instance in instances[goal]:
    test(instance)

    if instance['measured_time'] > MAX_TIME:
      out_of_time += 1
      cl.print_summaries(goals,instances,MAX_TIME,out_of_time,TAc,LANG)
      exit(0)
            
cl.print_summaries(goals,instances,MAX_TIME,out_of_time,TAc,LANG)
exit(0)
