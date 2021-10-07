#!/usr/bin/env python3

"""
These alternatives could lead to ultimately better solutions (but not sure on how having them working on Windows however):
1. using screen when launcing rtal to work on detached mode
2. using tmux when launcing rtal to work on detached mode
Note that sending the input text directly to the running process by sending this input text to the process' standard input "file" /proc/PID#/fd/0
is not a viable alternative. Indeed, it is not viable on Windows since one also needs to do an IOCTL operation of type TIOCSTI for every single byte to be sent.
More on this:
https://serverfault.com/questions/178457/can-i-send-some-text-to-the-stdin-of-an-active-process-running-in-a-screen-sessi/178470
"""

from sys import argv, stderr, exit
from pathlib import Path

from bot_interface import BotInterface


if len(argv) == 1:
    print(f"Usage: {argv[0]} [file_handle1=]your_load_folder/filename1 ... [file_handleN=]your_load_folder/filenameN\n    In other words, the command {argv[0]} should be followed by a non-empty list of file specifications separated by spaces. A file specification can begin with a file_handle assignment meant to specify the role of the file for the service. When files_handle are needed then you should use those specific to the problem.", file=stderr)
    exit(1)

map_handles_filenames = {}
    
for i in range(1, len(argv)):
    if '=' in argv[i]:
        handle, filename = argv[i].split('=')
    else:
        filename = argv[i]
        handle = f'file_handle{i}'
    if not Path(filename).is_file():
        print (f"File {filename} does not exist on your local machine. The bot ({argv[0]}) requires full paths to files actually existing on your machine.", file=stderr)
        exit(1)
    try:
        map_handles_filenames[handle] = open(filename,'rb')
    except IOError:
        print("File {filename} exists on your local machine but is not accessible. Check the read permissions of the file.", file=stderr)
        print(f"Correctly opened files: {i-1}/{len(argv)-1} files.", file=stderr)
        exit(1)

BTI = BotInterface(coloring_policy='standard-e')
BTI.bot_sends_required_files(map_handles_filenames)

while True:
    line = BTI.input_line()
