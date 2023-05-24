#!/usr/bin/python

def matMult(A,B,modulus):
  m = len(A)
  n = len(A[0])
  assert n == len(B)
  p = len(B[0])
  C = [ [None] * n for _ in range(p)]
  for i in range(n):
    for j in range(p):
      C[i][j] = sum([A[i][q]*B[q][j] for q in range(n)]) % modulus
  return C


def fastMatPow(M,N,modulus):
    if N == 0:
        return [ [1,0], [0,1] ]
    elif N % 2 == 0:
        tmp = fastMatPow(M,N//2,modulus)
        return matMult(tmp,tmp,modulus)
    else:
        return matMult(fastMatPow(M,N-1,modulus),M,modulus)


def num_piastrellature(N):
  assert N >= 0
  if N <= 1:
    return 1
  M = [ [1,1], [1,0] ]
  M_to_power_of_N = fastMatPow(M,N, 10**9 + 7)
  return M_to_power_of_N[0][0]



N = int(input("n="))
print(num_piastrellature(N))
