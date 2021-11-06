import string

def ex_column(matrix, i): #funzione per estrarre una colonna dato un indice
    return [row[i] for row in matrix]

def count_on_row(l, row): #funzione per contare le presenze su una riga
    count=0
    if l!=0: #verifico che la riga non sia vuota
        l_bar=l+1 #gli indici sono scalati rispetto al numero di colonna
        if l_bar%2==0: #se la colonna corrente è pari
            index=int(l_bar/2)
            splitted=row[index-1:l]
            count=count+splitted.count(2)
        else: #se è dispari
            index=int(((l_bar-1)/2)+1)
            splitted=row[index-1:l]
            count=count+splitted.count(2)
    return count #ritorno il conteggio effettuato

def count_on_column(table, num, i): #semplice funzione che controlla le celle sopra a quella considerata, quando sto costruendo le successive colonne nelle prime tre righe
    if num==0:
        return 0
    if num==1 or num==2:
        if table[num-1][i]==2:
            return 1
        else:
            return 0

def build_table(m, n, mode=False): #funzione per costruire la tabella
    table=[[2,1,2],[1,2,1],[2,1,2]] #tabella 3x3 da cui partire
    n_rows=len(table) #calcolo numero righe
    n_cols=len(table[0]) #calcolo numero colonne
    if n>n_cols: #se il valore inserito è maggiore rispetto al numero di colonne corrente
        for i in range(n_cols, n): #ciclo per costruire le colonne in più
            index_bar=i+1 #gli indici sulla matrice sono spostati rispetto a quelli sulla barra di cioccolato
            if index_bar%2==0: #se la colonna è pari
                for num, line in enumerate(table,0): #ciclo sulle righe della tabella
                    #print(index_bar, num, line)
                    count=0
                    index=int(index_bar/2) #calcolo gli indici
                    splitted=line[index-1:index_bar-1]
                    count=count+splitted.count(2) #conto nella riga
                    count=count+count_on_column(table, num, i) #conto nella colonna
                    
                    if count>0: #conto la presenza di 2
                        line.append(1)
                    else:
                        line.append(2)
            else: #se è dispari
                for num, line in enumerate(table,0): #ciclo sulle righe della tabella
                    #print(index_bar, num, line)
                    count=0
                    index=int(((index_bar-1)/2)+1) #calcolo gli indici
                    splitted=line[index-1:index_bar-1]
                    count=count+splitted.count(2) #conto nella riga
                    count=count+count_on_column(table, num, i) #conto nella colonna
                    
                    if count>0: #conto la presenza di 2
                        line.append(1)
                    else:
                        line.append(2)
    if m>n_rows: #se il valore inserito è maggiore rispetto al numero di righe corrente
        for i in range(n_rows, m): #ciclo per costruire le righe in più
            index_bar=i+1
            if index_bar%2==0:
                row=[] #riga vuota che poi aggiungerò alla tabella
                for j in range(n): #ciclo sulla riga corrente per ogni colonna
                    count=0
                    column=ex_column(table, j) #estraggo la colonna sopra alla cella che sto considerando
                    index=int(index_bar/2)
                    splitted=column[index-1:index_bar-1]
                    count=count+splitted.count(2) #conto le presenze nella colonna
                    count=count+count_on_row(len(row), row) #conto le presenze a sinistra della cella che sto considerando
                    
                    if count>0:
                        row.append(1)
                    else:
                        row.append(2)
                table.append(row)
            else:
                row=[] #riga vuota che poi aggiungerò alla tabella
                for j in range(n): #ciclo sulla riga corrente per ogni colonna
                    count=0
                    column=ex_column(table, j) #estraggo la colonna sopra alla cella che sto considerando
                    index=int(((index_bar-1)/2)+1)
                    splitted=column[index-1:index_bar-1]
                    count=count+splitted.count(2) #conto le presenze nella colonna
                    count=count+count_on_row(len(row), row) #conto le presenze a sinistra della cella che sto considerando
                    
                    if count>0:
                        row.append(1)
                    else:
                        row.append(2)
                table.append(row)
    #effettuo lo slicing nel caso i valori inseriti siano minori rispetto a quelli correnti
    if n<n_cols:
        table2=[]
        for line in table:
            row=line[:n]
            table2.append(row)
        table=table2
        
    if m<n_rows:
        table=table[:m][:]
        
    #for line in table:
    #    print(line)
    #print('\n')
    
    if mode:
        if table[-1][-1]==1:
            return 1
        else:
            return 0
    
    return table

