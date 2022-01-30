#!/usr/bin/env python3
from sys import argv
from time import sleep
import unittest

from bot_lib import Bot

class BubbleSortMachine:
    def __init__(self, wait_for_prompt=False):
        self.working_array = []
        self.log = []
        self.BOT = Bot(report_inputs = wait_for_prompt,reprint_outputs = wait_for_prompt, BOT_prefix_to_reported_input_line="SERVER> ",BOT_prefix_to_printed_lines="BOT> ", empty_line_is_comment = False)
        self.wait_for_prompt = wait_for_prompt

    def console(self, log_msg):
        """This method is called by each basic primitive of the abstract Sorting Machine. The method implementing the primitive calls the console method in order to print the LOG message associated with the primitive.
           If self.wait_for_prompt = True then the bot waits for an input line (not beginning with '#') before printing the LOG.
        """ 
        if self.wait_for_prompt:
            line = self.BOT.input()
        else:
            sleep(0.1)
        self.BOT.print(log_msg)
        self.log.append(log_msg)


    # Input vettore
    def input_array(self, vector: list):
        if vector is None or len(vector) == 0:
            self.BOT.print("Ahi, the operator required to insert a non existent working array.")
        self.working_array = vector
        self.console(f"LOG_input_array ({len(vector)}: {' '.join(map(str,vector))})")

    # Display vettore
    def display_array(self):
        if self.working_array is None or len(self.working_array) == 0:
            self.BOT.print("Ahi, the operator required to get a non existent working array.")
            return None
        self.console(f"LOG_display_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})")
        return self.working_array
    
    # Output Final Sorted
    def output_final_sorted_array(self):
        self.console(f"LOG_output_final_sorted_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})")

    # Output After One Single Pass
    def output_array_after_one_single_pass(self):
        self.console(f"LOG_output_array_after_one_single_pass ({len(self.working_array)}: {' '.join(map(str,self.working_array))})")

    # Sort 2 consecutive elements
    def sort_consecutive_pair(self, first_position: int):
        second_position = first_position + 1        
        # Checking positions
        if not 0 <= first_position < len(self.working_array):
            self.BOT.print(f"Ahi, the operator required to sort the elements in pos {first_position} and {second_position}, but {first_position} is not in the interval [0,{len(self.working_array)}).")
        if not 0 <= second_position < len(self.working_array):
            self.BOT.print(f"Ahi, the operator required to switch the elements in pos {second_position}, but {second_position} is not in the interval [0,{len(self.working_array)}).")
        # Sorting
        if self.working_array[first_position] > self.working_array[second_position]:
            self.working_array[first_position], self.working_array[second_position] = self.working_array[second_position], self.working_array[first_position]
        
        self.console(f"LOG_sort_pair_of_consecutive_elements_at_pos {first_position} {second_position}")
        
    # Swap consecutive elements
    def swap_consecutive_elements(self, first_position: int):
        second_position = first_position + 1
        
        # Checking positions
        if not 0 <= first_position < len(self.working_array):
            self.BOT.print(f"Ahi, the operator required to swap the elements in pos {first_position} and {second_position}, but is not in the interval [0,{len(self.working_array)}).")
        if not 0 <= second_position < len(self.working_array):
            self.BOT.print(f"Ahi, the operator required to swap the elements in pos {first_position} and {second_position}, but {second_position} is not in the interval [0,{len(self.working_array)}).")
        
        # Swapping
        self.working_array[first_position], self.working_array[second_position] = self.working_array[second_position], self.working_array[first_position]
        
        self.console(f"LOG_swap_consecutive_elements {first_position} {second_position}")
    
    # Compare consecutive elements
    def compare_consecutive_elements(self, first_position: int):
        """Compares element at 'first_position' parameter with the next one."""
        second_position = first_position + 1
        
        if self.working_array is None:
            self.BOT.print(
                "Ahi, the operator required to compare with others the element contained in the working_array, but this buffer is empty. I expect complaints from the checking server.")
            return False
        # Checking first element's existence
        if first_position >= len(self.working_array) or self.working_array[first_position] is None:
            self.BOT.print(
                f"Ahi, the operator required to compare element contained in position {first_position} with its next element of the current working array. However, no element has ever been placed in this position of the array. I expect complaints from the checking server.")
            return False
        # Checking second element's existence
        if second_position >= len(self.working_array) or self.working_array[second_position] is None:
            self.BOT.print(
                f"Ahi, the operator required to compare {second_position} with it previous element of the current working array. However, no element has ever been placed in this position of the array. I expect complaints from the checking server.")
            return False

        if self.working_array[first_position] < self.working_array[second_position]:
            self.console(f"LOG_compare_consecutive_elements {first_position} (<) {second_position}")
            return True
        self.console(f"LOG_compare_consecutive_elements {first_position} (>=) {second_position}")
        return False


if __name__ == "__main__":
    print("UNIT TEST")

    tc = unittest.TestCase()

    print("\nTEST 1: operating the InsertionSortMachine to sort <4: 12 11 15 13>")

    expected_logs = [
        "TODO"
    ]

    SM = BubbleSortMachine()
   
   # TODO
