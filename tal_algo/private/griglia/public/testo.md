# Una griglia bianconera

Ti viene data una griglia di $n$ righe e $m$ colonne con celle colorate di
bianco o di nero. Definiamo un percorso valido come un percorso che parte
nella cella $(0, 0)$ (quella più in alto a sinistra), termina nella cella
$(n-1,m-1)$ (quella più in basso a destra)$, passa solo da celle bianche e
si sposta solo in celle in basso o a destra.

Conta quanti percorsi validi sono presenti nella griglia in modulo $10^9+7$.

## Assunzioni

Sono presenti le seguenti `size`, dove il default è `big`:

* `small`: $n, m \leq 10$
* `big`: $n, m \leq 250$

Il tempo limite per testcase è di $2$ secondi.

## Input
La prima riga contiene $T$, il numero di testcase da risolvere. Seguono $T$
istanze del problema. Ogni istanza è composta nel seguente modo: nella prima
riga ci sono $n$ ed $m$, il numero di righe e di colonne della griglia.
Successivamente è disegnata la griglia in ASCII dove i punti sono le celle
bianche e i cancelletti sono le celle nere.

## Output
L'output deve contenere una riga per ogni testase, contenente il numero di
percorsi validi nella griglia modulo $10^9+7$.

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
##########.................###
```

### Output
```
172
0
```