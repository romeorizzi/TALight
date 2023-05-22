# Query su sotto-intervalli (interval_sum)

Dato un vettore di $n$ numeri interi, come:

```
   vect = [3, 1, 2, 1, 1, 1, 2]
```
dovete rispondere efficientemente a query del tipo:

```
   sum(a, b) = sum(vect[a:b])
```
La query ritorna il valore $\sum_{j=a}^{b-1} vect[j]$, assunto che $0<=a < b <= n$.


## Input
Si legga l'input da `stdin`.
La prima riga contiene $T$, il numero di testcase (istanze) da risolvere. Seguono le $T$ istanze del problema, ciascuna così codificata:
una prima riga contiene i numeri $n$ e $q$ separati da spazio.
Seguono $n$ righe di cui l'$i$-esima riporta l'$i$-esimo elemento del vettore.
Seguono le $q$ query, ognuna posta su una diversa riga composta dai due numeri $a$ e $b$ separati da spazio.

## Output
Scrivi su `stdout` le $q$ righe di risposta al testcase prima di passare a leggere quello successivo. L'$i$-esima di tali righe offre la risposta all'$i$-esima query del testcase.


## Esempio

### Input
```
2
7 6
3 1 2 1 1 1 2
0 1
0 2
0 7
6 7
2 7
2 6
7 7
1 1 1 1 1 1 1
0 1
0 2
0 3
0 4
0 5
0 6
0 7
```

Spiegazione: due testcase, il primo dei quali pone $6$ query sul vettore di $n=7$ elementi dato all'inizio di questo testo. La prima query chiede il valore del primo elemento, la seconda la somma dei primi due, la terza la somma di tutti gli elementi, la quarta il valore dell'ultimo elemento. Le rimanenti due query chiedono la somma su intervalli più generici.
Nel secondo testcase abbiamo $7$ query sul vettore di $7$ elementi tutti uguali ad $1$. L'$i$-esima di queste query chiede la somma dei primi $i$ elementi del vettore.


### Output
```
3
4
11
2
7
5
1
2
3
4
5
6
7
```

## Assunzioni

Puoi assumere che i numeri contenuti nel vettore siano sempre interi positivi sufficientemente piccoli da fare si che la somma di tutti loro non ecceda $2^30$.

## Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

Per il subtasking sono previste le seguenti `size`:

* **[ 2 istanze] esempi_testo:** i due esempi del testo
* **[ 8 istanze] small**: $n = 10$, $q = 20$
* **[10 istanze] medium**: $n = 1000$, $q = 1000$
* **[30 istanze] big**: $n = 10\,000$, $q = 10\,000$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi  fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

```
    rtal -s wss://ta.di.univr.it/algo  connect -a size=medium  interval_sum -- python my_solution.py
```

vengono valutati, nell'ordine, i subtask:

**esempi_testo**, **small**, **medium**.

Il valore di default per l'argomento **size** è **big** che include tutti i testcase.

