#!/usr/bin/env python3

import itertools


def parse_input(string):
    l = list(string.split(" "))
    return l

def is_subseq(s, T):
    it = iter(T)
    return all(any(c == ch for c in it) for ch in s)


def sub_sequences_num(T):
    combs = []
    seq_num = 0
    for l in range(1, len(T)+1):
        combs.append(list(itertools.combinations(T, l)))
    for c in combs:
        for t in c:
            seq_num+=1
    return seq_num


def sub_sequences(T):
    sub_seq = []
    combs = []
    for l in range(1, len(T)+1):
        combs.append(list(itertools.combinations(T, l)))
    for c in combs:
        for t in c:
            string = ""
            for i in t:
                string += str(i)
            sub_seq.append(string)
    return sub_seq  #list of string

def ordered_sub_sequences(T):
    tmp = sub_sequences(T)
    tmp.sort()
    return tmp




   
 