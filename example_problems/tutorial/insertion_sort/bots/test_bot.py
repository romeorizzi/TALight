#!/usr/bin/env python3
from sys import argv
from time import sleep

from template_lib import InsertionSortMachine

input_filename = argv[1]
fin = open(input_filename, "r")
N = int(fin.readline())
input_array_of_ints = list(map(int, fin.readline().strip().split()))
fin.close()
assert N == len(input_array_of_ints)
SM = InsertionSortMachine()
n_ordered = 0
while n_ordered < N:
    SM.load_next_input_element_in_tmp_buffer(int(input_array_of_ints[n_ordered]))
    pos_cmp = n_ordered - 1
    while pos_cmp >= 0 and SM.what_in_tmp_buffer_goes_before_than_what_in_pos(pos_cmp):
        SM.clone_to_its_right_ele_in_pos(pos_cmp)
        pos_cmp -= 1
    SM.flush_tmp_buffer_on_pos(pos_cmp + 1)
    n_ordered += 1
SM.output_final_array()

sleep(1)
