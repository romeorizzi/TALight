#!/usr/bin/python
from sys import stderr, exit, argv
# import argparse
import sys
import random
from bot_lib import Bot

# BOT = Bot(report_inputs=True,reprint_outputs=True)
BOT = Bot(report_inputs=False,reprint_outputs=False)

def calculate_sheets(rainbow):
  seq_len = len(rainbow)

  m = [[0 for __ in range(seq_len)] for _ in range(seq_len)]
  col = [0 for _ in range(seq_len)]

  old = 256
  j = 0
  second = [int(x) for x in rainbow]

  for i in range(seq_len):
    k = second[i]
    if ( k != old ):
      col[j] = k
      m[0][j] = 1
      j = j + 1
      old = k

  seq_len = j

  for i in range(1, seq_len):
    for j in range(seq_len - i):
      minimo=int(sys.maxsize)
      for k in range(1, i + 1):
        if col[j]==col[j+i]:
          temp = 1
        else:
          temp = 0
        a = m[k-1][j] + m[i-k][j+k] - temp
        minimo = min(a , minimo)
        m[i][j] = minimo

  return int(m[seq_len-1][0])

while True:
  seq_len = int(BOT.input())
  rainbow = BOT.input().split()
  #rainbow = []

  # for i in seq:
  #  rainbow.append(i)

  answer = calculate_sheets(rainbow)
  BOT.print(answer)
  
