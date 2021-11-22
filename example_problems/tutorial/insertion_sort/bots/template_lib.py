#!/usr/bin/env python3
from sys import argv
from time import sleep

import unittest


class InsertionSortMachine:
    def __init__(self):
        self.tmp_buffer = None
        self.working_array = []
        self.test_logs = []

    def console(self, log_msg, wait_for_receipt: bool, expected_log: str = None):
        assert expected_log is None or log_msg == expected_log
        sleep(1)
        print(log_msg)
        self.test_logs.append(log_msg)
        if wait_for_receipt:
            print("Insert a feedback line (or just press RETURN) to continue ...")
            input()

    def load_next_input_element_in_tmp_buffer(self, val: int, wait_for_receipt: bool = True, expected_log: str = None):
        if self.tmp_buffer is not None:
            print(
                "Ahi, my problem-solver bot is overwriting a yet unflushed value stored in the tmp_buffer. This is going to erase information which will be definitely lost it in the Insertion Sort algorithm approach.")
        self.tmp_buffer = val
        self.console(f"#LOG_load_next_input_element_in_tmp_buffer (got {val})", wait_for_receipt, expected_log)

    def flush_tmp_buffer_on_pos(self, i: int, wait_for_receipt: bool = True, expected_log: str = None):
        if self.tmp_buffer is None:
            print(
                "Ahi, my problem-solver bot is flushing an empty tmp_buffer. I expect complaints from the checking server.")
        while len(self.working_array) <= i:
            self.working_array.append(None)
        self.working_array[i] = self.tmp_buffer
        self.tmp_buffer = None
        self.console(f"#LOG_flush_tmp_buffer_on_pos {i}", wait_for_receipt, expected_log)

    def clone_to_its_right_ele_in_pos(self, i: int, wait_for_receipt: bool = True, expected_log: str = None):
        if not 0 <= i < len(self.working_array):
            print(
                f"Ahi, my problem-solver bot is asking to clone the element in pos {i} which does not exists since {i} is not in the interval [0,{len(self.working_array)}).")
        if len(self.working_array) == i+1:
            self.working_array.append(self.working_array[i])
        else:
            self.working_array[i + 1] = self.working_array[i]
        self.console(f"#LOG_clone_to_its_right_ele_in_pos {i}", wait_for_receipt, expected_log)

    def what_in_tmp_buffer_goes_before_than_what_in_pos(self, i: int, wait_for_receipt: bool = True, expected_log: str = None):
        if self.tmp_buffer is None:
            print(
                "Ahi, my problem-solver bot asks to compare with others the element contained in the tmp_buffer, but this buffer is empty. I expect complaints from the checking server.")
            return False
        if i >= len(self.working_array) or self.working_array[i] is None:
            print(
                f"Ahi, my problem-solver bot asks to compare with others the element contained in position {i} of the current working array. However, no element has ever been placed in this position of the array. I expect complaints from the checking server.")
            return False
        if self.tmp_buffer < self.working_array[i]:
            self.console(f"#LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} (<)", wait_for_receipt, expected_log)
            return True
        self.console(f"#LOG_compare_what_in_tmp_buffer_with_what_in_pos {i} (>=)", wait_for_receipt, expected_log)
        return False

    def output_final_sorted_array(self, wait_for_receipt: bool = True, expected_log: str = None):
        self.console(f"#LOG_output_final_sorted_array ({len(self.working_array)}: {' '.join(map(str,self.working_array))})", wait_for_receipt, expected_log)


