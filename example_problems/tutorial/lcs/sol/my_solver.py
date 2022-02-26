#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse

SOL_FORMAT = 'annotated_subseq'
INST_FORMAT = 'only_strings'
AVAILABLE_FORMATS = {'instance':{'only_strings':'only_strings.txt', 'with_m_and_n':'with_m_and_n.txt', 'gmpl_dat1':'dat'},'solution':{'subseq':'subseq.txt', 'annotated_subseq':'annotated_subseq.txt'}}

usage=f"""\nSono il programma che risolve questo problema. Ricevo l'istanza da stdin ed invio su stdout la soluzione. Puoi specificare il formato di input (istanza) e di output (soluzione) utilizzando i miei argomenti opzionali. La sintassi con cui chiamarmi è la seguente:

Usage: {os.path.basename(sys.argv[0])} [--inst_format] [--sol_format]

Il valore di default per `inst_format` è '{INST_FORMAT}', quello per `sol_format` è '{SOL_FORMAT}'.
I set di valori disponibili per `inst_format` è {list(AVAILABLE_FORMATS['instance'].keys())}, quello per `sol_format` è {list(AVAILABLE_FORMATS['solution'].keys())}.

"""

def opt_val_and_sol(s, t):
    """returns the maximum length of a common subsequence of strings s and t, and an optimal LCS(s,t)
    """
    #print(f"opt_val_and_sol called with {s=} and {t=}")
    m = len(s); n = len(t)
    risp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m):
        for j in range(n):
            if s[i] == t[j]:
                risp[i+1][j+1] = 1 + risp[i][j]
            else:
                risp[i+1][j+1] = max(risp[i+1][j],risp[i][j+1])
    opt_val = risp[m][n]
    an_opt_solution = {}
    while m > 0 and n > 0:
        if s[m-1] == t[n-1]:
            an_opt_solution[(m-1, n-1)] = s[m-1]
            m-=1
            n-=1
        elif risp[m-1][n] > risp[m][n-1]:
            m-=1
        else:
            n-=1
    return opt_val, an_opt_solution


if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=usage,
    epilog="""-------------------""")
    parser.add_argument('--sol_format', type=str, help=f'use this optional argument to specify the intended format of your solutions.', default=SOL_FORMAT)
    parser.add_argument('--inst_format', type=str, help=f'use this optional argument to specify the intended format of your instances.', default=INST_FORMAT)

    args = parser.parse_args()

    if args.sol_format:
        SOL_FORMAT=args.sol_format
        SOL_EXT = AVAILABLE_FORMATS['solution'][SOL_FORMAT]
    if args.inst_format:
        INST_FORMAT=args.inst_format
        INST_EXT = AVAILABLE_FORMATS['instance'][INST_FORMAT]

    if args.inst_format=='with_m_and_n':
        m,n = map(int,input().split())
    s = input()
    t = input()
    if args.inst_format=='with_m_and_n':
        assert m == len(s)
        assert n == len(t)
    m = len(s)
    n = len(t)
    
    opt_val, an_opt_sol_annotated_subseq = opt_val_and_sol(s, t)
    if args.sol_format=='annotated_subseq':
        print('\n'.join([f'{an_opt_sol_annotated_subseq[key]} {key[0]} {key[1]}' for key in sorted(an_opt_sol_annotated_subseq)]))
    if args.sol_format=='subseq':
        print("".join(char for char in [an_opt_sol_annotated_subseq[key] for key in sorted(an_opt_sol_annotated_subseq)]))
