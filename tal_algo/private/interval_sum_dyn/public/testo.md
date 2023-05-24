# Query su sotto-intevalli (interval_sum)

Dovete gestire nel dinamico un vettore di $n$ numeri interi. Inizialmente tutti gli $n$ numeri sono nulli, ad esempio, per $n=7$, si parte con:

```
   vect = [0, 0, 0, 0, 0, 0, 0]
```

nel dinamico dovete servire due tipi di richieste (query e updates), che si avvicenderanno in sequenze arbitrarie:

1. [updates] mantenere aggiornato il vettore a fronte di primitive di aggiornamento del tipo:

```
   increase(i, d) 
```
dove $0<=i < n$ e $d$ è un qualsiasi numero intero. A fronte di questa richiesta di update, l'effetto da produrre vuole essere il seguente:

```
   vect[i] := vect[i] + d 
```

2. rispondere efficientemente a query del tipo:

```
   sum(a, b) = sum(vect[a:b]) 
```

dove $0<=a < b <= n$ una tale query deve ritornare il valore $\sum_{j=a}^{b-1} vect[j]$.


## Input
Si legga l'input da `stdin`.
La prima riga contiene $T$, il numero di testcase (istanze) da risolvere. Seguono $T$ istanze del problema.
Ogni istanza si compone di una prima riga che contiene i due numeri interi positivi $n$ ed $r$ separati da spazio, dove $n$ è la dimensione del vettore (inizialmente tutto nullo) ed $r$ è il numero di richieste di update o query che verranno invocate.
Seguono le $r$ righe con una richiesta ciascuna:
una riga coi tre numeri $0$, $i$, $d$, separati da spazio, codifica e invoca la richiesta di update `increase(i, d)`;
una riga coi tre numeri $1$, $a$, $b$, separati da spazio, codifica e invoca la query `sum(a, b)`.

## Output
Per ciascun testcase, dopo aver letto l'intero input, devi rispondere a ciascuna delle sue $q <= r$ richieste di tipo query, prima di passare a leggere il testcase successivo.
La risposta a ciascuna query consta di un singolo numero da inviare su una nuova riga di `stdout`. L'$i$-esima di queste $q$ righe inviate su  `stdout` offre la risposta alla $i$-esima richiesta di query del testcase e deve tener conto di tutte le richieste di update che l'hanno preceduta, mentre non può dipendere da quelle che seguiranno.


## Esempio

### Input
```
2
7 14
1 0 7
0 0 3
0 1 1
0 2 2
0 3 1
0 4 1
0 5 1
0 6 2
1 0 2
1 0 3
1 0 4
1 0 5
1 0 6
1 0 7
7 15
1 0 7
0 0 3
0 1 1
0 2 2
1 0 7
0 3 1
0 4 1
0 5 1
0 6 2
1 0 1
1 0 2
1 0 7
1 6 7
1 2 7
1 2 6
```


### Output
```
0
3
4
6
7
8
9
11
0
6
3
4
11
2
7
5
```


## Assunzioni

Puoi assumere che i numeri contenuti nella matrice/vettore siano sempre interi positivi sufficientemente piccoli da fare si che la somma di tutti loro non ecceda mai $2^30$.

## Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

Per il subtasking sono previste le seguenti `size`:

* **[ 2 istanze] esempi_testo:** i due esempi del testo
* **[ 8 istanze] small**: $n = 10$, $q = 20$
* **[10 istanze] medium**: $n = 1000$, $q = 1000$
* **[30 istanze] big**: $n = 5000$, $q = 1000$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi  fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

```
    rtal -s wss://ta.di.univr.it/algo  connect -a size=medium  interval_sum_dyn -- python my_solution.py
```

vengono valutati, nell'ordine, i subtask:

**esempi_testo**, **small**, **medium**.

Il valore di default per l'argomento **size** è **big** che include tutti i testcase.