if __name__ == "__main__":
    print("UNIT TEST")

    tc = unittest.TestCase()

    print("\nTEST 1: operating the InsertionSortMachine to sort <4: 12 11 15 13>")

    expected_logs = [
        "#LOG_load_next_input_element_in_tmp_buffer (got 12)",
        "#LOG_flush_tmp_buffer_on_pos 0",
        "#LOG_load_next_input_element_in_tmp_buffer (got 11)",
        "#LOG_compare_what_in_tmp_buffer_with_what_in_pos 0 (<)",
        "#LOG_clone_to_its_right_ele_in_pos 0",
        "#LOG_flush_tmp_buffer_on_pos 0",
        "#LOG_load_next_input_element_in_tmp_buffer (got 15)",
        "#LOG_compare_what_in_tmp_buffer_with_what_in_pos 1 (>=)",
        "#LOG_flush_tmp_buffer_on_pos 2",
        "#LOG_load_next_input_element_in_tmp_buffer (got 13)",
        "#LOG_compare_what_in_tmp_buffer_with_what_in_pos 2 (<)",
        "#LOG_clone_to_its_right_ele_in_pos 2",
        "#LOG_compare_what_in_tmp_buffer_with_what_in_pos 1 (>=)",
        "#LOG_flush_tmp_buffer_on_pos 2",
        "#LOG_output_final_sorted_array (4: 11 12 13 15)"
    ]

    SM = InsertionSortMachine()
    SM.load_next_input_element_in_tmp_buffer(12, wait_for_receipt=False, expected_log=expected_logs[0])
    SM.flush_tmp_buffer_on_pos(0, wait_for_receipt=False, expected_log=expected_logs[1])
    SM.load_next_input_element_in_tmp_buffer(11, wait_for_receipt=False, expected_log=expected_logs[2])
    SM.what_in_tmp_buffer_goes_before_than_what_in_pos(0, wait_for_receipt=False, expected_log=expected_logs[3])
    SM.clone_to_its_right_ele_in_pos(0, wait_for_receipt=False, expected_log=expected_logs[4])
    SM.flush_tmp_buffer_on_pos(0, wait_for_receipt=False, expected_log=expected_logs[5])
    SM.load_next_input_element_in_tmp_buffer(15, wait_for_receipt=False, expected_log=expected_logs[6])
    SM.what_in_tmp_buffer_goes_before_than_what_in_pos(1, wait_for_receipt=False, expected_log=expected_logs[7])
    SM.flush_tmp_buffer_on_pos(2, wait_for_receipt=False, expected_log=expected_logs[8])
    SM.load_next_input_element_in_tmp_buffer(13, wait_for_receipt=False, expected_log=expected_logs[9])
    SM.what_in_tmp_buffer_goes_before_than_what_in_pos(2, wait_for_receipt=False, expected_log=expected_logs[10])
    SM.clone_to_its_right_ele_in_pos(2, wait_for_receipt=False, expected_log=expected_logs[11])
    SM.what_in_tmp_buffer_goes_before_than_what_in_pos(1, wait_for_receipt=False, expected_log=expected_logs[12])
    SM.flush_tmp_buffer_on_pos(2, wait_for_receipt=False, expected_log=expected_logs[13])
    SM.output_final_sorted_array(wait_for_receipt=False, expected_log=expected_logs[14])

    for e1, e2 in zip(expected_logs, SM.test_logs):
        tc.assertEqual(e1, e2)

    print("\nTEST 1 passed")

    print("\nTEST 2: Returning tmp_buffer overload error while operating the InsertionSortMachine to sort <2: 12 11>")

    SM = InsertionSortMachine()
    SM.load_next_input_element_in_tmp_buffer(12, wait_for_receipt=False, expected_log=expected_logs[0])
    tc.assertRaises(AssertionError, lambda: SM.load_next_input_element_in_tmp_buffer(11, wait_for_receipt=False, expected_log=expected_logs[0]))

    print("\nTEST 2 passed")

    print("\nTEST 3: Returning empty buffer flushing error while operating the InsertionSortMachine to sort <2: 12 11>")

    SM = InsertionSortMachine()
    tc.assertRaises(AssertionError, lambda: SM.flush_tmp_buffer_on_pos(1, wait_for_receipt=False, expected_log=expected_logs[1]))

    print("\nTEST 3 passed")

    print("\nTEST 4: Returning bad clone error while operating the InsertionSortMachine to sort <2: 12 11>")
    tc.assertRaises(IndexError, lambda: SM.clone_to_its_right_ele_in_pos(3, wait_for_receipt=False, expected_log=expected_logs[4]))

    print("\nTEST 4 passed")

    print("\nTEST 5: Returning compare with empty buffer error while operating the InsertionSortMachine to sort <2: 12 11>")
    SM = InsertionSortMachine()
    tc.assertFalse(SM.what_in_tmp_buffer_goes_before_than_what_in_pos(0, wait_for_receipt=False, expected_log=expected_logs[7]))

    print("\nTEST 5 passed")

    print("\nTEST 6: Returning compare with bad working array index(2) error while operating the InsertionSortMachine to sort <2: 12 11>")
    SM = InsertionSortMachine()
    SM.load_next_input_element_in_tmp_buffer(12, wait_for_receipt=False, expected_log=expected_logs[0])
    tc.assertFalse(SM.what_in_tmp_buffer_goes_before_than_what_in_pos(2, wait_for_receipt=False, expected_log=expected_logs[7]))

    print("\nTEST 6 passed")

    print("\nTEST 7: Returning general bad operation error while operating the InsertionSortMachine to sort <2: 12 11>")
    SM = InsertionSortMachine()
    tc.assertRaises(AssertionError, lambda: SM.load_next_input_element_in_tmp_buffer(12, wait_for_receipt=False, expected_log=expected_logs[4]))

    print("\nTEST 7 passed")
    print("\nfurther tests ...\n")

    print("OK. All tests have been successfully passed!")
