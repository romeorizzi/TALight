#!/usr/bin/env python3

while True:
    spoon = input()
    #print(f"# BOT: spoon={spoon}")
    if spoon[0] == '#':   # spoon contains a commented line from the service server
        if '# WE HAVE FINISHED' == spoon:
            exit(0)   # exit upon termination of the service server
    else:
        n = int(spoon)
        print(f"{n//2} {(n+1)//2}")
