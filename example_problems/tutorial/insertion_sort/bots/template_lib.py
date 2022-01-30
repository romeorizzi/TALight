#!/usr/bin/env python3
from sys import argv
from time import sleep
import unittest

from bot_lib import Bot

class InsertionSortMachine():
    def __init__(self, wait_for_prompt=False):
        self.tmp_buffer = None
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

    def load_next_input_element_in_tmp_buffer(self, val: int):
        if self.tmp_buffer is not None:
            print(
                "Ahi, my problem-solver bot is overwriting a yet unflushed value stored in the tmp_buffer. This is going to erase information which will be definitely lost it in the Insertion Sort algorithm approach.")
        self.tmp_buffer = val
        self.console(f"LOG_load_next_input_element_in_tmp_buffer (got {val})")

    def flush_tmp_buffer_on_pos(self, i: int):
        if self.tmp_buffer is None:
            print(
                "Ahi, my problem-solver bot is flushing an empty tmp_buffer. I expect complaints from the checking server.")
        while len(self.working_array) <= i:
            self.working_array.append(None)
        self.working_array[i] = self.tmp_buffer
        self.tmp_buffer = None
        self.console(f"LOG_flush_tmp_buffer_on_pos {i}")

    def clone_to_its_right_ele_in_pos(self, i: int):
        if not 0 <= i < len(self.working_array):
            print(
                f"Ahi, the operator required to clone the element in pos {i} which does not exists since {i} is not in the interval [0,{len(self.working_array)}).")
        if len(self.working_array) == i+1:
            self.working_array.append(self.working_array[i])
        else:
            self.working_array[i + 1] = self.working_array[i]
        self.console(f"LOG_clone_to_its_right_ele_in_pos {i}")

    def what_in_tmp_buffer_goes_before_than_what_in_pos(self, i: int):
        if self.tmp_buffer is None:
            print(
                "Ahi, the operator required to compare with others the element contained in the tmp_buffer, but this buffer is empty. I expect complaints from the checking server.")
            return False
        if i >= len(self.working_array) or self.working_array[i] is None:
            print(
                f"Ahi, the operator required to compare with others the element contained in position {i} of the current working array. However, no element has ever been placed in this position of the array. I expect complaints from the checking server.")
            return False
        if self.tmp_buffer < self.working_array[i]:
            self.console(f"LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} (<)")
            return True
        self.console(f"LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} (>=)")
        return False

    def output_final_sorted_array(self):
        self.console(f"LOG_output_final_sorted_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})")
        if self.wait_for_prompt:
            self.BOT.input() # to wait for termination by the server


