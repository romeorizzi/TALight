#!/usr/bin/env python3
from sys import argv, stderr

from insertion_sort_machine_lib import InsertionSortMachine

usage=f"""Call me like this:
   > {argv[0]}  [wait_for_prompt]

   The optional argument is as follows:
      [wait_for_prompt] whenever you provide a second argument (its face value is not even checked) then the InsertionSort bot will wait for confirmation at every log step of the InsertionSortMachine it operates.
"""

if len(argv) > 2:
    print(f"Error: you called this executable ({argv[0]}) providing too many arguments ({len(argv)-1} arguments received).")
    print(usage)
    exit(1)


require_prompt = len(argv) > 1
SM = InsertionSortMachine(input_array_of_ints, wait_for_prompt=require_prompt)

n_ordered = 0
while SM.load_next_input_element_in_tmp_buffer() != 0:
    pos_cmp = n_ordered - 1
    while pos_cmp >= 0 and SM.compare_ele_in_tmp_buffer_with_ele_in_pos(pos_cmp):
        SM.clone_to_its_right_ele_in_pos(pos_cmp)
        pos_cmp -= 1
    SM.flush_tmp_buffer_ele_in_pos(pos_cmp + 1)
    n_ordered += 1
SM.output_final_sorted_array()

