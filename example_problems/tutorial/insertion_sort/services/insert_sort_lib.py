#!/usr/bin/env python3
from sys import stdout, stderr, exit, argv

from bot_lib import Bot


class InsertionSort:
    def __init__(self, input_array):
        self.input_stream = input_array
        self.tmp_buffer = None
        self.working_array = []
        self.log = []

    def append_to_input_stream(self, new_ele: int):
        self.input_stream.append(new_ele)        
        
    def input_stream_is_empty(self):
        return len(self.input_stream) == 0
        
    def load_next_input_element_in_tmp_buffer(self):
        assert not self.input_stream_is_empty()
        self.tmp_buffer = self.input_stream[0]
        self.input_stream = self.input_stream[1:]
        self.log.append(f"LOG_load_next_input_element_in_tmp_buffer (got {self.tmp_buffer})")
        self.working_array.append(None)

    def flush_tmp_buffer_ele_in_pos(self, pos):
        self.working_array[pos] = self.tmp_buffer
        self.log.append(f"LOG_flush_tmp_buffer_on_pos {pos}")

    def overwrite_on_the_right_what_in_pos(self, pos):
        self.working_array[pos+1] = self.working_array[pos]
        self.log.append(f"LOG_clone_to_its_right_ele_in_pos {pos}")

    def what_in_tmp_buffer_goes_before_than_what_in_pos(self, pos):
        if self.tmp_buffer < self.working_array[pos]:
            self.log.append(f"LOG_compare_what_in_tmp_buffer_with_what_in_pos {pos} (<)")
            return True
        self.log.append(f"LOG_compare_what_in_tmp_buffer_with_what_in_pos {pos} (>=)")
        return False

    def generate_log_while_sorting(self):
        while not self.input_stream_is_empty():
            self.load_next_input_element_in_tmp_buffer()
            yield self.log[-1]
            curr_pos = len(self.working_array)-1
            while curr_pos > 0 and self.what_in_tmp_buffer_goes_before_than_what_in_pos(curr_pos-1):
                yield self.log[-1]
                self.overwrite_on_the_right_what_in_pos(curr_pos-1)
                yield self.log[-1]
                curr_pos -= 1
            if curr_pos > 0:
                yield self.log[-1]
            self.flush_tmp_buffer_ele_in_pos(curr_pos)
            yield self.log[-1]
        self.log.append(f"LOG_output_final_sorted_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})")
        yield self.log[-1]


if __name__ == "__main__":
    input_filename = argv[1]
    fin = open(input_filename, "r")
    N = int(fin.readline())
    input_array_of_ints = list(map(int, fin.readline().strip().split()))
    fin.close()
    assert N == len(input_array_of_ints)
    insertion_sort = InsertionSort(input_array_of_ints)
    for st in insertion_sort.generate_log_while_sorting():
        print(st)
    print("\nNOW, AFTER WHOLE EXECUTION, LET'S PRINT AGAIN THE WHOLE LOG:")
    for st in insertion_sort.log:
        print(st)