if __name__ == "__main__":
    print("UNIT TEST")

    tc = unittest.TestCase()

    print("\nTEST 1: operating the InsertionSortMachine to sort <4: 12 11 15 13>")

    expected_logs = [
        "LOG_load_next_input_element_in_tmp_buffer (got 12)",
        "LOG_flush_tmp_buffer_on_pos 0",
        "LOG_load_next_input_element_in_tmp_buffer (got 11)",
        "LOG_compare_what_in_tmp_buffer_with_what_in_pos 0 (<)",
        "LOG_clone_to_its_right_ele_in_pos 0",
        "LOG_flush_tmp_buffer_on_pos 0",
        "LOG_load_next_input_element_in_tmp_buffer (got 15)",
        "LOG_compare_what_in_tmp_buffer_with_what_in_pos 1 (>=)",
        "LOG_flush_tmp_buffer_on_pos 2",
        "LOG_load_next_input_element_in_tmp_buffer (got 13)",
        "LOG_compare_what_in_tmp_buffer_with_what_in_pos 2 (<)",
        "LOG_clone_to_its_right_ele_in_pos 2",
        "LOG_compare_what_in_tmp_buffer_with_what_in_pos 1 (>=)",
        "LOG_flush_tmp_buffer_on_pos 2",
        "LOG_output_final_sorted_array (4: 11 12 13 15)"
    ]

    SM = InsertionSortMachine(wait_for_prompt=False)
    SM.load_next_input_element_in_tmp_buffer(12)
    SM.flush_tmp_buffer_on_pos(0)
    SM.load_next_input_element_in_tmp_buffer(11)
    SM.what_in_tmp_buffer_goes_before_than_what_in_pos(0)
    SM.clone_to_its_right_ele_in_pos(0)
    SM.flush_tmp_buffer_on_pos(0)
    SM.load_next_input_element_in_tmp_buffer(15)
    SM.what_in_tmp_buffer_goes_before_than_what_in_pos(1)
    SM.flush_tmp_buffer_on_pos(2)
    SM.load_next_input_element_in_tmp_buffer(13)
    SM.what_in_tmp_buffer_goes_before_than_what_in_pos(2)
    SM.clone_to_its_right_ele_in_pos(2)
    SM.what_in_tmp_buffer_goes_before_than_what_in_pos(1)
    SM.flush_tmp_buffer_on_pos(2)
    SM.output_final_sorted_array()

    for e1, e2 in zip(expected_logs, SM.log):
        tc.assertEqual(e1, e2)

    print("\nTEST 1 passed")

    print("\nI PROSSIMI TEST SONO DA RIORGANIZZARE DIVERSAMENTE, LE PRIMITIVE DELLA MACCHINA NON DEVONO PRENDERE expected_log COME ARGOMENTO")

    
    print("\nTEST 2: Returning tmp_buffer overload error while operating the InsertionSortMachine to sort <2: 12 11>")

    SM = InsertionSortMachine(wait_for_prompt=False)
    SM.load_next_input_element_in_tmp_buffer(12, expected_log=expected_logs[0])
    tc.assertRaises(AssertionError, lambda: SM.load_next_input_element_in_tmp_buffer(11, expected_log=expected_logs[0]))

    print("\nTEST 2 passed")

    print("\nTEST 3: Returning empty buffer flushing error while operating the InsertionSortMachine to sort <2: 12 11>")

    SM = InsertionSortMachine(wait_for_prompt=False)
    tc.assertRaises(AssertionError, lambda: SM.flush_tmp_buffer_on_pos(1, expected_log=expected_logs[1]))

    print("\nTEST 3 passed")

    print("\nTEST 4: Returning bad clone error while operating the InsertionSortMachine to sort <2: 12 11>")
    tc.assertRaises(IndexError, lambda: SM.clone_to_its_right_ele_in_pos(3, expected_log=expected_logs[4]))

    print("\nTEST 4 passed")

    print("\nTEST 5: Returning compare with empty buffer error while operating the InsertionSortMachine to sort <2: 12 11>")
    SM = InsertionSortMachine(wait_for_prompt=False)
    tc.assertFalse(SM.what_in_tmp_buffer_goes_before_than_what_in_pos(0, expected_log=expected_logs[7]))

    print("\nTEST 5 passed")

    print("\nTEST 6: Returning compare with bad working array index(2) error while operating the InsertionSortMachine to sort <2: 12 11>")
    SM = InsertionSortMachine(wait_for_prompt=False)
    SM.load_next_input_element_in_tmp_buffer(12, expected_log=expected_logs[0])
    tc.assertFalse(SM.what_in_tmp_buffer_goes_before_than_what_in_pos(2, expected_log=expected_logs[7]))

    print("\nTEST 6 passed")

    print("\nTEST 7: Returning general bad operation error while operating the InsertionSortMachine to sort <2: 12 11>")
    SM = InsertionSortMachine(wait_for_prompt=False)
    tc.assertRaises(AssertionError, lambda: SM.load_next_input_element_in_tmp_buffer(12, expected_log=expected_logs[4]))

    print("\nTEST 7 passed")
    print("\nfurther tests ...\n")

    print("OK. All tests have been successfully passed!")
