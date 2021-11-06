#!/usr/bin/env python3
from sys import argv


class InsertionSortMachine:
    def __init__(self):
        self.tmp_buffer = None
        self.working_array = []

    def load_next_input_element_in_tmp_buffer(self, val: int):
        if self.tmp_buffer is not None:
            print(
                "Ahi, my problem-solver bot is overwriting a yet unflushed value stored in the tmp_buffer. This is going to erase information which will be definitely lost it in the Insertion Sort algorithm approach.")
        self.tmp_buffer = val
        print(f"#LOG_load_next_input_element_in_tmp_buffer (got {val})")

    def flush_tmp_buffer_on_pos(self, i: int):
        if self.tmp_buffer is None:
            print(
                "Ahi, my problem-solver bot is flushing an empty tmp_buffer. I expect complaints from the checking server.")
        while len(self.working_array) <= i:
            self.working_array.append(None)
        self.working_array[i] = self.tmp_buffer
        self.tmp_buffer = None
        print(f"#LOG_flush_tmp_buffer_on_pos {i}")

    def clone_to_its_right_ele_in_pos(self, i: int):
        if not 0 <= i < len(self.working_array):
            print(
                f"Ahi, my problem-solver bot is asking to clone the element in pos {i} which does not exists since {i} is not in the interval [0,{len(self.working_array)}).")
        if len(self.working_array) == i+1:
            self.working_array.append(self.working_array[i])
        else:
            self.working_array[i + 1] = self.working_array[i]
        print(f"#LOG_clone_to_its_right_ele_in_pos {i}")

    def what_in_tmp_buffer_goes_before_than_what_in_pos(self, i: int):
        if self.tmp_buffer is None:
            print(
                "Ahi, my problem-solver bot asks to compare with others the element contained in the tmp_buffer, but this buffer is empty. I expect complaints from the checking server.")
            return False
        if i >= len(self.working_array) or self.working_array[i] is None:
            print(
                f"Ahi, my problem-solver bot asks to compare with others the element contained in position {i} of the current working array. However, no element has ever been placed in this position of the array. I expect complaints from the checking server.")
            return False
        if self.tmp_buffer < self.working_array[i]:
            print(f"#LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} (<)")
            return True
        print(f"#LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} (>=)")
        return False

    def output_final_array(self):
        print(f"#LOG_output_final_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})")


if __name__ == "__main__":
    input_filename = argv[1]
    fin = open(input_filename, "r")
    ext_array_of_int = list(map(int, fin.readline().strip().split()))
    fin.close()
    N = len(ext_array_of_int)
    SM = InsertSortingMachine()
    n_ordered = 0
    while n_ordered < N:
        SM.load_next_input_element_in_tmp_buffer(ext_array_of_int[n_ordered])
        pos_cmp = n_ordered - 1
        while pos_cmp >= 0 and SM.what_in_tmp_buffer_goes_before_than_what_in_pos(pos_cmp):
            SM.clone_to_its_right_ele_in_pos(pos_cmp)
            pos_cmp -= 1
        SM.flush_tmp_buffer_on_pos(pos_cmp + 1)
        n_ordered += 1
    SM.output_final_array()
