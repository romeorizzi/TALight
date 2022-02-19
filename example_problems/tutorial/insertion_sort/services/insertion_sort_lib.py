#!/usr/bin/env python3
import sys
import unittest

from insertion_sort_machine_lib import InsertionSortMachine

class InsertionSort_machine_plus_algo(InsertionSortMachine):
    def generate_log_while_sorting(self):
        while not self.input_stream_is_empty():
            self.load_next_input_element_in_tmp_buffer()
            yield self.log[-1]
            curr_pos = len(self.working_array)
            while curr_pos > 0 and self.compare_ele_in_tmp_buffer_with_ele_in_pos(curr_pos-1):
                yield self.log[-1]
                self.clone_to_its_right_ele_in_pos(curr_pos-1)
                yield self.log[-1]
                curr_pos -= 1
            if curr_pos > 0:
                yield self.log[-1]
            self.flush_tmp_buffer_ele_in_pos(curr_pos)
            yield self.log[-1]
        self.output_final_sorted_array()
        yield self.log[-1]


if __name__ == "__main__":
    input_filename = sys.argv[1]
    fin = open(input_filename, "r")
    N = int(fin.readline())
    input_array_of_ints = list(map(int, fin.readline().strip().split()))
    fin.close()
    assert N == len(input_array_of_ints)
    insertion_sort = InsertionSort_machine_plus_algo(input_array_of_ints, log_on_console=False)
    for st in insertion_sort.generate_log_while_sorting():
        print(st)
    print("\nNOW, AFTER WHOLE EXECUTION, LET'S PRINT AGAIN THE WHOLE LOG:")
    for st in insertion_sort.log:
        print(st)
