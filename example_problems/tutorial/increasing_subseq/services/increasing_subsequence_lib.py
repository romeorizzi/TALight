#!/usr/bin/env python3

import itertools
import re
import random


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


def generate_random_seq(lenght, max):
    T = []
    for i in range(0, lenght):
        T.append(random.randint(0,max))
    return T

def get_rand_subseq(T):
    s=[]
    min = random.randint(0,len(T) - 1)
    while (min < len(T)):
        s.append(T[min])
        min = random.randint(min + 1,len(T)+1)
    return s

def get_not_subseq(T, s, max):
    tmp = s[:]
    while is_subseq_with_position(tmp, T)[0]:
        tmp.append(random.randint(0, max))
    return tmp

def get_n_subseq_all_diff(n):
    return (2**n) - 1

def LS(A , ordering):
    L = list()
    for i in range(0, len(A)):
        L.append(list())

    L[0].append(A[0])

    for i in range(1, len(A)):
        for j in range(0, i):
            if ordering == 'increasing':
                if (A[j] > A[i]) and (len(L[i]) < len(L[j])):
                    L[i] = []
                    L[i].extend(L[j])
            elif ordering == 'decreasing':
                if (A[j] < A[i]) and (len(L[i]) < len(L[j])):
                    L[i] = []
                    L[i].extend(L[j])
        L[i].append(A[i])
    return L

def find_ls(l):
    lung = 0
    index = []
    ret = []
    for i in l:
        if len(i) > lung:
            index.clear()
            lung = len(i)
            index.append(l.index(i))
        elif len(i) == lung:
            index.append(l.index(i))
    for i in index:
        if (l[i] not in ret):
            ret.append(l[i])
    return ret
   

def remove_duplicate_list(s):
    s = list(dict.fromkeys(s))
    return s

def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

def strictly_decreasing(L):
    return all(x>y for x, y in zip(L, L[1:]))

def non_increasing(L):
    return all(x>=y for x, y in zip(L, L[1:]))

def non_decreasing(L):
    return all(x<=y for x, y in zip(L, L[1:]))
 

def check_no_ordered_list_cert(S, a, b, ordering):
    if ordering == 'not_increasing':
        if S[a] >= S[b]:
            return True
        else:
            return False
    elif ordering == 'not_decreasing':
        if S[a] <= S[b]:
            return True
        else:
            return False

