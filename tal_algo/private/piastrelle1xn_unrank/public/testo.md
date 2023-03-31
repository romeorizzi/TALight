# Piastrellature di un bagno 1xn con piastrelle 1x1 e 1x2: unrank

Voglio piastrellare un bagno largo $1$ e lungo $n$ evitando di sovrapporre le piastrelle ma ricoprendolo perfettamente in ogni punto. Fortunatamente dispongo in quantità illimitata di due tipi di piastrelle:

* le piastrelle $1$ per $1$;
* le piastrelle $1$ per $2$.

Ecco le possibili piastrellature di un bagno 1x3 ordinate secondo il nostro criterio di ordinamento:

```
piastrellatura 0:  [-][-][-]
piastrellatura 1:  [-][----]
piastrellatura 2:  [----][-]
```

E' richiesta la competenza di saper produrre la piastrellatura $i$ dati $n$ e $i$:

```
n=4, i=0  --> unrank -->  [-][-][-][-]
n=4, i=1  --> unrank -->  [-][-][----]
n=4, i=2  --> unrank -->  [-][----][-]
n=4, i=3  --> unrank -->  [----][-][-]
n=4, i=4  --> unrank -->  [----][----]
```


## Input
La prima riga contiene $T$, il numero di testcase da risolvere. Seguono $T$
istanze del problema. Ogni istanza è composta da una singola riga contenente
 i numeri $n$ e $i$ separati da spazio.

## Output 
In ogni testase, l'unica riga dell'output deve contenere la piastrellatura $i$ del bagno di dimensione $n$.

## Esempio

### Input
```
5
3 1
4 0
5 0
5 2
5 7
```

### Output
```
[-][----]
[-][-][-][-]
[-][-][-][-][-]
[-][-][----][-]
[----][----][-]
```


## Assunzioni

Per il subtasking sono previste le seguenti `size`, dove il default è `big` che include tutti i testcase:

* `small`: $n \leq 10$
* `big`: $n \leq 1000$

Il tempo limite per testcase è di $1$ secondo.

