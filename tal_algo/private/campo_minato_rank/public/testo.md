# Campo minato

Ti viene data una griglia di $m$ righe e $n$ colonne le cui celle sono individuate da coppie $(i, j)$ con $0<= i < m$ e $0<= j < n$. Dalla cella $(i,j)$ puoi raggiungere solo le celle $(i+1, j)$ e $(i, j+1)$. Alcune celle sono proibite.
Un percorso è valido se parte dalla cella $(0, 0)$ (quella più in alto a sinistra) e termina nella cella $(m-1,n-1)$ (quella più in basso a destra), muovendosi ad ogni passo dalla cella corrente ad una delle due celle da essa raggiungibili, sempre evitando le celle proibile. Le celle $(0, 0)$ e $(m-1, n-1)$ sono sempre consentite.

Per questo problema è richiesto di calcolare il percoSrso k-esimo valido, dove $k$ è un numero naturale dato in input. Viene garantito che il percorso $k$-esimo esiste sempre.

Un percorso è identificato da una posizione nella lista dei percorsi da 0 a $H$ e formato dalla concatenazione dei caratteri ('S', 'E') che rappresentano il movimento verso il basso ('S') e verso destra ('E').

## Input
L'input avviene da `stdin`.
La prima riga contiene $T$, il numero di testcase da risolvere. Seguono $T$
istanze del problema. Ogni istanza è composta nel seguente modo: nella prima
riga ci sono $m$, $n$ e $k$, tutti separati da uno spazio, relativamente il numero di righe, colonne e il $k$-esimo percorso da trovare (i percorsi vanno da $0..H$, dove $k \in {0..H}$).
Nelle seguenti $m$ righe è disegnata la griglia in ASCII: i cancelletti indicano le celle proibite e i punti quelle consentite (tutte le altre).

## Output
Per ogni testase devi inviare su `stdout` una riga col numero di percorsi validi nella griglia.  ATTENZIONE: siccome questo numero potrebbe essere molto grande, assicurati di impiegare tipi di variabili sufficientemente capienti per evitare errori di overflow!

## Esempio

### Input
```
2
6 5 0
.....
.#...
.....
.#...
....#
.....
5 5 13
....#
.....
.....
#....
.....
```

### Output
```
SSSSSEEEE
SESSEEES
```

## Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

Per il subtasking sono previste le seguenti `size`, dove il default è `big` che include anche i testcase `medium`, `small` e `tiny`:

* `tiny`: $m, n \leq 6$
* `small`: $m, n \leq 10$
* `medium`: $m, n \leq 20$
* `big`: $m, n \leq 30$



