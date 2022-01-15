#!/usr/bin/env python3
import math
from multiprocessing.connection import wait
from signal import SIGINT, SIGKILL, SIGTERM, signal, SIGPIPE, SIG_DFL

while True:
    spoon = input()
    if not('WE HAVE FINISHED' in spoon) and not('Correct answers:' in spoon) and not('[Press ENTER to exit]' in spoon):
        if spoon[0] != '#':
            s,d = map(int, spoon.split() )
            x1 = (s + d) // 2
            x2 = (s - d) // 2
            print(f"{x1} {x2}")
        else:
            splitted=spoon.split()
            #print(splitted)
            s,d = map(int, splitted[2:] )
            x1 = (s + d) // 2
            x2 = (s - d) // 2
            print(f"{x1} {x2}")
    else:
        print('\0')
        signal(SIGPIPE,SIG_DFL)
        signal(SIGINT,SIG_DFL) 
        exit(0)
        #while True:
            #print('\0')
            #exit(0)
            #signal(SIGPIPE,SIG_DFL)
            #signal(SIGKILL,SIG_DFL) 
