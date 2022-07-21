#!/usr/bin/env python3
from sys import setrecursionlimit, stderr, exit, argv
import argparse
import sys
import random
from bot_lib import Bot

parser = argparse.ArgumentParser(description="I am a bot for the TALight problem `collage`. In a never ending loop (until I get the '# WE HAVE FINISHED' line), I read an input instances from stdin and I write my answer for it on stdout.")
parser.add_argument('--recursive', action='store_true', help="Use this option to select the recursive solution method.")
parser.add_argument('--dynprog', action='store_true', help="Use this option to select the dynamic programming solution method.")
args = parser.parse_args()

print(f"""# I am a bot for the TALight problem `Collage`. Call me like this:
#     {argv[0]} -h
# if you want to know more about me (how to call me, my arguments and what I am supposed to do for you).
# My parameters for the current call are set as follows:
#   {args.recursive=}
#   {args.dynprog=}""")

setrecursionlimit(10**8)

NMAX=1000

seq=[]
memo = [[0 for __ in range(NMAX)] for _ in range(NMAX)]

# BOT = Bot(report_inputs=True,reprint_outputs=True)
BOT = Bot(report_inputs=False,reprint_outputs=False)

def Min(i:int, j:int):
  if i > j:
    return 0
  
  if i == j:
    return 1
  
  if memo[i][j] > 0:
    return memo[i][j]

  ret = 1 + Min(i+1, j)

  for k in range(i+1,j+1):
    if seq[k] == seq[i]:
      ret = min(ret, Min(i+1, k-1) + Min(k, j))

  memo[i][j] = ret

  return memo[i][j]

def PD(n):
  for i in range(n, -1, -1):
    for j in range(i-1, n):
      if(i > j):
        memo[i][j] = 0
      elif(i==j):
        memo[i][j] = 1
      else:
        memo[i][j] = 1 + memo[i+1][j];
        for k in range(i+1, j+1):
          if seq[k] == seq[i]:
            memo[i][j] = min(memo[i][j], memo[i+1][k-1] + memo[k][j])
  return memo[0][n-1]

def calculate_sheets(rainbow):
  seq_len = len(rainbow)
  n=0
  prev=-1

  for i in range(seq_len):
    tmp = rainbow[i]

    if tmp != prev:
      seq.append(tmp)
      prev = tmp
      n += 1

  if args.recursive:
    risp=Min(0,n-1)
  elif args.dynprog:
    risp=PD(n)
  else:
    risp=Min(0,n-1)

  return risp


while True:
  seq_len = int(BOT.input())
  rainbow = BOT.input().split()

  answer = calculate_sheets(rainbow)
  BOT.print(answer)
  
