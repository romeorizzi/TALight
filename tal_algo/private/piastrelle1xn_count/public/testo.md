# Piastrellature di un bagno 1xn con piastrelle 1x1 e 1x2: count

Romeo ha deciso di piastrellare il suo bagno. Il bagno di Romeo è una linea di
$1$ per $n$ celle. Romeo ha a disposizione due tipi di piastrelle:

* le piastrelle $1$ per $1$;
* le piastrelle $1$ per $2$;

Per ogni tipo di piastrella Romeo ne ha a disposizione quante vuole. Romeo si
chiede quanti modi ci sono per piastrellare il suo bagno in modo che ogni cella
del bagno sia piastrellata e che le piastrelle non si sovrappongano. Poiché
la risposta potrebbe essere molto grossa, vuole sapere il numero di modi in cui
può piastrellare il bagno in modulo $10^9+7$.

## Input
La prima riga contiene $T$, il numero di testcase da risolvere. Seguono $T$
istanze del problema. Ogni istanza è composta da una singola riga contenente
$n$, il numero di celle del bagno.

## Output
L'output deve contenere una riga per ogni testase, contenente il numero di modi
per piastrellare il bagno di quel testcase in modulo $10^9+7$.

## Esempio

### Input
```
3
5
42
74
```

### Output
```
8
433494437
63197655
```

## Assunzioni

Per il subtasking sono previste le seguenti `size`, dove il default è `huge` che include tutti i testcase:

* `small`: $n < 10$
* `big`: $n < 10^6$
* `huge`: $n < 10^{18}$

Il tempo limite per testcase è di $1$ secondo.

