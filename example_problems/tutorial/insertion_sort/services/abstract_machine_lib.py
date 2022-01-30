#!/usr/bin/env python3
import sys
from time import sleep

from bot_lib import Bot

class AbstractMachine:
    def __init__(self, wait_for_prompt=False, log_on_console=True):
        self.log = []
        self.BOT = Bot(report_inputs = wait_for_prompt,reprint_outputs = wait_for_prompt, BOT_prefix_to_reported_input_line="SERVER> ",BOT_prefix_to_printed_lines="BOT> ", empty_line_is_comment = False)
        self.log_on_console = log_on_console
        self.wait_for_prompt = wait_for_prompt

    def console(self, log_msg):
        """This method is called by each basic primitive of the abstract Sorting Machine. The method implementing the primitive calls the console method in order to print the LOG message associated with the primitive.
           If self.wait_for_prompt = True then the bot waits for an input line (not beginning with '#') before printing the LOG.
        """ 
        if self.wait_for_prompt:
            line = self.BOT.input()
        else:
            sleep(0.1)
        self.log.append(log_msg)
        if self.log_on_console:
            self.BOT.print(log_msg)

