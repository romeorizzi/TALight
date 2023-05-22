# Campo minato via

Ti viene data una griglia di $m$ righe e $n$ colonne le cui celle sono individuate da coppie $(i, j)$ con $0<= i < m$ e $0<= j < n$. Dalla cella $(i,j)$ puoi raggiungere solo le celle $(i+1, j)$ e $(i, j+1)$. Alcune celle sono proibite.
Un percorso è valido se parte dalla cella $(0, 0)$ (quella più in alto a sinistra) e termina nella cella $(m-1,n-1)$ (quella più in basso a destra), muovendosi ad ogni passo dalla cella corrente ad una delle due celle da essa raggiungibili, sempre evitando le celle proibile. Le celle $(0, 0)$ e $(m-1, n-1)$ sono sempre consentite.

In questa variante viene fornito in input anche un cella $(i', j')$ attraverso cui i percorsi devono passare. Computare il numero dei possibili percorsi validi che passano per la cella $(i', j')$.

## Input
L'input avviene da `stdin`.
La prima riga contiene $T$, il numero di testcase da risolvere. Seguono $T$ istanze del problema. Ogni istanza è composta nel seguente modo: nella prima riga ci sono $m$, $n$ ed $s$, il numero di righe e di colonne della griglia, separati da spazio. Segue una nuova riga con $i'$ e $j'$ separati da uno spazio che indicano le coordinate della cella su cui passare. Nelle seguenti $m$ righe è disegnata la griglia in ASCII: i cancelletti indicano le celle proibite e i punti quelle consentite (tutte le altre).

## Output
Per ogni testase devi inviare su `stdout` una riga col numero di percorsi validi nella griglia.  ATTENZIONE: siccome questo numero potrebbe essere molto grande, assicurati di impiegare tipi di variabili sufficientemente capienti per evitare errori di overflow!

# m righe di n numeri interi separati da spazio

## Esempio

### Input
```
2
8 11
1 0
.##########
...........
.#....#.#..
.#....#.#..
...........
.#.#..#....
.#.#..#.##.
...........
4 11
2 1
.##########
.##########
..#########
...........
```

### Output
```
172
2
```

## Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

Per il subtasking sono previste le seguenti `size`, dove il default è `big` che include anche i testcase `medium`, `small` e `tiny`:

* `tiny`: $m, n \leq 6$
* `small`: $m, n \leq 10$
* `medium`: $m, n \leq 20$
* `big`: $m, n \leq 30$


