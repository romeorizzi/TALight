from sys import argv

def switch_row(i,pirellone):
    for j in range(len(pirellone[0])):
        pirellone[i][j] = int(not pirellone[i][j])
    return

def switch_col(j,pirellone):
    for i in range(len(pirellone)):
        pirellone[i][j] = int(not pirellone[i][j])
    return


def is_solvable(pirellone, n, m):
    for i in range(n):
        inv = pirellone[0][0] != pirellone[i][0]
        for j in range(m):
            v = not pirellone[i][j] if inv else pirellone[i][j]
            if v != pirellone[0][j]:
                return False
    return True 

def my_soluzione(pirellone,n,m):
    if is_solvable(pirellone, n, m):
        R=[0]*len(pirellone)
        C=[0]*len(pirellone[0])
    for i in range(0,n):    
        for j in range(0,m):
            if pirellone[i][j]:
                C[j] = 1
                switch_col(j,pirellone)
    for i in range(0,n):
         if pirellone[i][0]:
            R[i] = 1
            switch_row(i,pirellone)
    lista=[]
    for i in range(n):
        if R[i]:
            lista.append(f"r{i+1}")
    for j in range(m):
        if C[j]:
            lista.append(f"c{j+1}")
    return lista


    
def num_sol_bot():
    while True:
        tmp = input()
        tmp=tmp.split()
        if tmp[0] != '#':
            print(my_soluzione(tmp,len(tmp),len(tmp[0])))

if argv[1] == 'prova':
    num_sol_bot()