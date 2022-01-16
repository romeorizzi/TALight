#!/usr/bin/env python3
from sys import argv
from time import sleep

from template_lib import BubbleSortMachine

usage=f"""Call me like this:
   > {argv[0]}  [ <input_filename> [wait_for_receipt] ]

   The two (optional) arguments are as follows:
   <input_filename> provides the fullname of a file where the input is stored. This file comprises two lines:
       -the first line contains the number <n> of integers to be sorted. 
       -the second line contains <n> integer numbers separated by spaces.

   [wait_for_receipt] whenever you provide a second argument (its face value is not even checked) then the InsertionSort bot will wait for confirmation at every log step of the InsertionSortMachine it operates.
"""
# Args
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
require_receipt = len(argv) > 2

assert N == len(input_array_of_ints)
SM = BubbleSortMachine()

SM.input_array(input_array_of_ints, wait_for_receipt=require_receipt)

swap = True
right_pos = 1
while swap:
    swap = False

    for i in range(len(input_array_of_ints)-right_pos):
        if(not SM.compare_consecutive_elements(i, wait_for_receipt=require_receipt)):
            SM.swap_consecutive_elements(i, wait_for_receipt=require_receipt)
            swap = True
        SM.output_array(wait_for_receipt=require_receipt)
    print ("end FOR")
    right_pos += 1
SM.output_final_sorted_array(wait_for_receipt=require_receipt)

sleep(1)
