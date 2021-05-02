#!/usr/bin/python
from sys import stderr, exit, argv

usage=f"""I am an efficient (linear time) bot that in an infinite loop receives two integer sequences T and S (one per line) and decides whether S is a subsequence of T or not (y/n).

You should call me as follows:
$ {argv[0]} <certificate>

 + when called with certificate=0 then I only print 'y' or 'n', plus possibly comment lines (lines beginning with '#')

 + when called with certificate=1 then, after every 'y' answer, I also exhibit a certificate that S is indeed a subsequence of T. I do this by printing (in a new uncommented line) an increasing sequence of |S| indexes where the elements of S can be retrieved in T, one by one, in their order as they occur in S.

 + when called with certificate>1, then, as above, it also prints an uncommented line meant to be a certificate, which is however invalid in some way:
   certificate=2 the sequence of indexes has not length |S|
   certificate=3 the sequence of indexes is not increasing
   certificate=4 there are indexes that fall outside the interval [0,|T|-1]
   certificate=5 for some i, S[i] <> T[index_i] (as long as this is possibile). 
"""

if len(argv) != 2:
    print(f"ERROR from bot {argv[0]}:\n\n   called with the wrong number of parameters.\n")
    print(usage)
    exit(1)
certificate = int(argv[1])

while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    T = spoon.split()
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    S = spoon.split()
    pos_S = 0
    indexes = []
    for wanted, i in zip(T,range(len(T))):
        if S[pos_S] == wanted:
            pos_S += 1
            indexes.append(i)
            if pos_S == len(S):
                print('y')
                print("# correct certificate:")
                if certificate == 1:
                    print(" ".join(map(str,indexes)))
                else:
                    print("# " + " ".join(map(str,indexes)))
                    if certificate == 2:
                        if len(S) > 1:
                            print(" ".join(map(str,indexes[:-1])))
                        else:
                            print(" ".join(map(str,indexes.append(indexes[-1]+1))))
                    if certificate == 3:
                        print(" ".join(map(str,reversed(indexes))))
                    if certificate == 4:
                        print(" ".join(map(str,indexes[:-1] + [len(T)])))
                    if certificate == 5:
                        print(" ".join(map(str,indexes[:-1] + [len(T)-1])))
                break
    if pos_S < len(S):
        print('n')
exit(0)
