#!/usr/bin/env python3

from sys import stdout, stderr, exit, argv
from os import environ
import random

class InsertSort:
    def __init__(self, input_array):
        self.n = 0
        self.working_array = []
        self.tmp_buffer = None
        self.input_stream = input_array
        self.log = []


    def load_next_element_in_tmp_buffer(self):
        if len(self.input_stream) == 0:
            self.log.append(f"LOG_load_next_input_element_in_tmp_buffer NO MORE")
            return False
        else:
            self.tmp_buffer = self.input_stream[0]
            self.input_stream = self.input_stream[1:]
            self.log.append(f"LOG_load_next_input_element_in_tmp_buffer OK, got {self.tmp_buffer}")
            self.n += 1
            self.working_array.append(None)
            return True            

    def flush_tmp_buffer_ele_in_pos(self, pos):
        self.working_array[pos] = self.tmp_buffer
        self.log.append(f"LOG_flush_tmp_buffer_on_pos {pos}")

    def overwrite_on_the_right_what_in_pos(self, pos):
        self.working_array[pos+1] = self.working_array[pos]
        self.log.append(f"LOG_clone_ele_in_pos {pos} one_step_to_the_right")

    def what_in_tmp_buffer_goes_before_than_what_in_pos(self, pos):
        if self.working_array[pos] < self.tmp_buffer:
            self.log.append(f"LOG_compare_what_in_pos {pos} with_what_in_tmp_buffer <")
            return False
        elif self.working_array[pos] > self.tmp_buffer:
            self.log.append(f"LOG_compare_what_in_pos {pos} with_what_in_tmp_buffer >")
            return True
        else:
            self.log.append(f"LOG_compare_what_in_pos {pos} with_what_in_tmp_buffer =")
            return False
        
        self.working_array[pos+1] = self.working_array[pos]
        
    def generate_log_when_sorting(self):
        while self.load_next_element_in_tmp_buffer():
            curr_pos = self.n-1
            while curr_pos > 0 and self.what_in_tmp_buffer_goes_before_than_what_in_pos(curr_pos-1):
                self.overwrite_on_the_right_what_in_pos(curr_pos-1)
                curr_pos -= 1
            self.flush_tmp_buffer_ele_in_pos(curr_pos)
        self.log.append(f"LOG_output_final_array {len(self.working_array)} {' '.join(map(str,self.working_array))}")
        return self.log

    
if __name__ == "__main__":
    input_array = list(map(int,argv[1:])) 
    insert_sort = InsertSort(input_array)
    log=insert_sort.generate_log_when_sorting()
    print(log)
