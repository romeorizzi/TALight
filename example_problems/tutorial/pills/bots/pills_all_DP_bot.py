#!/usr/bin/env python3
from sys import argv, stdout, stderr

MAX_N = 1000

# num_sols[n_pills] = number of feasible treatment with <n_pills> pills.
# A treatment with n pills is a string of n 'I' characters and n 'H' characters such that no prefix contains more 'H's than 'I's and every 'I' matches with the first 'H' after it that brings back the balance.

num_sols = [1] * (MAX_N+1) # while allocating this we also set up the correct value for the two base cases

for n_pills in range(2,MAX_N+1):
    num_sols[n_pills] = 0
    for n_pills_included in range(n_pills):
        num_sols[n_pills] += num_sols[n_pills_included] * num_sols[n_pills - n_pills_included -1] 

def num_sol(n_pills):
    assert n_pills <= MAX_N
    return num_sols[n_pills]

def unrank(n_pills, pos, sorting_criterion="loves_I"):
    if n_pills == 0:
        return ""
    """I  ... H  ...
           A      B
    """    
    count = 0
    for n_pills_in_A in range(n_pills) if sorting_criterion=="loves_H" else reversed(range(n_pills)):
        num_A = num_sol(n_pills_in_A)
        num_B = num_sol(n_pills - n_pills_in_A -1)
        if count + num_A*num_B > pos:
            break
        count += num_A*num_B
    return "I" + unrank(n_pills_in_A, (pos-count) // num_B, sorting_criterion) + "H" + unrank(n_pills - n_pills_in_A -1, (pos-count) % num_B, sorting_criterion)

def rank(sol, sorting_criterion="loves_I"):
    if sol == "":
        return 0
    num_dangling_broken_pills = 0
    for char, i in zip(sol,range(len(sol))):
        if char == 'I':
            num_dangling_broken_pills += 1
        else:
            num_dangling_broken_pills -= 1
            if num_dangling_broken_pills == 0:
                break
    assert  i%2 == 1
    """
       I  ... H  ...    with len(A) even
       0   A  i    B
    """
    n_pills = len(sol)//2
    count = 0
    if sorting_criterion=="loves_I":
        for ii in range(i+2, len(sol)+1, 2):
            n_pills_A = ii//2
            n_pills_B = n_pills - n_pills_A -1
            num_A = num_sol(n_pills_A)
            num_B = num_sol(n_pills_B)
            count += num_A*num_B
    if sorting_criterion=="loves_H":
        for ii in range(1, i-1, 2):
            n_pills_A = ii//2
            n_pills_B = n_pills - n_pills_A -1
            num_A = num_sol(n_pills_A)
            num_B = num_sol(n_pills_B)
            count += num_A*num_B
    n_pills_A = i//2
    n_pills_B = n_pills - n_pills_A -1
    num_B = num_sol(n_pills_B)
    return count + rank(sol[1:i], sorting_criterion)*num_B + rank(sol[i+1:len(sol)+1], sorting_criterion)

def next_sol(sol):
    n_pills = len(sol) // 2
    r = rank(sol)
    assert r < num_sol(n_pills) -1
    return unrank(n_pills, r+1)


def num_sol_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            print(num_sol(int(tmp)))

def unrank_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            n, r = map(int, tmp.split())
            print(unrank(n, r))

def rank_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            print(rank(tmp))

def next_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            print(next_sol(tmp))

usage=f"""I am a general (non efficient) purpouse bot with the following functionalities:
  1. num_sol
  2. rank
  3. unrank
  4. next
You should call me as follows:
$ {argv[0]} <evalution service>
"""
if len(argv) != 2:
    print(f"WARNING from bot {argv[0]}: called with the wrong number of parameters.")
    print(usage)
    exit(1)

if argv[1] == 'num_sol':
    num_sol_bot()
if argv[1] == 'rank':
    rank_bot()
if argv[1] == 'unrank':
    unrank_bot()
if argv[1] == 'next':
    next_bot()
