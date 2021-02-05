#!/usr/bin/env python3

from sys import exit, argv
import string 
import random

from hash_and_cipher import hash_value

HASH_TYPE = "rabin_karp"
if len(argv) == 2:
    HASH_TYPE = argv[1]
    
score_mine = 0
score_yours = 0
while True:
    m = random.randrange(5)
    s = m + random.randrange(5)
    alphabet_string = string.ascii_letters + string.digits
    white_string_mine = chr(m+ord("0")) + "_" + chr(s+ord("0")) + "_" + ''.join(random.choices(alphabet_string, k=60))
    hash_str_mine = str(hash_value(white_string_mine,HASH_TYPE))
    spoon = input().strip()
    while spoon[0] != '?':
        spoon = input().strip()
    print(f"{hash_str_mine}")
    hash_str_yours = input().strip()
    while hash_str_yours[0] == '#':
        hash_str_yours = input().strip()
    print(f"{white_string_mine}")
    white_str_yours = input().strip()
    while white_str_yours[0] == '#':
        white_str_yours = input().strip()
    should_be = str(hash_value(white_str_yours,HASH_TYPE))
    if hash_str_yours != should_be:
        print(f"Ouch! h({white_str_yours}) = {should_be} != {hash_str_yours}.")
        exit(1)
    else:
        m_yours = ord(hash_str_yours[0])-ord("0")
        s_yours = ord(hash_str_yours[2])-ord("0")                       
        if s_yours == m + m_yours:
            score_yours += 1                  
        if s == m + m_yours:
            score_mine += 1                  

print(f"Your score: {score_yours}. My score: {score_mine}.")
            
exit(0)
