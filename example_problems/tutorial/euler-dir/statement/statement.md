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
Puoi prefissarti come obiettivo aggiuntivo di comporre un algoritmo efficiente, che puoi controllare chiamando:

```bash
rtal connect -a goal1=with_yes_certificates -a goal2=efficient euler-dir eval_euler_dir
```

Se invece non hai idea di come partire ti proponiamo un percorso che speriamo tu possa trovare formativo e stimolante.


### Codifica di un grafo

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

Ad esempio, un programma pensato per stabilire se un grafo passatogli in input ammetta un ciclo Euleriano, una volta ricevuto in input il grafo di cui sopra, restituisce il carattere 'Y' (invece che il carattere 'N') per indicare che il grafo è Euleriano. A questa prima riga, se il programma si prefigge di restituire anche i certificati per le risposte affermative, seguirebbe la codifica di un circuito Euleriano, che in questo caso potrebbe essere:

```bash
5 6
0 2
2 1
1 0
0 3
3 4
4 0
```


## Percorso

Se ti servono degli spunti su come partire ad affrontare il problema, ti proponiamo qui un percorso che speriamo tu possa trovare formativo e stimolante. Ti esibiremo inoltre dei servizi che possono agevolare o strutturare le tue investigazioni.

Il seguente servizio è pensato per solo stimolarle:

nella cartella `small_examples` trovi diverse piccole istanze per le quali potrai provare a rispondere autonomamente alle domande di pertinenza.
Solo confidiamo che il proporti noi delle piccole istanze significative non ti esima dal comporne tu stesso per condurre linee di esplorazione tue. 

Il seguente servizio può venirti a supporto: puoi sottoporgli un grafo di tua fantasia e che credi sia Euleriano. Il servizio controllerà per te che in effetti lo sia. Inoltre, a richiesta (gli argomenti di un servizio possono essere investigati col comando `rtal list` o anche col servizio `synopsis` del problema), il servizio produrrà inoltre un ordinamento corretto degli archi che conferme e certifica in modo trasparente la risposta affermativa. 

```bash
rtal connect euler-dir check_is_eulerian
```

Esiste anche un servizio duale se vuoi conferma sul fatto che un grafo da te proposto non sia Euleriano.

```bash
rtal connect euler-dir check_is_not_eulerian
```

In nocciolo della questione risiede quindi nel capire quando un grafo sia Euleriano. In questo, senza infingimenti: lavorare su esempi ha un valore insostituibile.
In aggiunta, per preparare il terreno potresti raccogliere prima ulteriori comprensioni, ad esempio partendo da un altro quesito, più semplice, che ti proponiamo:

   <strong>Competenza ausiliaria:</strong> Saresti in grado di individuare quali sono le componenti fortemente connesse di un grafo? 

Un grafo diretto si dice fortemente connesso quando, comunque scelti due nodi $u$ e $v$, in esso sia presente un cammino che consenta di portarsi da $u$ a $v$ senza violare i sensi unici. Nel tutorial è presente un problema (`strongly_connected_components`) con cui potrai impadronirti a fondo del concetto di componenti fortemente connesse e scoprirne i principali risvolti algoritmici.  

Se non sai da dove partire, ti suggeriamo di stabilire, per ciascuno dei grafi nella cartella `examples2` se esso sia:

1. fortemente connesso

2. Euleriano

Se vuoi controllare la tua etichettatura o ti serve aiuto, puoi avvalerti dei servizi di questo problema o del problema `strongly_connected_components`.

E' probabile che a valle di questo percorso tu possa avere acquisito chiarezza su quale possa essere il legame tra le proprità di connessione forte e di Eulerianità (ti sarà più facile se ti soffermerai ad analizzare gli esempi non fortemente connessi). In tal caso, avrai forse ottenuto delle prime _condizioni necessarie_ che devono essere rispettate affinché un grafo possa essere Euleriano.

Ossia ad un'affermazione del tipo:

Lemma: nessun grafo "così o cosà" può essere Euleriano

e della cui validità si possa essere certi.

Se sei in questa condizione, ecco un barbatrucco generale per ottenere una _buona congettura_:

Buona Congettura: tutti i grafi sono Euleriani tranne quelli "così o cosà".

