# Circuito Euleriano su grafi diretti (euler_dir)

## Descrizione del problema che abbiamo a riferimento e la cui soluzione anche efficiente poniamo come obittivo

Un grafo è diretto quando tutti i suoi archi sono orientati, ossia hanno una coda e una testa e possono essere percorsi solo dalla coda alla testa (come fossero strade a senso unico). 
Consideriamo la versione per grafi diretti del [problema dei ponti risolto da Eulero nel 1736](https://en.wikipedia.org/wiki/Seven_Bridges_of_K%C3%B6nigsberg). Si consideri ad esempio il grafo:

![image](figs/euler-dir.png)

Esso ammette il seguente circuito Euleriano:

$(0,3), (3,4), (4,0), (0,2), (2,1), (1,0)$

Un circuito Euleriano di un grafo è una permutazione dei suoi archi tale che per ogni arco $(a,b)$, cui nella permutazione segue un arco $(c,d)$, valga che $c = b$.

  <strong>Domanda Centrale:</strong> Dato un grafo diretto, stabilire se esso ammette un circuito Euleriano. 

Un grafo si dice Euleriano quando ammette un circuito Euleriano, ossia quando posso ordinarne gli archi in modo che il grafo sia esso stesso un circuito Euleriano.

Quando hai raccolto un metodo che ti consente di rispondere efficacemente a questa domanda considera di darne descrizione in un codice che potrai sottomettere al nostro servizio affinché ne valuti correttezza ed efficienza su un benchmark più esteso di istanze e ti forniscano dei feedback.

```bash
rtal connect -a goal1=with_yes_certificates euler-dir eval_euler_dir
```
Puoi prefissarti come obiettivo aggiuntivo di comporre un algoritmo efficiente, che puoi controllare con il servizio:

```bash
rtal connect -a goal1=with_yes_certificates -a goal2=efficient euler-dir eval_euler_dir
```

Se invece non hai idea di come partire ti proponiamo un percorso che speriamo tu possa trovare formativo e stimolante.


### Codifica di un circuito Euleriano

Assumiamo il grafo abbia $N$ vertici e $M$ archi diretti. Assumiamo che gli $N$ vertici siano numerati da $0$ a $N-1$.
La codifica avviene su $M+1$ righe (di un file o stream da terminale o da `stdin`). 
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

### Codifica di un circuito Euleriano
Nella prima riga scriviamo il numero di nodi $N$ ed il numero di archi $M$.
Nelle successive $M$ righe vengono disposti gli $M$ archi secondo l'ordine prescritto dal circuito Euleriano.
Ognuna di queste $M$ righe contiene due interi separati da spazio: il primo è la coda ed il secondo la testa dell'arco in questione.

#### Esempio

Ad esempio, un programma pensato per stabilire se un grafo passatogli in input ammetta un ciclo Euleriano, una volta ricevuto in input il grafo di vui sopra restituirebbe:

```bash
Y
5 6
0 2
2 1
1 0
0 3
3 4
4 0
```

Dove il carattere 'Y' che compone la prima riga stà ad indicare che un circuito Euleriano esiste. Dove esso non esista la risposta sarà di una sola riga costituita dal carattere 'N'. In caso di risposta affermativa alla prima riga potranno invece seguire le $M$ righe col circuito Euleriano,

## Percorso

Se ti servono degli spunti su come partire ad affrontare il problema, ti proponiamo quì un percorso che speriamo tu possa trovare formativo e stimolante. Inoltre, sempre quì, ti proponiamo dei servizi che possano agevolare o strutturare le tue investigazioni.

Il seguente servizio è pensato per agevolarle: puoi sottoporgli un grafo di tua fantasia e che credi sia Euleriano. Il servizio controllerà per te che in effetti lo sia. Inoltre, a richiesta (gli argomenti di un servizio possono essere investigati col comando `rtal list` o anche col servizio `synopsis` del problema), il servizio produrrà inoltre un ordinamento corretto degli archi. 

```bash
rtal connect -a eulerian=yes euler-dir check_is_eulerian
```

Esiste anche un servizio duale se vuoi conferma sul fatto che un grafo da te proposto non sia Euleriano.

```bash
rtal connect -a eulerian=no euler-dir check_is_not_eulerian
```

In nocciolo della questione risiede nel capire quando un grafo sia Euleriano. Per preparare il terreno protresti raccogliere prima ulteriori comprensioni, ad esempio partendo da un altro quesito, più semplice, che ti proponiamo:

   <strong>Competenza ausiliaria:</strong> Saresti in grado di individuare quali sono le componenti fortemente connesse di un grafo? 

Nel tutorial è presente un problema con cui potrai impadroniti del concetto di componenti fortemente connesse e scoprirne i principali risvolti algoritmici.



Individuate le componenti fortemente connesse, saresti in grado quindi di affermare se il grafo contiene un circuito euleriano?
Gioca utilizzando il seguente servizio che ti proporrà dei grafi diretti elencandone gli archi (per selezionare il grafo con cui vuoi giocare scrivi nel comando al posto di X un numero tra 1 e 7), sarà tuo compito calcolarne le componenti fortemente connesse:

```bash
rtal connect -a graph=X euler-dir eval_find_scc
```

In alternativa per cominciare con qualcosa di più semplice, potrai proporre tu un grafo e ti verrà risposto quali sono le componenti fortemente connesse usando il seguente servizio:

```bash
rtal connect euler-dir gimme_scc
```

------------------------------------------------

Il fatto (che ci insegna la teoria della complessità) è questo:
se sei riuscito a completare il percorso, allora dovresti avrere un'idea di quali solo le ragioni/il linguaggio del SI, ma anche quelle del NO per il problema euler-dir.


