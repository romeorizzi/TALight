#!/usr/bin/env python3
from sys import argv
from time import sleep

from template_lib import InsertionSortMachine

usage=f"""Call me like this:
   > {argv[0]}  [ <input_filename> [wait_for_recipt] ]

   The two (optional) arguments are as follows:
   <input_filename> provides the fullname of a file where the input is stored. This file comprises two lines:
       -the first line contains the number <n> of integers to be sorted. 
       -the second line contains <n> integer numbers separated by spaces.

   [wait_for_recipt] whenever you provide a second argument (its face value is not even checked) then the InsertionSort bot will wait for confirmation at every log step of the InsertionSortMachine it operates.
"""

#if len(argv) < 2:
#    print(f"Error: you called this executable ({argv[0]}) without providing any arguments.")
#    print(usage)
#    exit(1)
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

require_recipt = len(argv) > 2

assert N == len(input_array_of_ints)
SM = InsertionSortMachine()
n_ordered = 0
while n_ordered < N:
    SM.load_next_input_element_in_tmp_buffer(int(input_array_of_ints[n_ordered]), wait_for_recipt=require_recipt)
    pos_cmp = n_ordered - 1
    while pos_cmp >= 0 and SM.what_in_tmp_buffer_goes_before_than_what_in_pos(pos_cmp, wait_for_recipt=require_recipt):
        SM.clone_to_its_right_ele_in_pos(pos_cmp, wait_for_recipt=require_recipt)
        pos_cmp -= 1
    SM.flush_tmp_buffer_on_pos(pos_cmp + 1, wait_for_recipt=require_recipt)
    n_ordered += 1
SM.output_final_array(wait_for_recipt=require_recipt)

sleep(1)
