#!/usr/bin/env python3
# problem: lightCoin, Romeo Rizzi Jan 2015
from grader import (
    ottieni_numero_monete,
    piatto_con_peso_maggiore,
    collocaMoneta,
    denuncia,
    NONE,
    LEFT,
    RIGHT)

n = ottieni_numero_monete()

collocaMoneta(0, NONE)
collocaMoneta(1, LEFT)
collocaMoneta(2, RIGHT)

risp = piatto_con_peso_maggiore()

if risp == NONE:
    denuncia(NONE)

if risp == LEFT:
    denuncia(RIGHT)

if risp == RIGHT:
    denuncia(LEFT)
