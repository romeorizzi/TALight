#!/usr/bin/env python3
from sys import stderr, stdout, argv
from random import randrange, randint

usage = f"""
   Call as follows:
      {argv[0]} num_sols_ok solution_ok debug_level efficiency_level

   where the three arguments hold the following meaning:
   - num_sols_ok:
        0 the first output line never returns the right number (1)
        1 the first output line ought to be often ok, but not always
        2 first output line is always "1\n" (i.e., the right answer)
   - solution_ok
        0 never return a solution turning on all PCs
        1 the second output line ought to be often ok, but not always
        2 always return a correct solution turning on all PCs
   - debug_level
        0 print no debug info on stderr
        1 print checkpoint testcase number to help debugging
        2 print also the received instance
        3 echo also the output on stdout
   - efficiency_level
        0 quadratic in N
        1 N log N with nested lists of divisors of every number
        2 N log N without lists of divisors of every number"""


def Accendi0(N, acceso, pulsante):
  for i in range(N, 0, -1):
    if acceso[i]==0:
      pulsante[i] = 1
      for j in range(1,i+1):
        if i%j == 0:
          acceso[j] = 1-acceso[j]

def Accendi1(N, acceso, pulsante):
    divisors_of = [[]]*(N+1)
    for i in range(1,N+1):
        for n in range(2*i,N+1,i):
            divisors_of[n].append(i)
    for i in range(N,0,-1):
        if acceso[i]==0:
            pulsante[i] = 1
            for j in divisors_of[i]:
                acceso[j] = 1-acceso[j]
                
def Accendi2(N, acceso, pulsante):
    for i in range(N, 0, -1):
        for m in range(2*i,N+1,i):
            if pulsante[m]==1:
              acceso[i] = 1-acceso[i]
        if acceso[i]==0:
            pulsante[i] = 1
            
Accendi=[Accendi0,Accendi1,Accendi2]


if __name__ == "__main__":
    if len(argv) != 5:
        print(f"Error: program {argv[0]} called with {len(argv)-1} arguments rather than 4.")
        print(usage)
        exit(1)
    num_sols_ok, solution_ok, debug_level, efficiency_level = map(int, argv[1:])
    T = int(input())
    for t in range(1, 1 + T):
        if debug_level>0:
            print(f"Testcase {t}:", file=stderr)
        N = int(input())
        acceso = [None] + list(map(int, input().strip().split()))
        if debug_level>1:
            print(f"{N=}, {acceso=}", file=stderr)
        pulsante = [None] + [0]*N
        Accendi[efficiency_level](N, acceso, pulsante)
        spoil_num_sols = num_sols_ok==2 or (num_sols_ok==1 and randrange(4)>0)
        spoil_solution = solution_ok==2 or (solution_ok==1 and randrange(4)>0)
        fouts = [stdout]
        if debug_level>2:
            fouts.append(stderr)
        for fout in fouts:
          if spoil_num_sols: 
              print(1, file=fout)
          else:
              print(2*randint(0,1), file=fout)
          for i in range(1,N):
              print(pulsante[i], end=" ", file=fout)
          if spoil_solution:
              print(pulsante[N], file=fout)
          else:
              print(1-pulsante[N], file=fout)