def mex(nList):
    nList = set(nList)
    nmex = 0
    while nmex in nList:
        nmex += 1
    
    return nmex

def get_up_cell(table, num, i):
    if num==0:
        return []
    if num==1 or num==2:
        return [table[num-1][i]]
        
def get_row(l, row): #funzione per contare le presenze su una riga
    numb=[]
    if l!=0: #verifico che la riga non sia vuota
        l_bar=l+1 #gli indici sono scalati rispetto al numero di colonna
        if l_bar%2==0: #se la colonna corrente è pari
            index=int(l_bar/2)
            splitted=row[index-1:l]
            numb.extend(splitted)
        else: #se è dispari
            index=int(((l_bar-1)/2)+1)
            splitted=row[index-1:l]
            numb.extend(splitted)
    return numb #ritorno la riga
        
def get_grundy_value(m, n): #funzione per costruire la tabella
    table=[[0,1,0],[1,0,1],[0,1,0]] #tabella 3x3 da cui partire
    n_rows=len(table) #calcolo numero righe
    n_cols=len(table[0]) #calcolo numero colonne
    if n>n_cols: #se il valore inserito è maggiore rispetto al numero di colonne corrente
        for i in range(n_cols, n): #ciclo per costruire le colonne in più
            index_bar=i+1 #gli indici sulla matrice sono spostati rispetto a quelli sulla barra di cioccolato
            if index_bar%2==0: #se la colonna è pari
                for num, line in enumerate(table,0): #ciclo sulle righe della tabella
                    #print(index_bar, num, line)
                    numb=[]
                    index=int(index_bar/2) #calcolo gli indici
                    splitted=line[index-1:index_bar-1]
                    numb.extend(splitted) #attacco la riga
                    numb.extend(get_up_cell(table, num, i)) #attacco la cella
                    
                    line.append(mex(numb))
            else: #se è dispari
                for num, line in enumerate(table,0): #ciclo sulle righe della tabella
                    #print(index_bar, num, line)
                    numb=[]
                    index=int(((index_bar-1)/2)+1) #calcolo gli indici
                    splitted=line[index-1:index_bar-1]
                    numb.extend(splitted) #attacco la riga
                    numb.extend(get_up_cell(table, num, i)) #attacco la cella
                    
                    line.append(mex(numb))
    if m>n_rows: #se il valore inserito è maggiore rispetto al numero di righe corrente
        for i in range(n_rows, m): #ciclo per costruire le righe in più
            index_bar=i+1
            if index_bar%2==0:
                row=[] #riga vuota che poi aggiungerò alla tabella
                for j in range(n): #ciclo sulla riga corrente per ogni colonna
                    numb=[]
                    column=ex_column(table, j) #estraggo la colonna sopra alla cella che sto considerando
                    index=int(index_bar/2)
                    splitted=column[index-1:index_bar-1]
                    numb.extend(splitted) #attacco la colonna
                    numb.extend(get_row(len(row), row)) #attacco le celle della riga
                    row.append(mex(numb))
                table.append(row)
            else:
                row=[] #riga vuota che poi aggiungerò alla tabella
                for j in range(n): #ciclo sulla riga corrente per ogni colonna
                    numb=[]
                    column=ex_column(table, j) #estraggo la colonna sopra alla cella che sto considerando
                    index=int(((index_bar-1)/2)+1)
                    splitted=column[index-1:index_bar-1]
                    numb.extend(splitted) #attacco la colonna
                    numb.extend(get_row(len(row), row)) #attacco le celle della riga
                    row.append(mex(numb))
                table.append(row)
    #effettuo lo slicing nel caso i valori inseriti siano minori rispetto a quelli correnti
    if n<n_cols:
        table2=[]
        for line in table:
            row=line[:n]
            table2.append(row)
        table=table2
        
    if m<n_rows:
        table=table[:m][:]
        
    #for line in table:
    #    print(line)
    #print('\n')
    
    return table

def find_move(m, n):
    for s in range(1, n // 2 + 1):
        if not build_table(m - s, n, True):
            return (0, s)
    for s in range(1, m // 2 + 1):
        if not build_table(m, n - s, True):
            return (1, s)
    
def winning_move(m,n):
    (direction, sz) = find_move(m, n)
    if(direction):
        return (m,n-sz)
    else:
        return (m-sz,n)
