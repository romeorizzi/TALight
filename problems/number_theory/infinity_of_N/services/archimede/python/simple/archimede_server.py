#!/usr/bin/env python3

from os import environ
#from sys import exit
import random

ENV_num_rounds = int(environ["TAL_num_rounds"])

def random_decimal_string_smaller_than(decimal_string):
    """
    a decimal_string is a non-empty string of digits whose last digit is different than 0.
    """
    assert decimal_string[-1] != "0"
    tmp = decimal_string[:]
    pos = 0
    while tmp[pos] == "0":
        pos += 1
    tmp = tmp[:pos] + chr(ord("0") + random.randrange(int(tmp[pos])))
    if tmp[-1] == "0":
        tmp += chr(ord("0") + random.randrange(1,10))
    assert tmp[-1] != "0"
    return tmp

def decimals_of_reciprocal_of(n, length):
    assert n > 1
    risp = ""
    div = 10
    while length > 0:
        length -= 1
        risp += chr(ord("0") + div//n)
        div = (div%n)*10
    return risp

                   
print(f"# I will serve: problem=infinity_of_N, service=archimede, num_rounds={ENV_num_rounds}.")

my_real_int_part = random.randrange(20)
my_real_dec_part = random_decimal_string_smaller_than("9")
                   
for _ in range(ENV_num_rounds):
    print(f"{my_real_int_part}.{my_real_dec_part}")
    spoon = input().strip()
    while spoon[0] == '#':
        spoon = input().strip()
    your_n = int(spoon)
    if your_n == 0:
        print(f"You just replied with {your_n} to {my_real_int_part}.{my_real_dec_part}. However, you can reply only with POSITIVE natural numbers! Your bot has lost this match, whence the proof is missing.")
        exit(0)
    if my_real_int_part == 0: # otherwise your_n is already good since our decimal part is never null
        if your_n == 1 or decimals_of_reciprocal_of(your_n, len(my_real_dec_part)) >= my_real_dec_part:
            print(f"You just replied with n={your_n} to 0.{my_real_dec_part}. However, the decimal representation of 1/n begins in {1 if your_n == 1 else 0}.{decimals_of_reciprocal_of(your_n, len(my_real_dec_part)) if your_n > 1 else 0} >= 0.{my_real_dec_part}. Your bot has lost this match, whence the proof is missing.")
            exit(0)
    if my_real_int_part > 0:
        my_real_int_part = random.randrange(my_real_int_part)
    my_real_dec_part = random_decimal_string_smaller_than(my_real_dec_part)


print(f"! I give up. You won!")    
exit(0)
