#!/usr/bin/env python3
  
def solver(elementi,pesi,valori,Capacity):
    #print(f"elementi={elementi}\npesi={pesi}\nvalori={valori}\nCapacity={Capacity}")
    n = len(pesi)
    DPtable = [[0 for j in range(Capacity+1)] for i in range(n+1)] 
    for i in range(1,1+n):
        for j in range(Capacity+1):
            DPtable[i][j] = DPtable[i-1][j]
            if pesi[i-1] <= j and DPtable[i-1][j-pesi[i-1]] + valori[i-1] > DPtable[i][j]:
                DPtable[i][j] = DPtable[i-1][j-pesi[i-1]] + valori[i-1]
    opt_val=DPtable[i][j]
    promise = opt_val
    opt_sol = []
    while promise > 0:
        #print(f"\ni={i}\nj={j}\npromise={promise}\nelementi[i-1]={elementi[i-1]}\npesi[i-1]={pesi[i-1]}\nopt_sol={opt_sol}")
        if DPtable[i-1][j] < DPtable[i][j]:
            opt_sol.append(elementi[i-1])
            j -= pesi[i-1]
            assert j >= 0                
            promise -= valori[i-1]
        i -= 1
    #print(f"opt_sol={opt_sol}\nopt_val={opt_val}\nDPtable={DPtable}")
    return opt_val, opt_sol, DPtable
    
