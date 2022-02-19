#!/usr/bin/env python3

from sys import stderr
            
class Bot:
    def __init__(self, report_inputs=False,reprint_outputs=False, omit_reporting_clines_on_stderr=False, omit_reprinting_clines_on_stderr=False,omit_reporting_clines_on_log_file=False,omit_reprinting_clines_on_log_file=False,log_file_name=None,skip_printing_clines=False, BOT_prefix_to_reported_input_line="# BOT> input_debug got line=",BOT_prefix_to_printed_lines="# BOT> printed=", empty_line_is_comment = True):
        """1. when report_inputs=True then every line input by the bot through the class method `input_debug` is reported on stdterr, and also on the log file (if log_file_name != None). However, comment lines (lines starting with the '#' character) are omitted depending on the truth value of the parameters:
              (stderr) omit_reporting_clines_on_stderr
              (log_file) omit_reporting_clines_on_log_file
           2. when reprint_outputs=True then every line printed by the bot through the class method `print_debug` is printed also on stdterr, and also on the log file (if log_file_name != None). However, comment lines (lines starting with the '#' character) are omitted depending on the truth value of the parameters:
              (stderr) omit_reprinting_clines_on_stderr
              (log_file) omit_reprinting_clines_on_log_file
           Note: with skip_printing_clines=True then no line is actually printed (nor reprinted anywhere) when the bot commands to print a cline (line beginning with the '#' character, see function is_comment(line)).
        """
        self.report_inputs = report_inputs
        self.reprint_outputs = reprint_outputs
        self.omit_reporting_clines_on_stderr = omit_reporting_clines_on_stderr
        self.omit_reporting_clines_on_log_file = omit_reporting_clines_on_log_file
        self.omit_reprinting_clines_on_stderr = omit_reprinting_clines_on_stderr
        self.omit_reprinting_clines_on_log_file = omit_reprinting_clines_on_log_file
        self.skip_printing_clines=skip_printing_clines
        self.BOT_prefix_to_reported_input_line=BOT_prefix_to_reported_input_line
        self.BOT_prefix_to_printed_lines=BOT_prefix_to_printed_lines
        self.empty_line_is_comment = empty_line_is_comment
        
        self.log_file = None
        if log_file_name != None:
            self.log_file = open(log_file_name, 'w')
            

    def is_comment(line, empty_line_is_comment='default'):
        assert empty_line_is_comment in ['default', True, False]
        if empty_line_is_comment == default:
            empty_line_is_comment = self.empty_line_is_comment
        if empty_line_is_comment:
            return len(line)==0 or line[0]=='#'
        return len(line)>0 and line[0]=='#'
                              
    def input(self, report_inputs=None,
                    omit_reporting_clines_on_stderr=None,
                    omit_reporting_clines_on_log_file=None,
                    log_file='the_one_of_the_class'):
        """use report_inputs=False to disable the debug printing by the bot. You may also redirect stderr using the redirection 2> /dev/null or on a file. You may also pass an handler to a file for additional logging.
           Note: when log_file='the_one_of_the_class' this method will print on the log file self.log_file  opened when the class what instatiated (if any).
           If self.log_file != None because such file has been opened, and you do not want this method to print on any log file, then you should forcibly pass the argument log_file='the_one_of_the_class'."""
        if report_inputs == None:
            report_inputs = self.report_inputs
        if omit_reporting_clines_on_stderr == None:
            omit_reporting_clines_on_stderr = self.omit_reporting_clines_on_stderr
        if omit_reporting_clines_on_log_file == None:
            omit_reporting_clines_on_log_file = self.omit_reporting_clines_on_log_file
        if log_file == 'the_one_of_the_class':
            log_file = self.log_file
        #---------------------------                
        while True:
            line = input()
            is_cline = is_comment(line, self.empty_line_is_comment)
            if report_inputs and not (is_cline and omit_reporting_clines_on_stderr):
                print(self.BOT_prefix_to_reported_input_line + line, file = stderr)
            if log_file != None and not (is_cline and omit_reporting_clines_on_log_file):
                print(self.BOT_prefix_to_reported_input_line + line, file = log_file)
            if is_cline:
                if line == '# WE HAVE FINISHED':
                    exit(0)   # exit upon termination of the service server
            else:
                return line

    def print(self, line_msg, reprint_outputs=None,
                    skip_printing_clines=None,
                    omit_reprinting_clines_on_stderr=None,
                    omit_reprinting_clines_on_log_file=None,
                    log_file='the_one_of_the_class'):
        """Note 1: with skip_printing_clines=True then no line is actually printed (nor reprinted anywhere) when the bot commands to print a cline (line beginning with the '#' character, see function is_comment(line)).
           Note 2: when log_file='the_one_of_the_class' this method will print on the log file self.log_file  opened when the class what instatiated (if any). If self.log_file != None because such file has been opened, and you do not want this method to print on any log file, then you should forcibly pass the argument log_file='the_one_of_the_class'.
        """
        if reprint_outputs == None:
            reprint_outputs = self.reprint_outputs
        if skip_printing_clines == None:
            skip_printing_clines = self.skip_printing_clines
        if omit_reprinting_clines_on_stderr == None:
            omit_reprinting_clines_on_stderr = self.omit_reprinting_clines_on_stderr
        if omit_reprinting_clines_on_log_file == None:
            omit_reprinting_clines_on_log_file = self.omit_reprinting_clines_on_log_file
        if log_file == 'the_one_of_the_class':
            log_file = self.log_file
        #---------------------------    
        is_cline = self.is_comment(line_msg)
        if is_cline and skip_printing_clines:
            return
        print(line_msg)
        if reprint_outputs and not (is_cline and omit_reprinting_clines_on_stderr):
            print(self.BOT_prefix_to_printed_lines + line_msg, file = stderr)
        if log_file and not (is_cline and omit_reprinting_clines_on_log_file):
            print(self.BOT_prefix_to_printed_lines + line_msg, file = log_file)
