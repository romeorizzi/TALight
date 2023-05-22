#!/usr/bin/python
from sys import stderr, exit, argv

max_val = 100

st = []

def find(inp, out) :
    if len(inp)== 0 :
        if len(out) != 0 :

            st.append(out)
        return
  
    find(inp[1:], out[:])
  

    if len(out)== 0:
        find(inp[1:], inp[:1])
    elif inp[0] > out[-1] :
        out.append(inp[0])
        find(inp[1:], out[:])
  

while True:
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    T = spoon.split()
    T = list(map(int, T))

    n = len(T)
    out = []
    find(T, out)
   
    print(len(st))
    st.clear()
exit(0)