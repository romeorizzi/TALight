#!/usr/bin/python
"""una soluzione semplice, che risponde come richiesto in tutti i subtask con risposta < 10^9 +7, ed eccede i timelimits già per n > 10^6."""

memo_risp = [None] * 3

T = int(input())
for _ in range(T):
    N = int(input())
    memo_risp[0] = memo_risp[1] = 1
    for n in range(2, N + 1):
        memo_risp[n % 3] = memo_risp[(n - 1) % 3] + memo_risp[(n - 2) % 3]
    print(memo_risp[n%3])
