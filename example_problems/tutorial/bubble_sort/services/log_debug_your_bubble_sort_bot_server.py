#!/usr/bin/env python3
from sys import exit
from time import sleep

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import bubble_sort_lib

# METADATA OF THIS TAL_SERVICE:
problem = "bubble_sort"
service = "log_debug_a_single_bubble_sort_phase"
args_list = [
    ('feedback', str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

BSM = bubble_sort_lib.BubbleSortMachine([])
ins_sort_ref_iterator = BSM.generate_log_while_sorting()
finished = False

array = None
# Control flags
cmp_pos = 0
must_swap = False

# 1. controllo che prenda in input
line = input()
while line[:5] != "LOG_": # Skipping non-log inputs
    line = input()

if "LOG_input_array" not in line:
    TAc.print(LANG.render_feedback("no-array-input-first", f'No! Right now I was expecting the loading of the unordered array.'), "yellow", ["bold"])
    exit(0)

# Getting array
array = line[len("LOG_input_array got [")+1:-2].split(", ")
array = [int(elem) for elem in array]


#print("1. Input array - ok")
while not finished:
    line = input()
    # Skipping non-log inputs
    while line[:5] != "LOG_" or "LOG_output_array" in line: 
        line = input()

    # 3. Output
    #print("[bot out] "+ line)
    if("LOG_output_final_sorted_array" in line):
        bot_sorted = line[len("LOG_output_final_sorted_array")+1:]
        bot_sorted = bot_sorted.split(":")[1]
        bot_sorted = bot_sorted[:-1].split()
        bot_sorted = [int(elem) for elem in bot_sorted]

        finished = True # praticamente inutile
        break

    # 2. Compare/swap
    if(not must_swap): # Compare
        if("LOG_compare_consecutive_elements" in line):
            # prendo il primo elemento
            first_pos = line[len("LOG_compare_consecutive_elements ")+1:]
            first_pos = int(first_pos.split(" ")[0])

            #print(f"cmp - pos {first_pos}- cmp_pos: {cmp_pos}")

            # Controllo elementi confrontati
            if(first_pos != cmp_pos):
                TAc.print(LANG.render_feedback("wrong-compare-elem", f'No! I wasn\'t expected to compare element at position {first_pos} with the next one, the right one was {cmp_pos}.'), "yellow", ["bold"])
                exit(0)
            
            # capisco se elem in 1a pos deve swappare con il 2o
            if(">=" in line):
                must_swap = True
            else:
                must_swap = False

        else: # Wrong
            TAc.print(LANG.render_feedback("no-cmp", f'No! Right now I was expecting the compare of the next elements'), "yellow", ["bold"])
            exit(0)
    else: # Checking swap
        # Eseguo swap in locale
        array[cmp_pos], array[cmp_pos+1] = array[cmp_pos+1], array[cmp_pos]
        
        if("LOG_swap_consecutive_elements" in line):
            bot_first_pos = int(line[len("LOG_swap_consecutive_elements")+1:].split()[0])
            #print(f"swap - pos: {bot_first_pos} - cmp_pos: {cmp_pos}")
            must_swap = False
            if(bot_first_pos != cmp_pos):
                TAc.print(LANG.render_feedback("swap-wrong-pos", f'No! Right now I was expecting to swap element at pos {cmp_pos} with {cmp_pos+1}'), "yellow", ["bold"])
                exit(0)
        else:
            TAc.print(LANG.render_feedback("no-swap", f'No! Right now I was expecting to swap element at pos {cmp_pos}'), "yellow", ["bold"])
            exit(0)
    # aggiorno posizione 
    if(not must_swap):
        cmp_pos += 1
        if(cmp_pos > len(array)-2):
            cmp_pos = 0

if(bot_sorted == array):
    TAc.print(LANG.render_feedback("final-congrats",'CONGRATS! The log sent to the service id fully coherent with the execution of BubbleSort. \u2714'), "yellow", ["bold"])
    exit(0)
else:
    TAc.print(LANG.render_feedback("wrong-final",'Ahi! You sent me a wrong solution, the right one was {array}'), "yellow", ["bold"])
    exit(0)