Una congettura è uno strumento di lavoro che appunto serve per aprire un problema. Pertanto, il valore di una congettura non sta tanto nel fatto che essa sia vera oppure falsa, ma piuttosto nella qualità delle sue implicazioni ove fosse vera. Una congettura si dice buona quando il coltello è affilato, ma, se conosci le classi P, NP, co-NP, possiamo allora darti un criterio formale per riconoscere importanti classi di buone congetture, particolarmente affilate e con proprietà notevoli (quale essere win-win o autoavverranti).

Diciamo che il problema di riconoscere se un grafo è Euleriano è in NP in quanto, tutte le volta che la risposta è affermativa, allora è possibile esibire un certificato (il circuito Euleriano) che chiaramente può essere verificato in tempo polinomiale.
Il problema è pertanto nato in NP di suo, ma, condizione necessaria per poterlo portare in P (ossia per scoprire un algoritmo polinomiale per la sua soluzione, che è quanto richiesto dal presente problema `euler-dir`) è che esso sia anche in co-NP:
il problema è in co_NP quando, in modo complementare, tutte le volta che la risposta è negativa, allora esiste un analogo certificato (sempre una qualche stringa che potrebbe anche essere difficile andare a scoprire autonomamente) che possa chiaramente comprovare in NO e che possa essere verificato in tempo polinomiale.

Diciamo che una congettura è buona quando, ove fosse vera, ne conseguirebbe che il problema appartenga ad una classe di complessità (quale NP o co-NP) in cui ancora ci era ignoto rientrasse.
Riesci a vedere perché la congettura di cui sopra sia allora buona, alla luce di questa definizione, ed assumendo che la condizione "così o colà" del Lemma possa essere verificata in tempo polinomiale?

## Servizi per acclimatarsi col concetto di buona congettura

Vogliamo dimostrare che il problema nasce in NP. Il certificato di SI è un circuito Euleriano che potremmo esibire ogniqualvolta esso esista.
Scrivi un algoritmo A che riceva in input un grafo ed una proposta di certificato di SI, e verifichi il certificato.
Se vuoi esplorare le possibili ragioni di bocciatura di un certificato utilizza il nostro servizio

```bash
rtal connect -a feedback=full euler-dir check_YES_certificate
```
che in pratica implementa una nostra versione di A e che potrebbe ispirarti. Ti consigliamo di lanciarlo su tutte le istanze nella cartella examples_YES_certificates per esplorare tutti i modi in cui la verifica può fallire, oppure lancialo su istanze tue. 

Quando avrai poi realizzato tu stesso A, potrai valutarne correttezza ed efficienza col servizio:

```bash
rtal connect -a euler-dir eval_YES_certificate -- myA.py
```

## Ma la buona congettura potrebbe anche essere falsa

Una volta formulata una buona congettura lo sport è quello di andare a capire se possa essere vera oppure falsa.
La caccia può concludersi in due modi, cui corrispondono modi diversi per andare a reclamare la taglia:

A. un controesempio è il modo per dire che la congettura è falsa.

B. una dimostrazione è il modo per dire che la congettura è vera.

Se esce B non vi è alcun dubbio vi sia ragione di festeggiare: dato che si trattava di una buona congettura essa aveva valore potenziale per definizione. Ora sappiamo qualcosa di più su dove il problema si collochi dal punto di vista della sua complessità computazionale.

Se esce A possiamo comunque reputarci soddisfatti: ora del problema conosciamo qualcosa di più, e questo qualcosa si colloca comunque sul piano della struttura del problema in quanto se il controesempio non fosse esistito allora la struttura del problema si sarebbe manifestata benigna. Il controesempio è quindi un messaggero fecondo.

Per questo una buona congettura ci colloca in una situazione win-win. Ottimo affare, non è vero?
Anche ove falsa, una buona congettura è di per sé stessa un passo avanti nel dialogo col problema.

Possibili domande:

Ma come trovare un controesempio? Per ora questo lo lasciamo a voi. Qui merita solo aggiungere che amiamo i controesempi minimali e che, una volta trovato un controesempio, è importante spremerli come limoni. 

Ma come dimostrare una congettura vera? Qui siamo ancor più in mare aperto, ma di nuovo vanno aggiunte alcuni trucchi. Un paio di questi vengono esplorato con un percorso nella prossima sezione.

## Dimostrare buone congetture

se sei riuscito a completare il percorso delle precedenti sezioni, allora dovresti avere un'idea di quali solo le ragioni/il linguaggio del SI, ma anche quelle del NO per il problema euler-dir.


Il fatto (che ci insegna la teoria della complessità) è questo:
...

