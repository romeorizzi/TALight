#!/usr/bin/env python3
from sys import argv, stdout, stderr

def num_sol(num_pairs):
    if num_pairs == 0:
        return 1
    risp = 0
    for n_pairs_included in range(num_pairs):
        risp += num_sol(n_pairs_included) * num_sol(num_pairs - n_pairs_included -1) 
    return risp

def unrank(n_pairs, pos, sorting_criterion="loves_opening_par"):
    if n_pairs == 0:
        return ""
    """(  ... )  ...
           A      B
    """    
    count = 0
    for n_pairs_in_A in range(n_pairs) if sorting_criterion=="loves_closing_par" else reversed(range(n_pairs)):
        num_A = num_sol(n_pairs_in_A)
        num_B = num_sol(n_pairs - n_pairs_in_A -1)
        if count + num_A*num_B > pos:
            break
        count += num_A*num_B
    return "(" + unrank(n_pairs_in_A, (pos-count) // num_B, sorting_criterion) + ")" + unrank(n_pairs - n_pairs_in_A -1, (pos-count) % num_B, sorting_criterion)

def rank(wff, sorting_criterion="loves_opening_par"):
    if wff == "":
        return 0
    num_dangling_open = 0
    for char, i in zip(wff,range(len(wff))):
        if char == '(':
            num_dangling_open += 1
        else:
            num_dangling_open -= 1
            if num_dangling_open == 0:
                break
    assert  i%2 == 1
    """
       (  ... )  ...    with len(A) even
       0   A  i    B
    """
    n_pairs = len(wff)//2
    count = 0
    if sorting_criterion=="loves_opening_par":
        for ii in range(i+2, len(wff)+1, 2):
            n_pairs_A = ii//2
            n_pairs_B = n_pairs - n_pairs_A -1
            num_A = num_sol(n_pairs_A)
            num_B = num_sol(n_pairs_B)
            count += num_A*num_B
    if sorting_criterion=="loves_closing_par":
        for ii in range(1, i-1, 2):
            n_pairs_A = ii//2
            n_pairs_B = n_pairs - n_pairs_A -1
            num_A = num_sol(n_pairs_A)
            num_B = num_sol(n_pairs_B)
            count += num_A*num_B
    n_pairs_A = i//2
    n_pairs_B = n_pairs - n_pairs_A -1
    num_B = num_sol(n_pairs_B)
    return count + rank(wff[1:i], sorting_criterion)*num_B + rank(wff[i+1:len(wff)+1], sorting_criterion)

def next_wff(wff):
    n_pairs = len(wff) // 2
    r = rank(wff)
    assert r < num_sol(n_pairs) -1
    return unrank(n_pairs, r+1)


def num_sol_bot():
    while True:
        tmp = input()
        if tmp[0] != '#':
            print(num_sol(int(tmp)))

def unrank_bot():
    while True:
        tmp = input()
        if tmp[0] != '#':
            n, r = map(int, tmp.split())
            print(unrank(n, r))

def rank_bot():
    while True:
        tmp = input()
        if tmp[0] != '#':
            print(rank(tmp))

def next_sol_bot():
    while True:
        tmp = input()
        if tmp[0] != '#':
            print(next_wff(tmp))

if argv[1] == 'num_sol':
    num_sol_bot()
if argv[1] == 'rank':
    rank_bot()
if argv[1] == 'unrank':
    unrank_bot()
if argv[1] == 'next_sol':
    next_sol_bot()
