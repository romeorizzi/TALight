#!/usr/bin/env python3
from sys import argv


class InsertSortingMachine:
    def __init__(self, N):
        self.N = N
        self.tmp_buffer = None
        self.n = 0
        self.int_array_of_int = [None] * N

    def load_next_input_element_in_tmp_buffer(self, val: int):
        if self.tmp_buffer is not None:
            print(
                "Ahi, my problem-solver bot is overwriting a yet unflushed value stored in the tmp_buffer. This is going to erase information which will be definitely lost it in the Insertion Sort algorithm approach.")
        self.tmp_buffer = val
        self.n += 1
        print(f"#LOG_load_next_input_element_in_tmp_buffer {val}")

    def flush_tmp_buffer_on_pos(self, i: int):
        if self.tmp_buffer is None:
            print(
                "Ahi, my problem-solver bot is flushing an empty tmp_buffer. I expect complaints from the checking server.")
        self.int_array_of_int[i] = self.tmp_buffer
        self.tmp_buffer = None
        print(f"#LOG_flush_tmp_buffer_on_pos {i}")

    def clone_to_its_right_ele_in_pos(self, i: int):
        if not 0 <= i < self.n:
            print(
                f"Ahi, my problem-solver bot is asking to clone the element in pos {i} which does not exists since {i} is not in the interval [0,{self.n}).")
        self.int_array_of_int[i + 1] = self.int_array_of_int[i]
        print(f"#LOG_clone_to_its_right_ele_in_pos {i}")

    def compare_what_in_tmp_buffer_with_what_in_pos(self, i: int):
        if self.tmp_buffer is None:
            print(
                "Ahi, my problem-solver bot is comparing an element with an empty tmp_buffer. I expect complaints from the checking server.")

        if self.tmp_buffer > self.int_array_of_int[i]:
            print(f"#LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} >")
            return False

        elif self.tmp_buffer < self.int_array_of_int[i]:
            print(f"#LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} <")
            return True

        else:
            print(f"#LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} =")
            return True

    def output_final_array(self):
        print(f"#LOG_output_final_array {self.int_array_of_int}")


if __name__ == "__main__":
    input_filename = argv[1]
    fin = open(input_filename, "r")
    ext_array_of_int = list(map(int, fin.readline().strip().split()))
    fin.close()
    N = len(ext_array_of_int)
    SM = InsertSortingMachine(N)
    n_ordered = 0
    while n_ordered < N:
        SM.load_next_input_element_in_tmp_buffer(ext_array_of_int[n_ordered])
        pos_cmp = n_ordered - 1
        while pos_cmp >= 0 and SM.compare_what_in_tmp_buffer_with_what_in_pos(pos_cmp):
            SM.clone_to_its_right_ele_in_pos(pos_cmp)
            pos_cmp -= 1
        SM.flush_tmp_buffer_on_pos(pos_cmp + 1)
        n_ordered += 1
    SM.output_final_array()
