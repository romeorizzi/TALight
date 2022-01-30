#!/usr/bin/env python3
import sys
import unittest

from abstract_machine_lib import AbstractMachine

class AbstractMachineOperatingError(Exception):
    pass

class InsertionSortMachine(AbstractMachine):
    def __init__(self, input_array = [], wait_for_prompt=False, log_on_console=True):
        super(InsertionSortMachine, self).__init__(wait_for_prompt, log_on_console)
        self.input_stream = input_array
        self.tmp_buffer = None
        self.working_array = []

    def append_to_input_stream(self, new_ele: int):
        self.input_stream.append(new_ele)        
        
    def input_stream_is_empty(self):
        return len(self.input_stream) == 0
        
    def load_next_input_element_in_tmp_buffer(self):
        if self.tmp_buffer is not None:
            raise AbstractMachineOperatingError(sys._getframe(  ).f_code.co_name+"_1", "Ahi, the InsertionSort Machine has been asked to overwrite a yet unflushed value stored in its tmp_buffer. This would erase information and the value of the element currently stored in the tmp_buffer would be definitely lost.")
        if self.input_stream_is_empty():
            raise AbstractMachineOperatingError(sys._getframe(  ).f_code.co_name+"_2", "Ahi, the InsertionSort Machine has been asked to load in its tmp_buffer a new element from its input stream. However, the input stream is now empty!")
        self.tmp_buffer = self.input_stream[0]
        self.input_stream = self.input_stream[1:]
        self.console(f"LOG_load_next_input_element_in_tmp_buffer (got {self.tmp_buffer})")

    def flush_tmp_buffer_ele_in_pos(self, i: int):
        if self.tmp_buffer is None:
            raise AbstractMachineOperatingError(sys._getframe(  ).f_code.co_name+"_1", "Ahi, the InsertionSort Machine has been asked to flush out an empty tmp_buffer.")
        if i < 0:
            raise AbstractMachineOperatingError(sys._getframe(  ).f_code.co_name+"_2", f"Ahi, the InsertionSort Machine has been asked to flush out the element from the tmp_buffer onto position {i} of the working_array. Negative positions are not allowed.")            
        while len(self.working_array) <= i:
            self.working_array.append(None)
        self.working_array[i] = self.tmp_buffer
        self.tmp_buffer = None
        self.console(f"LOG_flush_tmp_buffer_ele_in_pos {i}")

    def clone_to_its_right_ele_in_pos(self, i: int):
        if not 0 <= i < len(self.working_array):
            raise AbstractMachineOperatingError(sys._getframe(  ).f_code.co_name, f"Ahi, the operator required to clone the element in pos {i} which does not exists since {i} is not in the interval [0,{len(self.working_array)}).")
        if len(self.working_array) == i+1:
            self.working_array.append(self.working_array[i])
        else:
            self.working_array[i+1] = self.working_array[i]
        self.console(f"LOG_clone_to_its_right_ele_in_pos {i}")

    def compare_ele_in_tmp_buffer_with_ele_in_pos(self, i: int):
        if self.tmp_buffer is None:
            raise AbstractMachineOperatingError(sys._getframe(  ).f_code.co_name+"_1", "Ahi, the operator required to compare with others the element contained in the tmp_buffer, but this buffer is empty.")
        if i >= len(self.working_array) or self.working_array[i] is None:
            raise AbstractMachineOperatingError(sys._getframe(  ).f_code.co_name+"_2", f"Ahi, the operator required to compare with others the element contained in position {i} of the current working array. However, no element has ever been placed in this position of the array.")
        if self.tmp_buffer < self.working_array[i]:
            self.console(f"LOG_compare_ele_in_tmp_buffer_with_ele_in_pos {i} (<)")
            return True
        self.console(f"LOG_compare_ele_in_tmp_buffer_with_ele_in_pos {i} (>=)")
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
        "LOG_flush_tmp_buffer_ele_in_pos 0",
        "LOG_load_next_input_element_in_tmp_buffer (got 11)",
        "LOG_compare_ele_in_tmp_buffer_with_ele_in_pos 0 (<)",
        "LOG_clone_to_its_right_ele_in_pos 0",
        "LOG_flush_tmp_buffer_ele_in_pos 0",
        "LOG_load_next_input_element_in_tmp_buffer (got 15)",
        "LOG_compare_ele_in_tmp_buffer_with_ele_in_pos 1 (>=)",
        "LOG_flush_tmp_buffer_ele_in_pos 2",
        "LOG_load_next_input_element_in_tmp_buffer (got 13)",
        "LOG_compare_ele_in_tmp_buffer_with_ele_in_pos 2 (<)",
        "LOG_clone_to_its_right_ele_in_pos 2",
        "LOG_compare_ele_in_tmp_buffer_with_ele_in_pos 1 (>=)",
        "LOG_flush_tmp_buffer_ele_in_pos 2",
        "LOG_output_final_sorted_array (4: 11 12 13 15)"
    ]

    SM = InsertionSortMachine([12, 11, 15, 13], wait_for_prompt=False)
    SM.load_next_input_element_in_tmp_buffer()
    SM.flush_tmp_buffer_ele_in_pos(0)
    SM.load_next_input_element_in_tmp_buffer()
    SM.compare_ele_in_tmp_buffer_with_ele_in_pos(0)
    SM.clone_to_its_right_ele_in_pos(0)
    SM.flush_tmp_buffer_ele_in_pos(0)
    SM.load_next_input_element_in_tmp_buffer()
    SM.compare_ele_in_tmp_buffer_with_ele_in_pos(1)
    SM.flush_tmp_buffer_ele_in_pos(2)
    SM.load_next_input_element_in_tmp_buffer()
    SM.compare_ele_in_tmp_buffer_with_ele_in_pos(2)
    SM.clone_to_its_right_ele_in_pos(2)
    SM.compare_ele_in_tmp_buffer_with_ele_in_pos(1)
    SM.flush_tmp_buffer_ele_in_pos(2)
    SM.output_final_sorted_array()

    for e1, e2 in zip(expected_logs, SM.log):
        tc.assertEqual(e1, e2)

    print("\nTEST 1 passed")

    print("\nI PROSSIMI TEST SONO DA RIORGANIZZARE DIVERSAMENTE, LE PRIMITIVE DELLA MACCHINA NON DEVONO PRENDERE expected_log COME ARGOMENTO")

    
    print("\nTEST 2: Returning tmp_buffer overload error while operating the InsertionSortMachine to sort <2: 12 11>")

    SM = InsertionSortMachine([12, 11, 15, 13], wait_for_prompt=False)
    SM.load_next_input_element_in_tmp_buffer()
    tc.assertEqual(expected_logs[0], SM.log[0])
    tc.assertRaises(AbstractMachineOperatingError, lambda: SM.load_next_input_element_in_tmp_buffer())

    print("\nTEST 2 passed")

    print("\nTEST 3: Returning empty buffer flushing error while operating the InsertionSortMachine to sort <2: 12 11>")

    SM = InsertionSortMachine([12, 11, 15, 13], wait_for_prompt=False)
    tc.assertRaises(AbstractMachineOperatingError, lambda: SM.flush_tmp_buffer_ele_in_pos(0))
    
    print("\nTEST 3 passed")

    print("\nTEST 4: Returning bad clone error while operating the InsertionSortMachine to sort <2: 12 11>")
    SM = InsertionSortMachine([12, 11, 15, 13], wait_for_prompt=False)
    SM.load_next_input_element_in_tmp_buffer()
    tc.assertEqual(expected_logs[0], SM.log[0])
    SM.flush_tmp_buffer_ele_in_pos(0)
    tc.assertEqual(expected_logs[1], SM.log[1])
    tc.assertRaises(AbstractMachineOperatingError, lambda: SM.clone_to_its_right_ele_in_pos(1))

    print("\nTEST 4 passed")

    print("\nTEST 5: Returning compare with empty buffer error while operating the InsertionSortMachine to sort <2: 12 11>")
    SM = InsertionSortMachine([12, 11, 15, 13], wait_for_prompt=False)
    tc.assertRaises(AbstractMachineOperatingError, lambda: SM.compare_ele_in_tmp_buffer_with_ele_in_pos(0))

    print("\nTEST 5 passed")

    print("\nTEST 6: Returning compare with bad working array index(2) error while operating the InsertionSortMachine to sort <2: 12 11>")
    SM = InsertionSortMachine([12, 11, 15, 13], wait_for_prompt=False)
    SM.load_next_input_element_in_tmp_buffer()
    tc.assertEqual(expected_logs[0], SM.log[0])
    tc.assertRaises(AbstractMachineOperatingError, lambda: SM.compare_ele_in_tmp_buffer_with_ele_in_pos(2))

    print("\nTEST 6 passed")
    
    print("\nConsider adding further tests ...\n")

    print("OK. All considered tests have been successfully passed!")
