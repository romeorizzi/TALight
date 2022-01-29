#!/usr/bin/env python3

from re import I
from sys import stdout, stderr, exit, argv


class BubbleSortMachine:
    def __init__(self, input_array):
        self.working_array = input_array
        self.log = []

    def swap_consecutive_elements(self, first_position: int):
        second_position = first_position + 1
        self.working_array[first_position], self.working_array[second_position] = self.working_array[second_position], self.working_array[first_position]
        self.log.append(f"LOG_swap_consecutive_elements {first_position} {second_position}")
    
    def compare_consecutive_elements(self, first_position: int):
        """Compares element at 'first_position' parameter with the next one."""
        second_position = first_position + 1

        if self.working_array[first_position] < self.working_array[second_position]:
            self.log.append(f"LOG_compare_consecutive_elements {first_position} (<) {second_position}")
            return True
        self.log.append(f"LOG_compare_consecutive_elements {first_position} (>=) {second_position}")
        return False

    def generate_log_while_sorting(self):
        self.log.append(f"LOG_input_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})")
        yield self.log[-1]
        swap = True
        right_pos = 1
        while swap:
            swap = False
            print(self.working_array)
            for i in range(len(self.working_array) - right_pos):
                if(not self.compare_consecutive_elements(i)):
                    self.swap_consecutive_elements(i)
                    swap = True
                    yield self.log[-1]
            right_pos += 1
        self.log.append(f"LOG_output_final_sorted_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})")
        yield self.log[-1]

if __name__ == "__main__":
    input_filename = argv[1]
    fin = open(input_filename, "r")
    N = int(fin.readline())
    input_array_of_ints = list(map(int, fin.readline().strip().split()))
    fin.close()
    assert N == len(input_array_of_ints)
    bubble_sort = BubbleSort(input_array_of_ints)
    for st in bubble_sort.generate_log_while_sorting():
        print(st)
    print("\nNOW, AFTER WHOLE EXECUTION, LET'S PRINT AGAIN THE WHOLE LOG:")
    for st in bubble_sort.log:
        print(st)
