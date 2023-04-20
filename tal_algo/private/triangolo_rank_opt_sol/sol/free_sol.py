#!/usr/bin/env python3
from sys import stderr

from triangolo_lib import Triangolo

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        Tr = Triangolo() # loads the triangle instance from stdin
        opt_path_given = input().strip()
        #Tr.display(stderr)
        #print(f"{opt_path_given=}", file=stderr)
        print(Tr.max_val_ric_memo())
        print(Tr.num_opt_sols_ric_memo())
        print(Tr.rank_safe(opt_path_given))
