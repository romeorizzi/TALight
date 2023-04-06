# Piastrellature di un bagno 1xn con piastrelle 1x1 e 1x2: count

Romeo ha deciso di piastrellare il suo bagno, che, assai stretto ma lungo, in pratica è una riga di $1$ per $n$ celle. Romeo ha a disposizione due tipi di piastrelle:

* le piastrelle $1$ per $1$;
* le piastrelle $1$ per $2$;

Per ogni tipo di piastrella Romeo ne ha a disposizione quante vuole. Quanti sono i modi diversi per piastrellare il bagno in modo che ogni sua cella sia piastrellata senza che le piastrelle si sovrappongano? Poiché questo numero potrebbe essere molto grande, ci si limiti a calcolarlo modulo $10^9+7$, ossia si ritorni il resto della divisione di tale numero per $1\,000\,000\,007$.

## Input
La prima riga contiene $T$, il numero di testcase da risolvere. Seguono $T$
istanze del problema. Ogni istanza è composta da una singola riga contenente $n$, il numero di celle del bagno.

## Output
L'output deve contenere una riga per ogni testase, contenente il resto della divisione per $1\,000\,000\,007 del numero di modi per piastrellare il bagno di quel testcase (ossia del bagno di dimensioni $1$ per $n$).

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

Per il subtasking sono previste le seguenti `size`, dove il default è `huge` che include anche i testcase `big`, `medium`, `small` e `tiny`:

* `tiny`: $n \leq 4$
* `small`: $n \leq 9$
* `medium`: $n \leq 25$
* `big`: $n \leq 10^6$
* `huge`: $n \leq 10^{18}$

Il tempo limite per testcase è di $1$ secondo.

