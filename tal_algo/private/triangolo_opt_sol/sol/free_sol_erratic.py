#!/usr/bin/env python3
from sys import stderr
import random

from triangolo_lib import Triangolo

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        Tr = Triangolo() # loads the triangle instance from stdin
        #Tr.display(stderr)
        opt_val = Tr.max_val_ric_memo()
        opt_sol = Tr.opt_sol()
        #print(opt_val, file=stderr)
        #print(opt_sol, file=stderr)
        dice = random.randrange(0, 6)
        if dice <= 1:
            opt_sol = opt_sol[:-1] + ('L' if opt_sol[-1]=='R' else 'R')
            if dice == 1:
                ok, new_opt_val = Tr.eval_sol_unsafe(opt_sol)
                if ok:
                    opt_val = new_opt_val
        print(opt_val)
        print(opt_sol)
