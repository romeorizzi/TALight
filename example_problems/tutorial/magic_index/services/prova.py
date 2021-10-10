#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

def num_questions_worst_case2(n):
    if n==0:
        return 0
    else:
        return 1 + num_questions_worst_case_support2((n-1)//2) + num_questions_worst_case_support2((n-1)//2 + ((n-1)%2) )

def num_questions_worst_case_support2(n):
    if n==0:
        return 0
    else:
        return 1+num_questions_worst_case_support2( (n-1)//2 + ((n-1)%2) )


def num_questions_worst_case(n):
    return num_questions_worst_case_support(n, n)

def num_questions_worst_case_support(n, nOriginal):
    """
    Args:
        n: the vector lenght 
        nOriginal: the original vector lenght. it is used at the end to sum n/2 rounded down

    Returns:
        questions: the minumum number of questions to spot all the magic indexes in the worst case
    """

    #base case
    if n == 0:
        return 0 + nOriginal//2 #default rounded down
    if n == 1:
        return 1 + nOriginal//2 #default rounded down
    
    return 1 + num_questions_worst_case_support((int(math.ceil(n / 2))) - 1, nOriginal)

for n in range(20):
    print(f"{n:3}", end=" ")
print()
for n in range(20):
    print(f"{num_questions_worst_case(n):3}", end=" ")
print()
for n in range(20):
    print(f"{num_questions_worst_case2(n):3}", end=" ")    
print()
