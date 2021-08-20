#!/usr/bin/env python3

from sys import stdout, stderr, exit, argv
import os, os.path
import re
from typing import Dict, BinaryIO

from base64 import b64encode, b64decode

termcolor_is_installed = True
try:
    from termcolor import colored, cprint
except Exception as e:
    termcolor_is_installed = False
    print("# Recoverable Error: ", end="", file=stderr)
    print(e, file=stderr)
    print("# --> We proceed using no colors. Don't worry.\n# (To enjoy colors install the python package termcolor on your local machine.)", file=stderr)

# THIS LIBRARY SUPPORTS THE EXCHANGE OF FILES BETWEEN THE BOT OF THE PROBLEM SOLVER AND THE SERVICE SERVER OF THE PROBLEM MAKER
# The library mainly assumes that the rtal connect subcommand is used WITHOUT THE -e FLAG as follows:
#    rtal connect problem service -- my_bot.py
# The library ALSO offers wrapped-up functions that allow the bot to print on the terminal of the problem solver and/or to echo on that same screen what is reveived from the problem maker. The echoing might be triggered by the service service via some simple conventions (echo all lines beginning with '#!e' but is mainly let to the problem solver who anyhow has the last word on what goes printed on this screen). 
# When exchanging files, the library must be specularly used both in the bot and the service server.
# Things you need to know to get an understanding of how the library works and its natural use:
# The problem solver calls the `rtal connect` subcommand without the -e flag, then:
#     when the bot writes to stdout then only the server sees that message (on stdin)
#     when the bot writes to stderr then only the student sees that message (on the terminal)
#     when the service server writes to stdout then only the bot sees that message (on stdin)
#     when the service server writes to stderr then that message only appears in the log of the `rtald` TALight server
#
# IMPORTANT NOTICE: The problem solver can not write to the bot after having launched it. (Again, the only way to get this feature is to develop two different versions of `rtal`, one for Linux/Mac and one for Windows).
# Reminder: the standard is that the bot writes in green whereas the server writes in yellow (this il what happens when the -e flag is used).

class BotInterface:
    def __init__(self, display_lines_from_bot=True, display_lines_from_server=True, lines_from_bot_prefix="bot> ", lines_from_server_prefix="server> ", coloring_policy='original', display_files_from_bot=False, display_files_from_server=False):
        """coloring policy='original' if you want to preserve the colors of the problem maker,
           coloring policy='decolor'  if you want to remove any ANSI formatting escape sequence,
           coloring policy='standard-e'  if you want to use the standard color for when the server writes (yellow) when the -e flag is used."""
        self.lines_from_bot_prefix=lines_from_bot_prefix
        self.lines_from_server_prefix=lines_from_server_prefix
        self.display_lines_from_bot=display_lines_from_bot
        self.display_lines_from_server=display_lines_from_server
        self.coloring_policy=coloring_policy
        self.display_files_from_bot=display_files_from_bot
        self.display_files_from_server=display_files_from_server

    def input_line(self):
        line = input()
        if self.display_lines_from_server:
            if self.coloring_policy != 'original':
                print("Original server line: ",line)
                reaesc = re.compile(r'\x1b[^m]*m')
                new_line = reaesc.sub('', line)
            if self.coloring_policy == 'standard-e':
                print(colored(self.lines_from_server_prefix + line, 'yellow'), file=stderr)
            else:
                print(self.lines_from_server_prefix + line, file=stderr)
        return line

    def print_line(self, line):
        print(line)
        if self.display_lines_from_bot:
            if self.coloring_policy != 'original':
                print("Original bot line: ",line)
                reaesc = re.compile(r'\x1b[^m]*m')
                new_line = reaesc.sub('', line)
            if self.coloring_policy == 'standard-e':
                print(colored(self.lines_from_bot_prefix + line, 'green'), file=stderr)
            else:
                print(self.lines_from_bot_prefix + line, file=stderr)

    def bot_sends_required_files(self, conventional_names_to_files_map : Dict[str, BinaryIO]):
        while conventional_names_to_files_map:
            next_string=input()
            assert next_string[0] == '#'
            if next_string.startswith("#!gimme "):
                name = next_string[8:]
                if name not in conventional_names_to_files_map:
                    print(colored(self.lines_from_bot_prefix + f"You have not programmed me to send a file with handle `{name}` in this situation.", 'red'), file=stderr)
                    exit(0)
                print(b64encode(conventional_names_to_files_map[name].read()))
                del conventional_names_to_files_map[name]


    def bot_collects_eventually_sent_files(self):
        while True:
            next_string=input()
            assert next_string[0] == '#'
            if next_string.startswith("#!now_sending_files "):
                break
        num_files = int(next_string[20:])
        res = {}
        for i in range(num_files):
            filename, data = input().split()
            res[filename] = b64decode(data)
        return res

    def bot_write_files(filenames_to_files_map : Dict[str, bytes], basedir=os.path.join('.','downloads')):
        os.makedirs(basedir,exist_ok=True)
        for filename in filenames_to_files_map:
            with open(filename, 'wb') as file_down:
                flie_down.write(filenames_to_files_map[filename])

                        
def service_server_requires_and_gets_file(conventional_name):
    print(f"#!gimme {conventional_name}")
    #print("ciao0")
    string_got=input()
    print("ciao1")
    return b64decode(string_got)
                        
def service_server_to_send_files(filenames_to_files_map : Dict[str, BinaryIO]):
    """The server calls this function when the protocol enters a point where the server could send some files. In case there are no files to be sent, then use an empty dictionary as argument."""
    print(f"#!now_sending_files {len(filenames_to_files_map)}")
    for filename in filenames_to_files_map:
        print("{filename} {b64encode(filenames_to_files_map[name].read())}")
                        
                
"""
# Usage Example, files going from bot to server
in the bot:

from bot_interface import BotInterface
...

BTI = BotInterface(coloring_policy='standard-e')

# usually (but not necessarily) towards the beginning of the interaction between the bot and the server:

BTI.bot_sends_required_files({
    'problem_solver_mod' : open(os.path.join(".","upload","my_mod.mod"),'rb'),
    'problem_solver_dat' : open(os.path.join(".","upload","my_mod.dat"),'rb')
})

meanwhile, in the server:
from bot_interface import service_server_requires_and_gets_file
...
service_server_requires_and_gets_file('problem_solver_mod')
service_server_requires_and_gets_file('problem_solver_dat')

Notice: for the files sent from the bot to the server there must be a previous agreement at the protocol lever on the internal conventional names of the files (handles)
"""


"""
# Usage Example, files going from server to bot
in the bot:

from bot_interface import BotInterface
...

BTI = BotInterface(coloring_policy='standard-e')

# usually (but not necessarily) towards the end of the interaction between the bot and the server:

BTI.bot_write_files(bot_finally_gets_files())

meanwhile, in the server:
from bot_interface import service_server_to_send_files
...

dict_of_files = { f"seq_n{n}.txt": " ".join(map(str,range(n))).encode('ascii')  for n in [10, 20, 30] }
   service_server_to_send_files(dict_of_files)

print(dict_of_files['seq_n10.txt'].decode())   # to get on of the files in clear
"""
