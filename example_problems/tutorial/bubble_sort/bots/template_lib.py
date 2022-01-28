#!/usr/bin/env python3
from sys import argv, stderr
from time import sleep
import unittest

from bot_lib import Bot

class BubbleSortMachine:
    def __init__(self):
        self.working_array = []
        self.test_logs = []
        self.BOT = Bot(report_inputs=True,reprint_outputs=True)

    def console(self, log_msg, wait_for_receipt: bool, expected_log: str = None):
        """This method is used by each basic primitive of the abstract Machine meant to be operated by the algorithm object of study, for which the machine has been designed.
           The method implementing the primitive calls the console method in order to print the LOG message associated with the primitive.
           After printing the LOG, the bot can be made to wait for an answer by passing wait_for_receipt = True.
           The argument <expected_log> is used for self-testing (e.g., in unit testing). 
        """ 
        assert expected_log is None or log_msg == expected_log
        self.BOT.print(log_msg)
        sleep(0.2)
        self.test_logs.append(log_msg)
        if wait_for_receipt:
            print("Insert a feedback line (or just press RETURN) to continue ...")
            self.BOT.input()

    # 1.  scabio di elementi consecutivi
    def swap_consecutive_elements(self, first_position: int, wait_for_receipt: bool = True, expected_log: str = None):
        second_position = first_position + 1
        
        # Checking positions
        if not 0 <= first_position < len(self.working_array):
            self.BOT.print(f"Ahi, the operator required to switch elements in pos {first_position} and {second_position}, but {first_position} (and therefore same for {second_position}) is not in the interval [0,{len(self.working_array)}).")
        if not 0 <= second_position < len(self.working_array):
            self.BOT.print(f"Ahi, the operator required to switch elements in pos {first_position} and {second_position}, but {second_position} is not in the interval [0,{len(self.working_array)}).")
        
        # Swapping
        self.working_array[first_position], self.working_array[second_position] = self.working_array[second_position], self.working_array[first_position]
        
        self.console(f"#LOG_swap_consecutive_elements {first_position} {second_position}", wait_for_receipt, expected_log)
    
    # 2.  confronto di elementi consecutivi
    def compare_consecutive_elements(self, first_position: int, wait_for_receipt: bool = True, expected_log: str = None):
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
            self.console(f"#LOG_compare_consecutive_elements {first_position} (<) {second_position}", wait_for_receipt, expected_log)
            return True
        self.console(f"#LOG_compare_consecutive_elements {first_position} (>=) {second_position}", wait_for_receipt, expected_log)
        return False

    # 3. Input vettore
    def input_array(self, vector: list, wait_for_receipt: bool = True, expected_log: str = None):
        if vector is None or len(vector) == 0:
            self.BOT.print("Ahi, the operator required to insert a non existent working array.")
        self.working_array = vector
        self.console(f"#LOG_input_array (got {vector})", wait_for_receipt, expected_log)

    # 4. Display vettore
    def display_array(self, wait_for_receipt: bool = True, expected_log: str = None):
        if self.working_array is None or len(self.working_array) == 0:
            self.BOT.print("Ahi, the operator required to get a non existent working array.")
            return None
        self.console(f"#LOG_output_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})", wait_for_receipt, expected_log)
        return self.working_array
    
    # Output Final Sorted
    def output_final_sorted_array(self, wait_for_receipt: bool = True, expected_log: str = None):
        self.console(f"#LOG_output_final_sorted_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})", wait_for_receipt, expected_log)

    # Output After One Single Pass
    def output_array_after_one_single_pass(self, wait_for_receipt: bool = True, expected_log: str = None):
        self.console(f"#LOG_output_array_after_one_single_pass ({len(self.working_array)}: {' '.join(map(str,self.working_array))})", wait_for_receipt, expected_log)


if __name__ == "__main__":
    print("UNIT TEST")

    tc = unittest.TestCase()

    print("\nTEST 1: operating the InsertionSortMachine to sort <4: 12 11 15 13>")

    expected_logs = [
        "TODO"
    ]

    SM = BubbleSortMachine()
   
   # TODO
