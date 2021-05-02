#!/usr/bin/python
from sys import stderr, exit, argv

usage=f"""I am an efficient (linear time) bot that in an infinite loop receives two integer sequences T and S (one per line) and decides whether S is a subsequence of T or not (y/n).

You should call me as follows:
$ {argv[0]} <with_feedback>\n
when called with_feedback=1 then, after every 'y' answer, I also exhibit an S subsequence of T to certify that S is indeed a subsequence of T. I do this by printing (in a new uncommented line) an increasing sequence of |S| indexes where the elements of S can be orderly retrieved in T.
"""

if len(argv) != 2:
    print(f"ERROR from bot {argv[0]}:\n\n   called with the wrong number of parameters.\n")
    print(usage)
    exit(1)
with_certificate = False
if argv[1] == '1':
    with_certificate = True

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
                if with_certificate:
                    print(" ".join(map(str,indexes)))
                else:
                    print("# " + " ".join(map(str,indexes)))
                break
    if pos_S < len(S):
        print('n')
exit(0)
