#!/usr/bin/env python3
from sys import exit
import re
import numpy as np
from itertools import zip_longest
import insert_sort_lib
import log_debug_your_insertion_sort_bot_server
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from sys import stdout, stderr, exit, argv

# METADATA OF THIS TAL_SERVICE:
problem = "insert_sort"
service = "log_debug_your_insertion_sort_bot_server"
args_list = [
    ('feedback', str),
    ('lang', str),
    ('goal', str)
]


# ENV = Env(problem, service, args_list)
# TAc = TALcolors(ENV)
# LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# TODO: L'esercizio è molto simile al precedente, perchè non riciclare log_debug_your_insertion_sort_bot cambiando le primitive?

print("Our instance is: ")
input_array = np.random.randint(1, 100, np.random.randint(1, 10))
print(input_array)
print("Now you have to create the file with your insert sort solution. Type the name of the file when you finish.")
try:
    filename = input()
    goal = "adhere_to_insert_sort_algorithm"
    feedback = "tell_whats_right_instead"
    if goal == "adhere_to_insert_sort_algorithm":
        if feedback == "tell_whats_right_instead":
            debug = log_debug_your_insertion_sort_bot_server.DebugYourInsertSort(input_array, filename, "tell_whats_right_instead")
            print(debug.check_if_insert_sort())
        elif feedback == "just_signal_first_error":
            debug = log_debug_your_insertion_sort_bot_server.DebugYourInsertSort(input_array, filename, "just_signal_first_error")
            print(debug.check_if_insert_sort())
    elif goal == "just sort the array":
        insert_sort = insert_sort_lib.InsertSort(input_array)
        for line in insert_sort.generate_log_when_sorting():
            if "LOG_output_final_array " in line:
                print("Length: " + line[23:][0] + "\nSorted array: " + line[23:][2:])
except FileNotFoundError:
    print("File not found.")
    exit(1)
