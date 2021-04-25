#!/usr/bin/env python3
from sys import stderr, exit
import re
from os import environ


ENV={}
ENV['r'] = environ["TAL_r"]
ENV['s'] = environ["TAL_s"]

#print("Hi there, please enter a regular expression and a string.")
#print("I'll tell you if the string belongs to the regular expression.")
#pattern, string = input().split()

feedback = {"regex" : False, "string_memebership" : False}

try:
    e = re.compile(ENV['r'])
    feedback["regex"] = True
except:
    pass

if not feedback["regex"]:
    print("Error! {} is not a regular expression.".format(ENV['r']))
    exit(0)    
print("Good! {} is a regular expression.".format(ENV['r']))

feedback["string_memebership"] = (re.fullmatch(ENV['r'], ENV['s']) is not None)

if not feedback["string_memebership"]:
    print("Error! {} does not belong to {}.".format(ENV['s'], ENV['r']))
    exit(0)

print("Good! {} belongs to {}.".format(ENV['s'], ENV['r']))

exit(0)
