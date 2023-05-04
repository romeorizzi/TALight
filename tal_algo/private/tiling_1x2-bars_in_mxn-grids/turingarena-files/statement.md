# Ricopertura di una griglia mxn tramite tessere del domino (barre 1x2)

Ecco una ricopertura (tiling) di una griglia 8x8 (come la scacchiera) tramite barre 1x2:

<!--- ![](https://upload.wikimedia.org/wikipedia/commons/a/a4/Pavage_domino.svg) -->
![esempio di tiling](figs/Pavage_domino.svg)

Quindi la griglia 8x8 ammette un tiling con tessere del domino.

Assegnati due numeri naturali m ed n, il tuo programma deve stabilire se la griglia mxn ammetta anche essa un tiling con tessere del domino.

Nei casi in cui la tua risposta sia affermativa, riesci ad esibire un tale tiling disponendo le tessere una ad una?

Nei casi in cui la tua risposta sia negativa, vuoi esprimere una ragione per cui un tale tiling non possa esistere?


goal 1: decidere, m = 1, n <= 100
goal 2: decidere, 1 <= m, n <= 10
goal 3: decidere, 1 <= m, n <= 100
goal 4: decidere, 1 <= m, n <= 100.000
goal 5: costruire il tiling, m = 1, n <= 100
goal 6: costruire il tiling, 1 <= m, n <= 10
goal 7: costruire il tiling,  1 <= m, n <= 100

Non avendo pre-accordato un linguaggio comune per le ragioni di non-esistenza, quella parte, benchè preziosa, non è oggetto della valutazione automatica. Gli argomenti per la non'esistenza potranno essere invece disussi in classe.

Per collocare le tessere nella griglia, la procedura `compose_tiling` che sei chiamato ad implementare si avvale della callback `place_tile(row,col,dir)` che colloca una tessera in orizzontale se `dir = H` e in vertiale  se `dir = V`. I primi due parametri indicano la posizione dell'angolo in alto a sinistra della tessera entro la griglia. Le righe della griglia mxn sono numerate da 1 ad m; le colonne da 1 a n. 
