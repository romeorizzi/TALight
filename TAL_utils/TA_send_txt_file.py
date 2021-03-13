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

if len(argv) == 1:
    print(f"Usage: {argv[0]} file1.txt file2.txt ... \n    In other words, the command {argv[0]} should be followed by a non-empty list of filenames separated by spaces.\n    Each filename should specify the full path of a file on your local machine.", file=stderr)
    exit(1)

for i in range(1,len(argv)):
    if not Path(argv[i]).is_file():
        print (f"File {argv[i]} does not exist on your local machine. Please, provide full paths to files actually existing on your machine.", file=stderr)
        exit(1)

spoon = input().strip()
while spoon[:len("# waiting for ")] != "# waiting for ":
    spoon = input().strip()
    assert spoon[0] == "#"

print(f"TA_send util will now send {len(argv)-1} files.", file=stderr)

for i in range(1,len(argv)):
    print(f"The TAlight util {argv[0]} will now send the file {argv[i]} ...", file=stderr)
    try:
        f = open(argv[i], "r")
        lines=f.readlines()
        for line in lines:
            print(line.strip())
    except IOError:
        print("File {argv[i]} exists on your local machine but is not accessible. Check the read permissions of the file.", file=stderr)
        print(f"Correctly transmitted files: {i-1}/{len(argv)-1} files.", file=stderr)
        exit(1)
    finally:
        f.close()
        if i < len(argv)-1:
            print("#next")
        else:
            if line.strip() != "#end":
                print("#end")
        assert input() == "# FILE GOT" 
        print(f"File {argv[0]} has been correctly sent and received.", file=stderr)
if len(argv) > 2:
    print(f"The TAlight util has correctly sent {len(argv)-1}/{len(argv)-1} files.", file=stderr)

