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

if ENV["code_lang"] == "compiled":
  MAX_TIME = 1
else:
  MAX_TIME = 2

instances = {}
goals = []
type_seq = random.choice([1,2])

# INSTANCES FOR GOAL = seq_1_to_50
if ENV["goal"] == 'seq_from_1_to_50':
  goals.append('seq_from_1_to_50')

  seq_len = 7
  num_col = 3
  NUM_INSTANCES = 5
  scaling_factor = 1.6

  instances['seq_from_1_to_50'] = cl.instances_generator(NUM_INSTANCES, scaling_factor, seq_len, num_col, type_seq)

# INSTANCES FOR GOAL = seq_from_50_to_200
if ENV["goal"] == 'seq_from_50_to_200':
  goals.append('seq_from_50_to_200')
  
  seq_len = 50
  num_col = 35  
  NUM_INSTANCES = 5
  scaling_factor = 1.4

  instances['seq_from_50_to_200'] = cl.instances_generator(NUM_INSTANCES, scaling_factor, seq_len, num_col, type_seq)
           
# INSTANCES FOR GOAL = seq_from_200_to_1000
if ENV["goal"] == 'seq_from_200_to_1000':
  goals.append('seq_from_200_to_1000')

  seq_len = 200
  num_col = 160
  NUM_INSTANCES = 7
  scaling_factor = 1.3

  instances['seq_from_200_to_1000'] = cl.instances_generator(NUM_INSTANCES, scaling_factor, seq_len, num_col, type_seq)


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
