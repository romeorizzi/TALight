#!/usr/bin/env python
from random import random, seed
from sys import argv, exit

if( len(argv) < 2 ):
    print "Uso:", argv[0], "num [colori] [seed]"
    exit(1)

MAXCOL = 256
if len(argv) > 2:
    MAXCOL = min( MAXCOL, int(argv[2]) )

if len(argv) > 3:
    seed( int( argv[3] ) )
else:
    seed()

print int(argv[1])
for i in range( int(argv[1]) ):
    print int(random()*MAXCOL),
