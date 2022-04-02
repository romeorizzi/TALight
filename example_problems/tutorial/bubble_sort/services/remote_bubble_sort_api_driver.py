#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
import sys
import random


'''
COMANDI

CMD_GET_ARRAY -> ritorna array
CMD_COMPARE_CONSEC_ELEM i -> ritorna se array[i] > array[i+1]
CMD_SWAP_CONSEC_ELEM i -> scambia elemento in pos i con pos i+1
'''

# METADATA OF THIS TAL_SERVICE:
problem = "bubble_sort"
service = "remote_bubble_sort_api"
args_list = [
    ('feedback', str),
    ('lang', str),
    ('goal', str)
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

max_value = 30
max_array = 20

# Generating array
length = random.randint(1, max_array)

array = [random.randrange(1, max_value, 1) for i in range(length)]
array = [22, 1, 16]
print(array, file=sys.stderr)
line = input()

#print(line[:4])
# Skipping non-cmd inputs
while line[:4] != "CMD_":
    line = input()

# 1. get array len
if "CMD_GET_DIM" not in line:
    TAc.print(LANG.render_feedback("no-array-input-first", f'No! Right now I was expecting you to ask the length of the array.'), "yellow", ["bold"])
    exit(0)
else:
    print(len(array))

# 2


must_compare = True
i = 0
iters = len(array) - 1
while iters > 0:
    line = input()
    
    print(f"line: {line}", file=sys.stderr)
    '''
    print(array, file=sys.stderr)
    print(f"must-comp: {must_compare}", file=sys.stderr)
    '''
    # Skipping non-cmd inputs
    while line[:4] != "CMD_": 
        line = input()

    if("CMD_FINISHED" in line or iters == 0):
        break

    # Checking compare
    if(must_compare):
        if("CMD_COMPARE_CONSEC_ELEM" in line):
            idx = line[len("CMD_COMPARE_CONSEC_ELEM "):] # DOMANDA: e se mi passano parametri sbagliati?
            idx = int(idx)
            # Checking wrong index
            if(idx != i):
                TAc.print(LANG.render_feedback("cmp-wrong-idx", f'No! Right now I was expecting the compare element at position {i} with {i+1}'), "yellow", ["bold"])
                exit(0)
            
            cmp = array[idx] > array[idx+1]
            print(cmp)
            print(f"__{array[idx]} > {array[idx+1]} = {cmp}", file=sys.stderr)

            # Next step is swap or compare?
            must_compare = not cmp
        else:
            print("expecting compare", file=sys.stderr)
            TAc.print(LANG.render_feedback("no-cmp", f'No! Right now I was expecting the compare of two consecutive elements.'), "yellow", ["bold"])
            exit(0)
    else: # Swap
        if("CMD_SWAP_CONSEC_ELEM" in line):
            idx = line[len("CMD_SWAP_CONSEC_ELEM "):] # DOMANDA: e se mi passano parametri sbagliati?
            idx = int(idx)

            # Checking wrong index
            if(idx != i):
                TAc.print(LANG.render_feedback("cmp-wrong-idx", f'No! Right now I was expecting the compare element at position {i} with {i+1}'), "yellow", ["bold"])
                exit(0)

            array[i], array[i+1] = array[i+1], array[i]
            # Next step is compare
            must_compare = True
        else:
            print("expecting swap", file=sys.stderr)
            TAc.print(LANG.render_feedback("no-swap", f'No! Right now I was expecting the swap of two consecutive elements.'), "yellow", ["bold"])
            exit(0)
    
    # Next element to compare
    if(must_compare):
        i += 1
        if(i > len(array)- 2):
            i = 0
            iters -= 1

# TODO: controllare se array è ordinato

TAc.print(LANG.render_feedback("final-congrats",'CONGRATS! You\'ve successfully used BubbleSort. \u2714'), "yellow", ["bold"])
exit(0)