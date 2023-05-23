#!/usr/bin/env python3
from sys import stderr, exit
from random import randrange
from os import environ
import random
from turing_machine_lib import random_seq 

ENV={}
ENV['seed'] = environ['TAL_seed']

# START CODING YOUR SERVICE: 
    
sequence = random_seq(ENV['seed'])


#TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
print(sequence)
#TAc.print(LANG.render_feedback("long-sol","Too long solution: "), "yellow", ["bold"])
   
exit(0)