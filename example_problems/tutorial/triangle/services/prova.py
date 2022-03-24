#!/usr/bin/env python3
from sys import stderr

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
ENV = 'diocane'
TAc = 'porcodio'
TALf = TALfilesHelper(TAc, ENV)

TALf.str2output_file(500,f'prova.txt')
