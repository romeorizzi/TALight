#!/usr/bin/env python3
from sys import stderr, exit

import random
from IPv4_lib import *

subnet=subnet_mask()
internet=net_address(subnet)
print("SUBNET MASK:  ",subnet)
print("INTERNET ADDRESS:  ",internet)
list_all(internet)
