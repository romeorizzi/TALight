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

min = 0
max = n - 1
last_left = 0
first_right = 0

for i in range(n):
    collocaMoneta(i, NONE)

while min < max:
    nAlive = max - min + 1
    for i in range((nAlive + 1) // 3):
        collocaMoneta(min + i, LEFT)
        last_left = min + i
        collocaMoneta(max - i, RIGHT)
        first_right = max - i

    risp = piatto_con_peso_maggiore()
    for i in range((nAlive + 1) // 3):
        collocaMoneta(min + i, NONE)
        collocaMoneta(max - i, NONE)

    if risp == NONE:  # Allora la moneta e' tra quelle non pesate
        min = last_left + 1
        max = first_right - 1

    if risp == LEFT:  # la moneta leggera e' tra quelle sul piatto RIGHT
        min = first_right

    if risp == RIGHT:  # la moneta leggera e' tra quelle sul piatto LEFT
        max = last_left

denuncia(min)
