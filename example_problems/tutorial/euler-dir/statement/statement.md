# Circuito Euleriano su grafi diretti (euler_dir)

## Descrizione del problema che abbiamo a riferimento e la cui soluzione anche efficiente poniamo come obittivo
   
Consideriamo la versione per grafi diretti del [problema dei ponti risolto da Eulero nel 1736](https://en.wikipedia.org/wiki/Seven_Bridges_of_K%C3%B6nigsberg).

Qui ci interessa il caso di grafi diretti (le strade/i ponti sono a senso unico):

![image](figs/euler-dir.png)

Sono dati $N$ vertici, numerati da $0$ a $N-1$, e $M$ archi diretti, che collegano i nodi in modo ordinato.

  <strong>Domanda Centrale:</strong> Ti è possibile ritornare una permutazione degli archi tale che per ogni arco $(a,b)$, cui nella permutazione segue un arco $(c,d)$, valga che $c = b$? 
Ti ricordo che, nel nostro gioco, questa è anche la definizione di grafo diretto. Un grafo è diretto quando gli archi sono percorribili solo nel verso della freccia, pertanto se imponiamo che nella permutazione c'è un arco $(a,b)$ seguito da un arco $(c,d)$ con $c = b$, il verso delle frecce è da $a a $b = c$ a $d.


### Dati di input
  
L'input (da terminale o da `stdin` se lo rivolgi ad un tuo bot)è formato da $M+1$ righe. 
La prima riga contiene due interi $N$ e $M$, separati da uno spazio: il numero di vertici e il numero di archi diretti.
Le successive $M$ righe contengono ciascuna un arco, rappresentato da una coppia di interi separati da uno spazio: il primo indica il nodo di coda ed il secondo il nodo di testa.

### Dati di output

L'output (da immettere a terminale, o su `stdout` del caso giochi un tuo bot) riporta innanzitutto se il grafo è euleriano o meno, in caso affermativo viene stampata anche una permutazione degli archi rappresenti un circuito euleriano, con ogni arco su una nuova riga.

### Esempio

#### Input

```bash
5 6
0 2
0 3
1 0
2 1
3 4
4 0
```

#### Output

```bash
Y
0 2
2 1
1 0
0 3
3 4
4 0
```

Quando hai raccolto un metodo che ti consente di rispondere efficacemente a questa domanda considera di darne descrizione in un codice che potrai sottomettere al nostro servizio affinché ne valuti correttezza ed efficienza su un benchmark più esteso di istanze e ti forniscano dei feedback.

```bash
rtal connect euler_dir -a goal=with_yes_certificates eval_euler_dir
```

Se invece non hai idea di come partire ti proponiamo un percorso che speriamo tu possa trovare formativo e stimolante.

## Percorso

Cominciamo con una questione più semplice e cerchiamo di capire insieme quando un grafo è euleriano.
Puoi usare il seguente servizio per fornirci un grafo di tua fantasia credi sia euleriano. Il servizio cotrollerà per te la veridicità della tua assunzione.
(Esiste anche un servizio duale se vuoi verificare il grafo da te proposto non è euleriano).

```bash
rtal connect -a eulerian=yes euler-dir check_is_eulerian
```

```bash
rtal connect -a eulerian=no euler-dir check_is_not_eulerian
```

Se invece sei in difficoltà nel capire come stabilire se un grafo è euleriano, ti proponiamo di studiare il problema partendo da un altro quesito.
Saresti in grado di individuare quali sono le componenti fortemente connese di un grafo? 
Individuate le componenti fortemente connesse, saresti in grado quindi di affermare se il grafo contiene un circuito euleriano?
Gioca utilizzando il seguente servizio che ti proporrà dei grafi diretti elencandone gli archi, sarà tuo compito calcolarne le componenti fortemente connesse:

```bash
rtal connect -a goal=yes_no euler-dir eval_find_scc
```

In alternativa per cominciare con qualcosa di più semplice, potrai proporre tu un grafo e ti verrà risposto quali sono le componenti fortemente connesse usando il seguente servizio:

```bash
rtal connect euler-dir gimme_scc
```

------------------------------------------------

Il fatto (che ci insegna la teoria della complessità) è questo:
se sei riuscito a completare il percorso, allora dovresti avrere un'idea di quali solo le ragioni/il linguaggio del SI, ma anche quelle del NO per il problema euler-dir.


