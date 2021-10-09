#!/usr/bin/env python3

class InsertSortingMachine:
    def __init__(N):
        self.N = N
        self.tmp_buffer = None
        self.n = 0
        self.int_array_of_int = [ None * N ] 

    def load_next_input_element_in_tmp_buffer(val : int):
        if self.tmp_buffer!=None:
            print("Ahi, my problem-solver bot is overwriting a yet unflushed value stored in the tmp_buffer. This is going to erase information which will be definitely lost it in the Insertion Sort algorithm approach.")
        self.tmp_buffer = val
        print(f"#LOG_load_next_input_element_in_tmp_buffer {val}")

    def flush_tmp_buffer_on_pos(i:int):
        if self.tmp_buffer==None:
            print("Ahi, my problem-solver bot is flushing an empty tmp_buffer. I expect complaints from the checking server.")
        self.a_of_int[i] = self.tmp_buffer
        self.tmp_buffer = None
        print(f"#LOG_flush_tmp_buffer_on_pos {i}")

    def clone_to_its_right_ele_in_pos(i:int):    
        if not 0 <= i < self.n:
            print(f"Ahi, my problem-solver bot is asking to clone the element in pos {i} which does not exists since {i} is not in the interval [0,{self.n}).")
        print(f"#LOG_clone_to_its_right_ele_in_pos {i}")

    def compare_what_in_tmp_buffer_with_what_in_pos(i:int):    
        print(f"#LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} <outcome>")

    def output_final_array():    
        print(f"#LOG_output_final_array <final_array>")

if __name__=="main":
    input_filename = argv[1]
    fin = open(input_filename,"r")
    ext_array_of_int = list(map(int,fin.readline().strip().split()))
    fin.close()
    N = len(ext_array_of_int)
    SM = InsertSortingMachine(N) 
    n_ordered = 0
    while n_ordered < N:
        SM.load_next_input_element_in_tmp_buffer()
        pos_cmp = n_ordered-1
        while pos_cmp >= 0 and SM.compare_what_in_tmp_buffer_with_what_in_pos(pos_cmp):
            SM.clone_to_its_right_ele_in_pos(pos_cmp)
        SM.flush_tmp_buffer_on_pos(pos_cmp+1)
    SM.output_final_array()
