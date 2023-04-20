#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""
 *  percorso di soluzione condotto per specchio
 *  Romeo Rizzi, 2023-04-18
"""
from sys import stderr

T = int(input())
for _ in range(T):
    num_figli = list(map(int, input().strip().split()))
    print(f"\n\n{num_figli=}", file = stderr)
    """
    Ad esempio, voglio andare da:
    4 2 0 3 0 0 1 0 0 0 0
    a:
    4 0 0 0 2 3 1 0 0 0 0

    Ci siamo proposti di farlo in 3 steps:

    Step 1:

    produrre la lista dei figli per ciascun nodo:
    lista_figli = [ [1, 8, 9, 10], [2, 3], [], [4, 5, 6], [], [], [7], [], [], [], [] ]

    Step 2:
    la lista_figli offre una rappresentazione dell'albero in input.
    Riusciamo a rovesciarlo entro tale rappresentazione?

    Step 3:
    scrivere la codifica dell'albero rovesciato.
    """

    # Step 1:
    lista_figli = []
    primo_nome_disp = 0
    def dfs_riempi_lista_figli():
        global primo_nome_disp
        tizio = primo_nome_disp
        primo_nome_disp += 1
        lista_figli.append([]) # per ospitare i figli di tizio
        for _ in range(num_figli[tizio]):
            nome_figlio = dfs_riempi_lista_figli()
            lista_figli[tizio].append(nome_figlio)
        return tizio
    dfs_riempi_lista_figli()
    print(f"{lista_figli=}", file=stderr)
    
    # Step 2:
    """
    Step 2:

    cerchiamo di capire meglio, voglio andare da:
    lista_figli = [ [1, 8, 9, 10], [2, 3], [], [4, 5, 6], [], [], [7], [], [], [], [] ]
    a:

    lista_figli_albero_riflesso_A = [ [1, 2, 3, 4], [], [], [], [5, 10], [6 , 8, 9], [7], [], [], [], [] ], dove i nodi sono stati rinominati secondo l'ordine di vista DFS nell'albero rovesciato

    oppure a:
    lista_figli_albero_riflesso_B = [ [10, 9, 8, 1], [3, 2], [], [6, 5, 4], [], [], [7], [], [], [], [] ], dove i nodi hanno mantenuto lo stesso nome (dato dall'ordine di vista DFS nell'albero originale)

    Il primo sembra più difficile da fare, perche' di fatto è' come non sfruttare i nomi che abbiamo introdotto nello Step 1. Ma forse conviene fare così per facilitare lo Step 3 (che se facciamo così è ovvio, si fà la DFS).


    Questo Step 2 è il passo cuore del problema, abbiamo pertanto sbirciato prima cosa davvero ci serva per portare a casa il passo 3. Abbiamo così scoperto che ci basta realizzare quanto nel caso B.
    Pertanto facciamolo:
    """

    lista_figli_albero_riflesso_B = []
    for i in range(len(lista_figli)):
      lista_figli_albero_riflesso_B.append((lista_figli[i][::-1]))
    print(f"{lista_figli_albero_riflesso_B=}", file=stderr)

    # Step 3:
    # prima sotto ipotesi A, dove è facile:
    def dfs_dichiara_anagrafe_A(adamo):
        num_figli_adamo = len(lista_figli_albero_riflesso_A[adamo])
        print(num_figli_adamo, end = " ", file = stderr)
        for figlio in lista_figli_albero_riflesso_A[adamo]:
          dfs_dichiara_anagrafe_A(figlio)

    lista_figli_albero_riflesso_A = [ [1, 2, 3, 4], [], [], [], [5, 10], [6 , 8, 9], [7], [], [], [], [] ]
    # da chiamarsi con:
    dfs_dichiara_anagrafe_A(adamo = 0); print(file = stderr)
    # ma in realtà scopriamo che è altrettanto facile produrre la stringa che codifica l'albero secondo la rappresentazione B. Di fatto possiamo usare la stessa identica funzione (ho solo rinominato le variabili):

    def dfs_dichiara_anagrafe_B(adamo):
        num_figli_adamo = len(lista_figli_albero_riflesso_B[adamo])
        print(num_figli_adamo, end = " ")
        for figlio in lista_figli_albero_riflesso_B[adamo]:
          dfs_dichiara_anagrafe_B(figlio)

    dfs_dichiara_anagrafe_B(adamo = 0)
    print()
