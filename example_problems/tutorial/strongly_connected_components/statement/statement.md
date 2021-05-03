# Grafo diretto fortemente connesso (strongly_connected_components)

## Descrizione del problema e risvolti algoritmici

Data la definizione di Grafo Diretto: un grafo i cui archi sono orientati, ossia hanno una coda e una testa e possono essere percorsi solo dalla coda alla testa (come fossero strade a senso unico). 
Come in figura:

![image](figs/euler-dir.png)

Possiamo dare la definizione di Grafo Diretto Fortemente Connesso, ossia un grafo con una e una sola Componente Fortemente Connessa.
Prendendo come esempio la figura, nel grafo c'è una sola componente fortemente connessa, così formata:
$01243$
Pertanto è un Grafo Diretto Fortemente connesso.

  <strong>Domanda Centrale:</strong> Dato un grafo diretto G, possiamo stabilire se è fortemente connesso?

Quando hai raccolto un metodo che ti consente di rispondere efficacemente a questa domanda considera di darne descrizione in un codice che potrai sottomettere ai nostri servizi affinché ne valutino correttezza su un benchmark più esteso di istanze e ti forniscano dei feedback.

```bash
rtal connect strongly_connected_components eval_gsc
```

### Codifica di un grafo diretto G

Assumiamo che il grafo abbia $N$ vertici e $M$ archi diretti. Assumiamo che gli $N$ vertici siano numerati da $0$ a $N-1$.
La codifica avviene su $M+1$ righe (di uno stream da terminale o da `stdin`). 
La prima riga contiene i due interi $N$ e $M$, in questo ordine e separati da uno spazio.
Le successive $M$ righe contengono ciascuna un diverso arco, rappresentato da una coppia di interi separati da uno spazio: il primo indica il nodo di coda ed il secondo il nodo di testa. Non facciamo alcuna assunzione su quale sia l'ordine di queste $M$ righe.

#### Esempio

```bash
5 6
0 2
0 3
1 0
2 1
3 4
4 0
```

### Codifica di un output
La codifica dell'output avviene su tante righe quante sono le componenti fortemente connesse individuate nel grafo.
Le componenti fortemente connesse e i nodi che le compongono vengono stampate nell'ordine in cui il servizio le calcola, non sempre sono in ordine crescente.

#### Esempio

```bash
01234
```

Se ti servono degli spunti su come partire ad affrontare il problema, ti proponiamo quì un percorso che speriamo tu possa trovare formativo e stimolante. 

## Percorso

In questo percorso ti proponiamo dei servizi che possano agevolare o strutturare le tue investigazioni.

Il seguente servizio è pensato per agevolarle: puoi sottoporgli un grafo di tua fantasia e che credi sia fortemente connesso. Il servizio controllerà per te che in effetti lo sia e su richiesta potrà fornire il cerificato.

```bash
rtal connect strongly_connected_components check_is_gsc
```
Il cui servizio duale è pensato per sottoporgli un grafo che credi non sia fortemente connesso. Il servizio controllerà per te che in effetti non lo sia e su richiesta potrà fornire il certificato.

```bash
rtal connect strongly_connected_components check_is_not_gsc
```

Vediamo la definizione di Componente Fortemente Connessa, in un grafo diretto G è un sottografo massimale di G in cui esiste un cammino orientato tra ogni coppia di nodi ad esso appartenenti.

In nocciolo della questione risiede nel capire quante componenti fortemente connesse ci sono un grafo diretto G. Per preparare il terreno protresti raccogliere prima ulteriori comprensioni, ad esempio partendo da un altro quesito, più semplice, che ti proponiamo:

   <strong>Competenza ausiliaria:</strong> Saresti in grado di individuare quali sono le componenti fortemente connesse di un grafo? 

Gioca con il seguente servizio a cui potrai proporre tu un grafo, nel formato di input definito sopra, e ti verrà risposto quali sono le componenti fortemente connesse.
La codifica dell'output avviene su tante righe quante sono le componenti fortemente connesse individuate nel grafo.
Le componenti fortemente connesse e i nodi che le compongono vengono stampate nell'ordine in cui il servizio le calcola, non sempre sono in ordine crescente.

```bash
rtal connect strongly_connected_components gimme_scc
```

 Qui invece sarà il servizio a proporti dei grafi diretti elencandone gli archi (per selezionare il grafo con cui vuoi giocare scrivi nel comando al posto di X un numero tra 1 e 7), sarà tuo compito calcolarne le componenti fortemente connesse. 
 Fornisci in input le componenti che hai calcolato tutte su una riga e separate da uno spazio, come segue:
```bash
0123 45 6
```
Il servizio:
```bash
rtal connect -a graph=X strongly_connected_components eval_find_scc
```


------------------------------------------------

Il fatto (che ci insegna la teoria della complessità) è questo:
se sei riuscito a completare il percorso, allora dovresti avrere un'idea di quali solo le componenti fortemente connesse di un grafo diretto G, quindi stabilire se G è fortemente connesso.


