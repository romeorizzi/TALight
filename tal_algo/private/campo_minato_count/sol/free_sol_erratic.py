#!/usr/bin/env python3
from sys import stderr
from random import randrange, randint

from triangolo_lib import Triangolo

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        Tr = Triangolo() # loads the triangle instance from stdin
        #Tr.display(stderr)
        #print(Tr.max_val_ric_memo(), file=stderr)
        #print(Tr.num_opt_sols_ric_memo(), file=stderr)
        print(Tr.max_val_ric_memo())
        dice = randrange(0,6)
        if dice == 0:
            print(Tr.num_opt_sols_ric_memo() + randint(-1,1))
        else:
            print(Tr.num_opt_sols_ric_memo())
