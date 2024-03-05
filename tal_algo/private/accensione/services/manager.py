#!/usr/bin/env python3
from os import environ
from sys import stderr, stdout
from random import randrange, randint

from tc import TC


############## TESTCASES' PARAMETERS ############################
TL = 1   # the time limit for each testcase

HARDCODED = (
             [0, 1, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1],    
            )
DATA = tuple((1, ("hardcoded", 0,1, len(acceso), acceso)) for acceso in HARDCODED) + (
            ( 7, ("rand_gen", 1,1,     10)),
            ( 8, ("rand_gen", 0,2,   1000)),
            ( 5, ("rand_gen", 0,5,  10000)),
            ( 5, ("rand_gen", 0,3, 100000)),
        ) 
MAPPER = {"esempi_testo": 3, "small": 4, "medium": 5, "big": 6, "huge": 7}
#################################################################

def Accendi(N, acceso):
    pulsante = [None] + [0]*N
    for i in range(N, 0, -1):
        for m in range(2*i,N+1,i):
            if pulsante[m]==1:
              acceso[i] = 1-acceso[i]
        if acceso[i]==0:
            pulsante[i] = 1
    return pulsante

def Simulate(N, acceso, pulsante_risp):
    """verifica con una simulazione se tutti i PC con stato inziziale <acceso> finiranno accesi sotto <pulsante_risp>.
       Ritorna il booleano <some_PC_still_off> e se questo è True il magior indice <who> di un PC spento."""
    for i in range(N, 0, -1):
        for m in range(i,N+1,i):
            if pulsante_risp[m]==1:
              acceso[i] = 1-acceso[i]
        if acceso[i]==0:
            return True, i
        if acceso[i]==0:
            pulsante[i] = 1
    return False, None



def check(N, acceso, pulsante_risp):
    #print(f"entering check({N=}\n{acceso=}\n{pulsante_submitted=})", file = stderr)
    context = f"\nLo stato iniziale dei computer era:\n{' '.join(map(str,acceso))}"
    if len(pulsante_risp) != N:
        return False, f"La tua seconda riga di output contiene {len(pulsante_risp)} interi invece che {N=}." + context
    some_PC_still_off, who = Simulate(N, [None] + acceso, [None] + pulsante_risp)
    if some_PC_still_off:
        return False, f"Il computer di indice {who} è ancora spento dopo aver agito sui pulsati che hai indicato nella seconda riga del tuo output:\n{' '.join(map(str,pulsante_risp))}." + context + f"\nPotevi accendere tutti i PC portando invece i pulsanti nel seguente stato:\n{' '.join(map(str,Accendi(N, [None] + acceso)[1:]))}"
    return True, ""


def gen_tc(*args):
    gen_type = args[0]
    if gen_type == "hardcoded":
        points1, points2, N, acceso = args[1:]
    else:
        points1, points2, N = args[1:]
        acceso = [ randint(0,1) for _ in range(N)]
    print(N)
    print(' '.join(map(str,acceso)))
    return (points1,points2,N,acceso,)


def check_tc(points1,points2,N,acceso):
    #print(f"{N=}, {acceso=}", file=stderr)
    risp_num_sol = int(input())
    risp_pulsante = list(map(int, input().strip().split()))
    if risp_num_sol==1:
        points = points1
        feedback1 = ""
    else:
        points = 0 
        feedback1 = f"I modi per accendere tutti i PC sono 1, non {risp_num_sol}."
    ok, feedback2 = check(N,acceso,risp_pulsante)
    if ok:
        points += points2
    feedback = feedback1 + feedback2 if len(feedback1)*len(feedback2)==0 else 'Warning 1: ' + feedback1 + '\nWarning 2: ' + feedback2
    return points, feedback, points1+points2


if __name__ == "__main__":
    size = MAPPER[environ["TAL_size"]]
    tc = TC(DATA[:size], TL)
    tc.run(gen_tc, check_tc)
