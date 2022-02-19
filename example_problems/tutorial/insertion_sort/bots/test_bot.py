#!/usr/bin/env python3
from sys import argv

from insertion_sort_machine_lib import InsertionSortMachine

usage=f"""Call me like this:
   > {argv[0]}  [ <input_filename> [wait_for_prompt] ]

   The two (optional) arguments are as follows:
   <input_filename> provides the fullname of a file where the input is stored. This file comprises two lines:
         -the first line contains the number <n> of integers to be sorted. 
         -the second line contains <n> integer numbers separated by spaces.
       When no argument is given, the input array is taken from stdin, according to the same format.

   [wait_for_prompt] whenever you provide a second argument (its face value is not even checked) then the InsertionSort bot will wait for confirmation at every log step of the InsertionSortMachine it operates.
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
SM = InsertionSortMachine(input_array_of_ints, wait_for_prompt=require_prompt)

n_ordered = 0
while n_ordered < N:
    SM.load_next_input_element_in_tmp_buffer()
    pos_cmp = n_ordered - 1
    while pos_cmp >= 0 and SM.compare_ele_in_tmp_buffer_with_ele_in_pos(pos_cmp):
        SM.clone_to_its_right_ele_in_pos(pos_cmp)
        pos_cmp -= 1
    SM.flush_tmp_buffer_ele_in_pos(pos_cmp + 1)
    n_ordered += 1
SM.output_final_sorted_array()

