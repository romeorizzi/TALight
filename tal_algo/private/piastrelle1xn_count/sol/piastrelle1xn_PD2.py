#!/usr/bin/python
"""una soluzione semplice, che non si preoccupa di rispettare il protocollo per il dialogo col manager della sottoposizione offerto dal servizio solve. E' riscritta per rispettare tale protocollo nel file sol_PD2.py."""

memo_risp = [None] * 3
memo_risp[0] = memo_risp[1] = 1

N = int(input("N="))

for n in range(2, N + 1):
    memo_risp[n % 3] = memo_risp[(n - 1) % 3] + memo_risp[(n - 2) % 3]

print(f"Le piastrellature sono {memo_risp[n%3]}.")
