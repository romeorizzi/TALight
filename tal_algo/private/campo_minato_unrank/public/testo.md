# Campo minato

Ti viene data una griglia di $m$ righe e $n$ colonne le cui celle sono individuate da coppie $(i, j)$ con $0<= i < m$ e $0<= j < n$. Dalla cella $(i,j)$ puoi raggiungere solo le celle $(i+1, j)$ e $(i, j+1)$. Alcune celle sono proibite.
Un percorso è valido se parte dalla cella $(0, 0)$ (quella più in alto a sinistra) e termina nella cella $(m-1,n-1)$ (quella più in basso a destra), muovendosi ad ogni passo dalla cella corrente ad una delle due celle da essa raggiungibili, sempre evitando le celle proibile. Le celle $(0, 0)$ e $(m-1, n-1)$ sono sempre consentite.

Computa quanti sono i percorsi validi.

## Input
L'input avviene da `stdin`.
La prima riga contiene $T$, il numero di testcase da risolvere. Seguono $T$
istanze del problema. Ogni istanza è composta nel seguente modo: nella prima
riga ci sono $m$ ed $n$, il numero di righe e di colonne della griglia, separati da spazio.
Nelle seguenti $m$ righe è disegnata la griglia in ASCII: i cancelletti indicano le celle proibite e i punti quelle consentite (tutte le altre).

## Output
Per ogni testase devi inviare su `stdout` una riga col numero di percorsi validi nella griglia.  ATTENZIONE: siccome questo numero potrebbe essere molto grande, assicurati di impiegare tipi di variabili sufficientemente capienti per evitare errori di overflow!

## Esempio

### Input
```
2
7 11
...........
.#....#.#..
.#....#.#..
...........
.#.#..#....
.#.#..#.##.
...........
14 30
..####################.....###
######################...#####
##############################
##############################
######...##################..#
#######.....###########.....##
#########.................####
##########...............#####
#########...##......##...#####
#########...##......##....####
########.##....###....###.####
########.##....#.#....##...###
#########.......#..........###
##########.................##.
```

### Output
```
172
0
```

## Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

Per il subtasking sono previste le seguenti `size`, dove il default è `big` che include anche i testcase `medium`, `small` e `tiny`:

* `tiny`: $m, n \leq 6$
* `small`: $m, n \leq 10$
* `medium`: $m, n \leq 20$
* `big`: $m, n \leq 30$


