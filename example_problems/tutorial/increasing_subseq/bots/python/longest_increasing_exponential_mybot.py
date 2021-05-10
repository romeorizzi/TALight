#!/usr/bin/python
from sys import stderr, exit, argv

usage=f"""I am an efficient (linear time) bot that in an infinite loop receives two integer sequences T and S (one per line) and decides whether S is a subsequence of T or not (y/n).

You should call me as follows:
$ {argv[0]} <certificate>

+ when called with certificate=0 then I only print the length of S, plus possibly comment lines (lines beginning with '#')

+ when called with certificate=1 then, after every answer, I also exhibit a certificate that S is indeed a subsequence of T. I do this by printing (in a new uncommented line) an increasing sequence of |S| indexes where the elements of S can be retrieved in T, one by one, in their order as they occur in S.

+ when called with certificate>1, then, as above, it also prints an uncommented line meant to be a certificate, which is however invalid in some way:
   certificate=2 the sequence has not length |S|
   certificate=3 the sequence S is not increasing
   certificate=4 for some i, S[i] isn't in T
"""

if len(argv) != 2:
    print(f"ERROR from bot {argv[0]}:\n\n   called with the wrong number of parameters.\n")
    print(usage)
    exit(1)
certificate = int(argv[1])

def all_increasing_subseq(A):
    L = list()
    for i in range(0, len(A)):
        L.append(list())

    L[0].append(A[0])

    for i in range(1, len(A)):
        for j in range(0, i):

            if (A[j] < A[i]) and (len(L[i]) < len(L[j])):
                L[i] = []
                L[i].extend(L[j])

        L[i].append(A[i])
    return L

def find_ls(l):
    lung = 0
    index = []
    ret = []
    for i in l:
        if len(i) > lung:
            index.clear()
            lung = len(i)
            index.append(l.index(i))
        elif len(i) == lung:
            index.append(l.index(i))
    for i in index:
        if (l[i] not in ret):
            ret.append(l[i])
    return ret, lung


while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    T = spoon.split()
    T = list(map(int, T))


    subseq = all_increasing_subseq(T)
    subseq, n_elements = find_ls(subseq)
    cert = subseq[0]
   
    print(n_elements)
    print("# correct certificate:")
    if certificate == 0:
        print("# " + " ".join(map(str,cert)))
    elif certificate == 1:
        print(" ".join(map(str,cert)))
    elif certificate == 2:
        cert.pop()
        print(" ".join(map(str,cert)))
    elif certificate == 3:
        cert.reverse()
        print(" ".join(map(str,cert)))
    elif certificate == 4:
        cert = [x+1 for x in cert]
        print(" ".join(map(str,cert)))
        

exit(0)
