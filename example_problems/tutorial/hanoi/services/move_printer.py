#!/usr/bin/env python3
from sys import stderr, exit, argv

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors



def get_move(disk, current, target, lang=None):
    return f'Move disk {disk} from {current} to {target}'
