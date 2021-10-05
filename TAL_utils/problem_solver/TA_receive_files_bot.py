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


BTI = BotInterface(coloring_policy='standard-e')
BTI.bot_write_files(BTI.bot_collects_eventually_sent_files())