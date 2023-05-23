# Query su sotto-intevalli (interval_sum)

Dovete gestire nel dinamico un vettore di $n$ numeri interi. Inizialmente tutti gli $n$ numeri sono nulli, ad esempio, per $n=7$, si parte con:

```
   vect = [0, 0, 0, 0, 0, 0, 0]
```

nel dinamico dovete servire richieste di due tipologie (query e updates), che si avvicenderanno in sequenze arbitrarie:

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

dove $0<=a < b <= n$ tali query devono ritornare il valore della somma $\sum_{j=a}^{b-1} vect[j]$.

Più in generale, nel caso di una matrice $M$, di dimensioni $n_1\times n_2$, avremo updates del tipo $increase(i, j, delta)$ e query del tipo $sum(a_1, b_1, a_2, b_2) = \sum_{i=a_1}^{b_1 -1} \sum_{j=a_2}^{b_2 -1} M[i_1, i_2]$.


## Input
Si legga l'input da `stdin`.
La prima riga contiene $T$, il numero di testcase (istanze) da risolvere. Seguono $T$ istanze del problema.
Ogni istanza si compone di un preambolo di due sole righe: la prima riga contiene i due numeri interi positivi $n_1$ e $n_2$ separati da spazio, la seconda riga contiene solo $r$, il numero di richieste di primitive di update o query che verranno invocate.
Seguono le $r$ righe con una richiesta ciascuna:
una riga di tre numeri $i$, $j$ e $d$ separati da spazio, codifica una richiesta di update;
una riga con quattro numeri $a_1$, $b_1$, $a_2$ e $b_2$ separati da spazio, codifica una query.

## Output
Si scriva su `stdout`.
Dopo aver letto l'intero input del testcase, devi rispondere a ciascuna delle sue $q <= r$ richieste di tipo query, prima di poter passare alla prossima istanza.
Tali risposti constano di un singolo numero, ciascuno da inviare su una nuova riga di `stdout`. L'$i$-esima di queste $q$ righe inviate su  `stdout` offre la risposta alla $i$-esima richiesta di query del testcase e deve tener conto di tutte le richieste di update che l'hanno preceduta, mentre non può dipendere da quelle che seguiranno.


## Esempio

### Input
```
2
1 7
15
0 1 0 7
0 0 3
0 1 1
0 2 2
0 1 0 7
0 3 1
0 4 1
0 5 1
0 6 2
0 1 0 1
0 1 0 2
0 1 0 7
0 1 6 7
0 1 2 7
0 1 2 6
2 3
13
0 0 3
0 1 1
0 2 2
1 0 1
1 1 1
1 2 1
0 2 0 3
0 2 1 3
0 2 1
0 0 1
0 1 1
0 2 0 3
0 2 1 3
```


### Output
```
0
6
3
4
11
2
7
5
9
5
12
7
```


## Assunzioni

Puoi assumere che i numeri contenuti nella matrice/vettore siano sempre interi positivi sufficientemente piccoli da fare si che la somma di tutti loro non ecceda mai $2^30$.

## Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

Per il subtasking sono previste le seguenti `size`:

* **[ 2 istanze] esempi_testo:** i due esempi del testo
* **[ 8 istanze] array_small**: $n_1 = 1$, $n_2 = 10$, $r = 20$
* **[10 istanze] array_medium**: $n_1 = 1$, $n_2 = 100$, $r = 200$
* **[10 istanze] mat_small**: $n_1, n_2 = 10$, $r = 30$
* **[10 istanze] mat_medium**: $n_1, n_2 = 30$, $r = 300$
* **[30 istanze] array_big**: $n_1 = 1$, $n_2 = 10\,000$, $r = 1000$
* **[30 istanze] mat_big**: $n_1, n_2 = 100$, $r = 1000$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi  fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

```
    rtal -s wss://ta.di.univr.it/algo  connect -a size=mat_medium  interval_sum_dyn -- python my_solution.py
```

vengono valutati, nell'ordine, i subtask:

**esempi_testo**, **array_small**, **array_medium**, **mat_medium**.

Il valore di default per l'argomento **size** è **mat_big** che include tutti i testcase.

