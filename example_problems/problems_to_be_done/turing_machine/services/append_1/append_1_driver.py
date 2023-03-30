#!/usr/bin/env python3
from sys import stderr, exit

#from multilanguage import Env, TALcolors, Lang
#from TALinputs import TALinput

from os import environ
import random
#import turing_machine_lib as tl_lib


ENV={}
ENV['seed'] = environ['TAL_seed']

# START CODING YOUR SERVICE: 
    
if ENV['seed']=='random_seed': 
    random.seed()
    seed = random.randrange(0,1000000)
    print(seed)
else:
    seed = int(ENV['seed'])
    print(seed)

random.seed(seed)
length = random.randint(1, 20)
sequence = []
for i in range(length):
    sequence.append(random.randint(0, 1))


#TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
print(sequence)
#TAc.print(LANG.render_feedback("long-sol","Too long solution: "), "yellow", ["bold"])
   
exit(0)
