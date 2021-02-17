#!/usr/bin/env python3

from os import environ
from sys import exit
import string 
import random

from hash_and_cipher import hash_value

ENV_num_rounds = int(environ.get("TAL_num_rounds"))
ENV_hash_type = environ.get("TAL_hash_type")

print(f"# I will serve: problem=morra, service=play, num_rounds={ENV_num_rounds}, hash_type={ENV_hash_type}.")

"""
With a different protocol we could attempt to take profit of a possible ingenuity on the side of the problem solver: 
def brake_secret_attempt(prev_secret_str_adversary, curr_hash_str_adversary):
    for guess_m in range(5):
        for guess_s in range(9):
            white_string_guess = chr(m+ord("0")) + "_" + chr(s+ord("0")) + "_" + prev_secret_str_adversary
            if curr_hash_str_adversary==str(hash_value(prev_secret_str_adversary)):
                return m,s
    return None
"""

score_mine = 0
score_yours = 0
cheated = 0
#prev_secret_str_yours = None
for i in range(1,ENV_num_rounds+1):
    print("?")
    m = random.randrange(5)
    s = m + random.randrange(5)
    alphabet_string = string.ascii_letters + string.digits
    white_string_mine = chr(m+ord("0")) + "_" + chr(s+ord("0")) + "_" + ''.join(random.choices(alphabet_string, k=60))
    hash_str_mine = str(hash_value(white_string_mine,ENV_hash_type))
    print(f"{hash_str_mine}")
    hash_str_yours = input().strip()
    while hash_str_yours[0] == '#':
        hash_str_yours = input().strip()
    print(f"{white_string_mine}")
    white_str_yours = input().strip()
    while white_str_yours[0] == '#':
        white_str_yours = input().strip()
    #prev_secret_str_yours = white_str_yours[4:]     
    should_be = str(hash_value(white_str_yours,ENV_hash_type))
    if hash_str_yours != should_be:
        print(f"No! You tried to cheat: h({white_str_yours}) = {should_be} != {hash_str_yours}.")
        score_mine += 10
        cheated += 1
    else:
        m_yours = ord(hash_str_yours[0])-ord("0")
        s_yours = ord(hash_str_yours[2])-ord("0")                       
        if s_yours == m + m_yours:
            score_yours += 1                  
        if s == m + m_yours:
            score_mine += 1                  

print(f"Your score: {score_yours}. My score: {score_mine}. You cheated {cheated} times.")
            
exit(0)
