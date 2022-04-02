#!/usr/bin/env python3
from sys import stderr, exit
import re
from os import environ

ENV={}
ENV['r'] = environ["TAL_r"]
ENV['s'] = environ["TAL_s"]

try:
    e = re.compile(ENV['r'])
except:
    print("Error! {} is not a regular expression.".format(ENV['r']))
    exit(0)    

print("Good! {} is a regular expression.".format(ENV['r']))

if re.fullmatch(ENV['r'], ENV['s']) is None:
    print("Error! {} does not belong to {}.".format(ENV['s'], ENV['r']))
    exit(0)

print("Good! {} belongs to {}.".format(ENV['s'], ENV['r']))

exit(0)
