#!/usr/bin/env python3

import itertools
import re


def parse_input(string):
    string = remove_duplicate_spaces(string)
    l = list(string.split(" "))
    return l

def is_subseq(s, T):
    it = iter(T)
    return all(any(c == ch for c in it) for ch in s)

def remove_duplicate_spaces(T):
    return re.sub(' +', ' ', T)

def is_subseq_with_position(s, T):

    pos = []
    c_i = 0
    i = 0
    while (c_i < len(T) and i < len(s)):
        
        if T[c_i] == s[i]: 
            i+=1
            pos.append(c_i)
        c_i +=1
    if i == len(s):
        return [True, pos]
    else:
        return [False, pos]

def get_yes_certificate(T, pos):
    cert = ""
    index = 0
    i = 0
    while (i < len(T) and index < len(pos)):
        num_ciphers = len(str(T[i]))
        
        if i == pos[index]:
            index+=1
            for _ in range(0, num_ciphers):
                cert+= "^"
        else:
            for _ in range(0, num_ciphers):
                cert+= " " 
        cert+= " "
        i+=1
    return cert

    
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




   
 