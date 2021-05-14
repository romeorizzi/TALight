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

def CeilIndex(A, l, r, key):
    while (r - l > 1):
        m = l + (r - l)//2
        if (A[m] >= key):
            r = m
        else:
            l = m
    return r
  
def LongestIncreasingSubsequenceLength(A, size):
 
    tailTable = [0 for i in range(size + 1)]
    length = 0
  
    tailTable[0] = A[0]
    length = 1
    for i in range(1, size):
     
        if (A[i] < tailTable[0]):
            tailTable[0] = A[i]
  
        elif (A[i] > tailTable[length-1]):
            tailTable[length] = A[i]
            length+= 1
  
        else:
    
            tailTable[CeilIndex(tailTable, -1, length-1, A[i])] = A[i]
         
    tailTable = tailTable[:length]
    return tailTable, length



while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    T = spoon.split()
    T = list(map(int, T))

    
    cert, n_col = LongestIncreasingSubsequenceLength(T, len(T))
   
    print(n_col)
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