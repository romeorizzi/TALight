#!/usr/bin/env python3
from sys import stderr, exit
import re
from os import environ

ENV={}
ENV['r'] = environ["TAL_r"]
ENV['s'] = environ["TAL_s"]

feedback = {"regex" : False, "memebership" : False}

try:
    e = re.compile(ENV['r'])
    feedback["regex"] = True
except:
    pass

if not feedback["regex"]:
    print("Error! {} is not a regular expression.".format(ENV['r']))
    exit(0)    
print("Good! {} is a regular expression.".format(ENV['r']))

feedback["memebership"] = (re.fullmatch(ENV['r'], ENV['s']) is not None)

if not feedback["memebership"]:
    print("Error! {} does not belong to {}.".format(ENV['s'], ENV['r']))
    exit(0)

print("Good! {} belongs to {}.".format(ENV['s'], ENV['r']))

exit(0)
