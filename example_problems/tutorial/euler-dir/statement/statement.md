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

L'output (da immettere a terminale, o su `stdout` del caso giochi un tuo bot) riporta una permutazione degli archi, con ogni arco su una nuova riga.
Se la permutazione esiste e costituisce un certificato verificabile di SI alla Domanda Centrale sopra formulata.
Altrimenti, accetteremo un semplice NO, almeno fino a quando non avrai scoperto la forma del certificato/linguaggio di NO per questo problema.

### Esempio

#### Input

0 2
0 3
1 0
2 1
3 4
4 0

#### Output

0 2
2 1
1 0
0 3
3 4
4 0

```bash
rtal connect -a goal=with_yes_certificates euler-dir eval_euler_dir
```
Quando hai raccolto un metodo che ti consente di rispondere efficacemente a questa domanda considera di darne descrizione in un codice che potrai sottomettere ai nostri servizi affinché ne valutino correttezza ed efficienza su un benchmark più esteso di istanze e ti forniscano dei feedback.

Se invece non hai idea di come partire ti proponiamo dei percorsi che speriamo tu possa trovare formativi e stimolanti.

## Percorso

Cominciamo con una questione più semplice: usa check_is_eulerian e check_is_not_eulerian
```bash
rtal connect -a eulerian=yes euler-dir check_is_eulerian
```
Genera un grafo diretto che ritieni essere euleriano, fornisci in input al servizio il grafo e la tua risposta affermativa, sarà il servizio a veificare se hai indovinato.
```bash
rtal connect -a eulerian=no euler-dir check_is_not_eulerian
```
Genera un grafo diretto che ritieni essere euleriano, fornisci in input al servizio il grafo e la tua risposta negativa, sarà il servizio a veificare se hai indovinato.

Prova a capire come è possibile stabilire se un grafo è euleriano, con 
```bash
rtal connect euler-dir check_is_a_scc
```
potrai proporre tu un grafo diretto e ti verrà risposto quali sono le componenti fortemente connesse.
Quando avrai trovato un criterio semplice per stabilire quali sono le comonenti fortemente connesse, potrai verificarlo col servizio:
```bash
rtal connect -a goal=yes_no euler-dir eval_find_scc
```
che ti mette a disposizione due grafi diretti di cui puoi calcolare le componeti fortemente connesse e fornircele in input insieme al tuo certificato di si o di no.

------------------------------------------------

Se invece non ti aiuta o non ti è piacevole, considera quest'altra sfida:

   sapresti scrivere un bot (il più semplice possibile) che, data in input una sequenza di archi diretti su un insieme di N nodi, riesca a stabilire se questi archi formano dei cicli diretti e senza nodi in comune tra di loro?

   sapresti, dirmi SI o NO all'aggiunta di ogni singolo arco?

Esempio:
```bash
rtal connect euler_dir -a N=10 play_incrementally_just_disjoint_directed_cycles
> 1 4
< n
> 3 2
< n
> 5 6
< n
> 4 5
< n
> 5 1
< n
> 2 3
< y
```
Gioca prima qualche partita a mano, e poi, una volta compreso il protocollo, realizza il tuo bot e fallo giocare in tua vece con 

```bash
rtal connect euler_dir -a N=10 play_incrementally_just_disjoint_directed_cycles -- python my_bot.py
```

Il fatto (che ci insegna la teoria della complessità) è questo:
se sei riuscito a costruire un tale bot, allora conosci non solo le ragioni/il linguaggio del SI, ma anche quelle del NO (ossia quando il grafo non è una collezione di cicli diretti e disgiunti sui nodi puoi segnalare un'osservazione puntuale a supporto, una ragione semplice e chiara di NO).
Se hai individuato questo semplice argomento di NO per un caso particolare, come questo, del problema originale, e questo ha la sua bellezza e semplicità, hai allora delle chances che tale argomento caratterizzante possa generalizzare all'intero problema di tuo interesse.
  








