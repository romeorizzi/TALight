# Una griglia bianconera

Ti viene data una griglia di $m$ righe e $n$ colonne con celle colorate di
bianco o di nero. Definiamo un percorso valido come un percorso che parte
nella cella $(0, 0)$ (quella più in alto a sinistra), termina nella cella
$(n-1,m-1)$ (quella più in basso a destra)$, passa solo da celle bianche e
si sposta solo in celle in basso o a destra.

Computa quanti sono i percorsi validi. ATTENZIONE: questo numero potrebbe essere molto grande, assicurati di impiegare tipi di variabili sufficientemente capienti per evitare errori di overflow!

## Input
La prima riga contiene $T$, il numero di testcase da risolvere. Seguono $T$
istanze del problema. Ogni istanza è composta nel seguente modo: nella prima
riga ci sono $m$ ed $n$, il numero di righe e di colonne della griglia.
Successivamente è disegnata la griglia in ASCII dove i punti sono le celle
bianche e i cancelletti sono le celle nere.

## Output
L'output deve contenere una riga per ogni testase, contenente il numero di
percorsi validi nella griglia. Siccome questo numero potrebbe essere molto grande, assicurati di impiegare tipi di variabili sufficientemente capienti per evitare errori di overflow!

\pagebreak
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

## Assunzioni

La cella di partenza e quella di arrivo sono sempre bianche (transitabili).

Per il subtasking sono previste le seguenti `size`, dove il default è `big` che include anche i testcase `medium`, `small` e `tiny`:

* `tiny`: $n \leq 6$
* `small`: $n \leq 10$
* `medium`: $n \leq 20$
* `big`: $n \leq 30$

Il tempo limite per testcase è di $1$ secondo.

