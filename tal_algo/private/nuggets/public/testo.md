# Troppi Chicken McNuggets

Dario è un appassionato di Chicken McNuggets, e da buon intenditore conosce le
dimensioni delle scatole disponibili nei vari paesi del mondo. Ad esempio, in
Italia le scatole disponibili sono da $4$, $6$, $9$ e $20$. Dario deve decidere
quanti Chicken McNuggets ordinare, tuttavia si rende conto che non è sempre
possibile ordinarne il numero che si vuole: in Italia, non importa che
combinazione di scatole e quante se ne prendono, non si possono ordinare $7$
Chicken McNuggets.

Dario si chiede quale sia quindi il numero massimo di Chicken McNuggets che non
è possibile ordinare dato un insieme $S$ di $n$ dimensioni di scatole
disponibili. Aiuta Dario a trovare la risposta!

## Assunzioni

Sono presenti le seguenti `size`, dove il default è `big`:

* `small`: $n \leq 5$, $\max(S) \leq 50$
* `big`: $n \leq 250$, $\max(S) \leq 1000$

Il tempo limite per testcase è di $1$ secondo.

## Input
La prima riga contiene $T$, il numero di testcase da risolvere. Seguono $T$
istanze del problema. Ogni istanza è composta nel seguente modo: nella prima
riga c'è $n$, il numero di possibili scatole, e nella seconda riga c'è
l'insieme $S$, separato da spazi.

## Output
L'output deve contenere una riga per ogni testase, contenente il numero massimo
di Chicken McNuggets non ordinabili. È garantito essere un numero finito.

## Esempio

### Input
```
2
4
4 6 9 20
2
41 43
```

### Output
```
11
1679
```