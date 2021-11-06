#!/usr/bin/env python3
from sys import argv

from template_lib import InsertionSortMachine

N = int(input())
SM = InsertionSortMachine()
n_ordered = 0
while n_ordered < N:
    SM.load_next_input_element_in_tmp_buffer(int(input()))
    pos_cmp = n_ordered - 1
    while pos_cmp >= 0 and SM.what_in_tmp_buffer_goes_before_than_what_in_pos(pos_cmp):
        SM.clone_to_its_right_ele_in_pos(pos_cmp)
        pos_cmp -= 1
    SM.flush_tmp_buffer_on_pos(pos_cmp + 1)
    n_ordered += 1
SM.output_final_array()
