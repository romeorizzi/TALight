# Triangolo (Discesa): costruzione di una soluzione ottima
   
Ti viene dato un triangolo di numeri interi tutti presi dall'intervallo [0,9]:
```
       4
      1 5
     7 2 3
    1 2 1 2
   1 5 3 3 3
```
   
Consideriamo ammissibile un percorso che discenda dal vertice in alto (quì di valore 4) visitando precisamente uno dei valori per ciascuna riga senza mai compiere salti eccessivi, nè verso sinistra nè verso destra. In pratica, nel passare da una riga alla successiva, non essendo presente un elemento immediatamente sottostante, l'unica scelta consentita è quella di portarsi verso sinistra oppure verso destra, ma solo fino al primo elemento della riga successiva che si incontra in tale direzione.
Si richiede di restituire un percorso ammissibile di massimo valore.


## Input
La prima riga contiene $T$, il numero di testcase da risolvere. Seguono $T$
istanze del problema. Ogni istanza è composta nel seguente modo: la prima
riga fornisce $n$, il numero di righe del triangolo.
Seguono le n righe del triangolo allineate tutte a sinistra.

## Output
L'output atteso consta di due righe per ogni testcase: la prima riga deve contenere il massimo valore di un percorso ammissibile, la seconda conterrà codifica di un percorso ammissibile di massimo valore. Tale codifica è una stringa di lunghezza $n-1$ sull'alfabeto $\{L,R\}$ (sinistra/destra, si specifichino le scelte come a partire dal vertice in alto).


## Esempio

### Input
```
2
1
7
5
4
1 5
7 2 3
1 2 1 2
1 5 3 3 3
```
Spiegazione: due testcase, il primo dei quali è un triangolo di una sola riga (e quindi di un solo valore intero, il 7). Il secondo triangolo ha invece 5 righe.

### Output
```
7

19
LLRL
```

Spiegazione: nel primo testcase, la soluzione ottima ha valore 7 ed è specificata dalla stringa vuota. Nel secondo testcase una soluzione ottima (un percorso di valore 19) è specificata dalla stringa di navigazione "LLRL" (sinistra, sinistra, destra, sinistra).


## Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

Per il subtasking sono previste le seguenti `size`, dove il default è `big` che include anche i testcase `medium`, `small` e `tiny`:

* `tiny`: $n \leq 7$
* `small`: $n \leq 10$
* `medium`: $n \leq 28$
* `big`: $n \leq 40$


