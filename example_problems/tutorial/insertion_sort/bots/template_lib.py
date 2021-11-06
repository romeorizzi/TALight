#!/usr/bin/env python3
from sys import argv
from time import sleep

class InsertionSortMachine:
    def __init__(self):
        self.tmp_buffer = None
        self.working_array = []

    def pause(self, wait_for_recipt: bool):
        if wait_for_recipt:
            print("Insert a feedback line (or just press RETURN) to continue ...")
            input()
            
    def load_next_input_element_in_tmp_buffer(self, val: int, wait_for_recipt: bool = True):
        if self.tmp_buffer is not None:
            print(
                "Ahi, my problem-solver bot is overwriting a yet unflushed value stored in the tmp_buffer. This is going to erase information which will be definitely lost it in the Insertion Sort algorithm approach.")
        self.tmp_buffer = val
        print(f"#LOG_load_next_input_element_in_tmp_buffer (got {val})")
        self.pause(wait_for_recipt)

    def flush_tmp_buffer_on_pos(self, i: int, wait_for_recipt: bool = True):
        if self.tmp_buffer is None:
            print(
                "Ahi, my problem-solver bot is flushing an empty tmp_buffer. I expect complaints from the checking server.")
        while len(self.working_array) <= i:
            self.working_array.append(None)
        self.working_array[i] = self.tmp_buffer
        self.tmp_buffer = None
        print(f"#LOG_flush_tmp_buffer_on_pos {i}")
        self.pause(wait_for_recipt)

    def clone_to_its_right_ele_in_pos(self, i: int, wait_for_recipt: bool = True):
        if not 0 <= i < len(self.working_array):
            print(
                f"Ahi, my problem-solver bot is asking to clone the element in pos {i} which does not exists since {i} is not in the interval [0,{len(self.working_array)}).")
        if len(self.working_array) == i+1:
            self.working_array.append(self.working_array[i])
        else:
            self.working_array[i + 1] = self.working_array[i]
        print(f"#LOG_clone_to_its_right_ele_in_pos {i}")
        self.pause(wait_for_recipt)

    def what_in_tmp_buffer_goes_before_than_what_in_pos(self, i: int, wait_for_recipt: bool = True):
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
            self.pause(wait_for_recipt)
            return True
        print(f"#LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} (>=)")
        self.pause(wait_for_recipt)
        return False

    def output_final_array(self, wait_for_recipt: bool = True):
        print(f"#LOG_output_final_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})")
        self.pause(wait_for_recipt)


if __name__ == "__main__":
    input_filename = argv[1]
    fin = open(input_filename, "r")
    N = int(fin.readline())
    input_array_of_ints = list(map(int, fin.readline().strip().split()))
    fin.close()
    assert N == len(input_array_of_ints)
    SM = InsertionSortMachine()
    n_ordered = 0
    while n_ordered < N:
        SM.load_next_input_element_in_tmp_buffer(input_array_of_ints[n_ordered], wait_for_recipt=True)
        pos_cmp = n_ordered - 1
        while pos_cmp >= 0 and SM.what_in_tmp_buffer_goes_before_than_what_in_pos(pos_cmp, wait_for_recipt=True):
            SM.clone_to_its_right_ele_in_pos(pos_cmp, wait_for_recipt=True)
            pos_cmp -= 1
        SM.flush_tmp_buffer_on_pos(pos_cmp + 1, wait_for_recipt=True)
        n_ordered += 1
    SM.output_final_array(wait_for_recipt=True)
    
    sleep(1)
