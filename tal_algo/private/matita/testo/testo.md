# Disegna senza sollevare la matita (Oii 2012, selezioni nazionali)

Sai risolvere il classico puzzle di disegnare una casetta (con una X
nel suo riquadro centrale) senza mai sollevare la
matita dal foglio?
<p align = "center">
<img src="./casetta.png" width="8%"></img>
</p>
<p align = "center">
Fig.1 - Disegna questa casetta senza mai sollevare la
matita dal foglio.
</p>

In generale, sono dati $N$ vertici, numerati da $1$ a
$N$, e $M$ lati che li collegano. Sapresti indicare in quale sequenza attraversare i lati, e per ciascuno di essi in quale direzione, in modo che il vertice cui ci conduce ciascun lato coincida col vertice da cui ci preleva il lato successivo (senza alzare quindi la matita)? La sfida è di riuscire ad attraversare ciascun lato una ed una volta sola.
Ti è possibile riuscire a farlo tornando infine al vertice di partenza?

## Input
Si legga l'input da `stdin`.
La prima riga contiene $T$, il numero di testcase (istanze) da risolvere. Seguono $T$
istanze del problema. Per ogni istanza, la prima riga contiene quattro numeri interi $N$,
$M$, $A$ e $B$ separati da uno spazio:
il numero di vertici, il numero di lati che si richiede di attraversare (ogni lato una ed una volta sola, dovrai decidere tu in quale direzione), il vertice di
partenza, e quello di arrivo.
Le successive $M$ righe offrono, uno per riga, gli $M$ lati del puzzle, ciascun rappresentato da una
coppia non-ordinata di interi nell'intervallo $[1,N]$, separati da uno spazio (questi interi sono i nomi dei vertici collegati dal lato in questione). Per ciascun lato "$X$ $Y$" dovrai scegliere se attraversarlo da $X$ ad $Y$ oppure da $Y$ ad $X$, oltre che stabilire in quale ordine vadano attraversati i lati.


## Output
Per ciascuna istanza, prima di poter leggere l'istanza successiva, occorre trasmettere su `stdout` l'output che sarà così strutturato:
per ogni riga dell'input intesa a rappresentare un lato del puzzle (ossia nel formato "$X$ $Y$"), l'output dovrà contenere una riga "$X$ $Y$" se il lato viene percorso da $X$ a $Y$, oppure una riga "$Y$ $X$" se il lato viene percorso da $Y$ a $X$.
Le righe in output saranno pertanto $M$, ma riordinate rispetto alle $M$ rispettive righe dell'input in modo da specificare inoltre in quale ordine gli $M$ lati dell'input vengano attraversati: per la prima di queste righe deve valere la condizione che $X = A$. Il vertice $X$ di ciascun altra riga deve coincidere col vertice $Y$ della riga precedente (non devi staccare mai la matita dal foglio), e per l'ultima riga deve valere anche che $Y=B$.

## Esempio

### Input
```
1
5 8 1 5
1 4
2 3
5 4
2 1
2 4
3 4
1 5
5 2

```

### Output
```
1 2
2 3
3 4
4 5
5 2
2 4
4 1
1 5
```

## Note

1. Viene garantito che sia sempre possibile disegnare senza alzare la matita. Nel caso vi siano più soluzioni valide, è sufficiente restituirne una qualsiasi.

2. Nessun testcase presenta lati multipli che collegano la stessa coppia di vertici (se un lato di un'istanza è descritto dalla stringa "$X$ $Y$", nella stessa istanza non potrai ritrovare la stessa stringa e nemmeno la stringa "$Y$ $X$"). Inoltre non forniremo mai lati della forma "$X$ $X$". Tutti i vertici e tutti i lati devono essere attraversati dalla matita.

3. Per chi non lo avesse riconosciuto, questo è il noto problema affrontato dal matematico Eulero in un lavoro (1735) considerato l'atto di nascita della teoria dei grafi e della topologia.


## Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

I testcase sono raggruppati nei seguenti subtask.

* **[1 istanza] esempi_testo:** l'esempio del testo (disegna la casetta)
* **[8 istanze] smallest:** $N = 2, 3, 4$ ($M \leq 6$) 
* **[10 istanze] small:** $N = 5, 6$ ($M \leq 12$)
* **[30 istanze] medium:** $N \leq 100$, $M \leq 500$
* **[21 istanze] big:** $N \leq 1\,000$, $M \leq 5\,000$
* **[30 istanze] huge:** $N \leq 10\,000$, $M \leq 50\,000$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi  fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

```
    rtal -s wss://ta.di.univr.it/algo  connect -a size=medium  matita -- python my_solution.py
```

vengono valutati, nell'ordine, i subtask:

**esempi_testo**, **smallest**, **small**, **medium**.

Il valore di default per l'argomento **size** è **huge** che include tutti i testcase.



