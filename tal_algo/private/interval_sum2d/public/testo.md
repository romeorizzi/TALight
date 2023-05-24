# Query su sotto-intervalli e matrici (interval_sum2d)

Dato un vettore di $n$ numeri interi, come:

```
   vect = [3, 1, 2, 1, 1, 1, 2]
```
dovete rispondere efficientemente a query del tipo:

```
   sum(a, b) = sum(vect[a:b]) 
```

La query ritorna il valore $\sum_{j=a}^{b-1} vect[j]$, assunto che $0<=a < b <= n$.

Più in generale, nel caso di una matrice $M$, di dimensioni $n_1\times n_2$, avremo query del tipo $sum(a_1, b_1, a_2, b_2) = \sum_{i=a_1}^{b_1 -1} \sum_{j=a_2}^{b_2 -1} M[i_1, i_2]$.


## Input
Si legga l'input da `stdin`.
La prima riga contiene $T$, il numero di testcase (istanze) da risolvere. Seguono $T$ istanze del problema.
Ogni istanza si compone del seguente preambolo:
una prima riga fornisce i due numeri interi positivi $n_1$, $n_2$, separati da spazio.
Seguono le $n_1$ righe della matrice (quando $n_1=1$ siamo nel caso del vettore):
l'$i$-esima di tali righe riga riporta, nell'ordine e separati da spazio, gli $n_2$ interi che compongono l'$i$-esima riga della matrice $M$ in input. Dopo queste $n_1$ righe il preambolo viene concluso da un'ultima riga che riporta il numero di query $q$.
Seguono le $q$ query, ognuna posta su una diversa riga e composta dai quattro numeri $a_1$, $b_1$, $a_2$, $b_2$ separati da spazio (nel caso particolare del vettore avremo sempre $a_1 = 1, b_1 = 2$).

## Output
Dopo aver letto l'intero input, scrivi su `stdout` le $q$ righe di risposta al testcase prima di passare a leggere quello successivo. L'$i$-esima di tali righe offre la risposta all'$i$-esima query del testcase.


## Esempio

### Input
```
2
1 7
3 1 2 1 1 1 2
6
0 1 0 1
0 1 0 2
0 1 0 7
0 1 6 7
0 1 2 7
0 1 2 6
5 7
3 1 2 1 1 1 2
1 1 1 1 1 1 1
3 1 2 1 1 1 2
0 0 0 0 0 0 0
3 1 2 1 1 1 2
6
0 1 0 1
0 1 0 7
2 3 2 7
0 5 0 7
1 2 1 2
1 2 1 3
```

Spiegazione: due testcase, il primo dei quali pone $6$ query sul vettore ($n_1=1$) di $n_2=7$ elementi dato all'inizio di questo testo. La prima query chiede il valore del primo elemento, la seconda la somma dei primi due, la terza la somma di tutti gli elementi, la quarta il valore dell'ultimo elemento. Le rimanenti due query chiedono la somma su intervalli più generici.
Nel secondo testcase abbiamo $6$ query su una matrice $5\time 7$. La prima query chiede il valore della cella $M[0][0]$, la seconda query riguarda la sola prima riga e risulta così anch'essa analoga ad una query del testcase precedente. Lo stesso può dirsi per la terza query che riguarda la sola terza riga, anch'essa identica al vettore di cui al testcase precedente di cui ripropone la risposta alla quinta query. La quarta query chiede la somma di tutti gli elementi della matrice. Non commentiamo le rimanenti due query, vedi piuttosto quì sotto cosa ciascuna query debba ritornare.


### Output
```
3
4
11
2
7
5
3
11
7
40
1
2
```

## Assunzioni

Puoi assumere che i numeri contenuti nella matrice/vettore siano sempre interi positivi sufficientemente piccoli da fare si che la somma di tutti loro non ecceda $2^30$.

## Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

Per il subtasking sono previste le seguenti `size`:

* **[ 2 istanze] esempi_testo:** i due esempi del testo
* **[ 5 istanze] array_small**: $n_1 = 1$, $n_2 = 10$, $q = 20$
* **[ 5 istanze] array_medium**: $n_1 = 1$, $n_2 = 100$, $q = 200$
* **[ 5 istanze] mat_small**: $n_1, n_2 = 10$, $q = 20$
* **[10 istanze] mat_medium**: $n_1, n_2 = 30$, $q = 300$
* **[11 istanze] array_big**: $n_1 = 1$, $n_2 = 10\,000$, $q = 3000$
* **[12 istanze] mat_big**: $n_1, n_2 = 100$, $q = 3000$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi  fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

```
    rtal -s wss://ta.di.univr.it/algo  connect -a size=mat_medium  interval_sum -- python my_solution.py
```

vengono valutati, nell'ordine, i subtask:

**esempi_testo**, **array_small**, **array_medium**, **mat_medium**.

Il valore di default per l'argomento **size** è **mat_big** che include tutti i testcase.

