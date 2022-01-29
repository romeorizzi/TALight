#!/usr/bin/env python3
from sys import argv
from time import sleep

from template_lib import BubbleSortMachine

usage=f"""I am an implementation of the first phase of the BubbleSort algorithm. Call me like this:
   > {argv[0]}  [ <input_filename> [wait_for_prompt] ]

   The two (optional) arguments are as follows:
   <input_filename> provides the fullname of a file where the input array is stored. This file comprises two lines:
         -the first line contains the number <n> of integers to be sorted. 
         -the second line contains <n> integer numbers separated by spaces.
       When no argument is given, the input array is taken from stdin, according to the same format.

   [wait_for_prompt] whenever you provide a second argument (its face value is not even checked) then the bot will wait for a prompt at every, before operating the Sorting Machine primitive and printing the corresponding LOG line.
"""

if len(argv) > 3:
    print(f"Error: you called this executable ({argv[0]}) providing too many arguments ({len(argv)-1} arguments received).")
    print(usage)
    exit(1)

if len(argv) < 2:
    N = int(input())
    input_array_of_ints = list(map(int, input().split()))
else:
    input_filename = argv[1]
    fin = open(input_filename, "r")
    N = int(fin.readline())
    input_array_of_ints = list(map(int, fin.readline().strip().split()))
    fin.close()
    
require_prompt = len(argv) > 2
assert N == len(input_array_of_ints)
BSM = BubbleSortMachine(wait_for_prompt=require_prompt)
BSM.input_array(input_array_of_ints)

for i in range(N-2):
    BSM.sort_consecutive_pair(i)
N -= 1
BSM.output_array_after_one_single_pass()

