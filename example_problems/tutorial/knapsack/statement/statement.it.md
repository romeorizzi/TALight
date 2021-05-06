# Problemi di decisione, di ottimizzazione, di search -- il modello del **Knapsack**

Il modello del **Knapsack** è di pertinenza quando dobbiamo scegliere quali oggetti prendere da un dato insieme. Di ogni oggetto sono noti peso e valore, e il peso totale per gli oggetti scelti non può eccedere un dato limite.

## Formalizzazione

Assumiamo che l'insieme dei possibili oggetti sia finito, di cardinalità $n$. Ogni oggetto $i=0,\ldots,n-1$ ha un *peso* $w_i\in \mathbf{N}$ ed un *valore* $v_i\in \mathbf{N}$
e noi vogliamo scegliere un sottoinsieme $S$ di $\mathbf{N}_n := \{0,1,2,\ldots, n-1\}$ che massimizzi $\sum_{i\in S} v_i$ sotto il rispetto del vincolo $\sum_{i\in S} w_i \leq C$. Qui $C\in \mathbf{N}$ è un parametro in input che esprime il massimo carico sostenibile, la *capacità dello zaino* (knapsack) appunto.

## Prima Formalizzazione (motivata dalle applicazioni)

Denotiamo con $opt(C,n,w,v)$ il valore della soluzione ottima, ossia il massimo valore totale acquisibile senza sforare il vincolo di capacità dello zaino.

**Knapack [come problema di costruzione]**

INPUT: $C$, $n$, e i $2\,n$ numeri naturali
$v_i$ e $w_i$, $i\in \mathbf{N}_n$.

OUTPUT: restituire una scelta di oggetti $S\subseteq \mathbf{N}_n$ tale che $\sum_{i\in S} w_i \leq C$ e $\sum_{i\in S} v_i = opt(C,n,w,v) \geq T$. 

## Formalizzazioni oggetto di studio

Prima di essere un modello fondamentale della Ricerca Operativa e della Computer Science, il Knapsack è un problema per il quale è stato opportuno sviluppare efficaci algoritmi che lo risolvano. Per focalizzare meglio questi sforzi, risultano preferibili delle formulazioni più essenziali del problema.

**Knapack [forma di ottimizzazione]**

INPUT: $C$, $n$, e i $2\,n$ numeri naturali
$v_i$ e $w_i$, $i\in \mathbf{N}_n$, ma anche un valore target $T\in \mathbf{N}$.

OUTPUT: $opt(C,n,w,v)$.

Per analizzare meglio la complessità di questo problema di ottimizzazione combinatoria potremmo associare ad esso il seguente problema di decisione:

**Knapack [forma di decisione]**

INPUT: $C$, $n$, e i $2\,n$ numeri naturali
$v_i$ e $w_i$, $i\in \mathbf{N}_n$, ma anche un valore target $T\in \mathbf{N}$.

OUTPUT: stabilire se $opt(C,n,w,v) \geq T$, dove $opt(C,n,w,v)$ indica il valore della soluzione ottima, ossia il massimo valore totale acquisibile senza sforare il vincolo di capacità dello zaino. Si risponda **SI** oppure **NO**.

# Equivalenza delle tre forme

La prima questione che spesso dobbiamo porci anche nello studio di analoghi problemi è quella di investigare la relazione che vi sia tra queste tre versioni (forma di costruzione, di ottimizzazione e di decisione) del problema Knapsack.
L'intuizione ci dice che la forma di decisione possa solo essere più modesta della forma di ottimizzazione e di quella di costruzione, ma l'unico modo per argomentare questo in modo stringente, formale e conclusivo è quello di ridurre un problema all'altro, ossia operare secondo il seguente schema:

1. assumere di avere un oracolo (una procedura di libreria) che quando le assegnamo un'istanza del problema di ottimizzazione lo risolva;
2. implementare una procedura (scrivere un'algoritmo) che risolva in tempo polinomiale il problema di decisione avvalendosi dell'oracolo. Il nostro algoritmo può chiamare (anche più volte entro una stessa esecuzione) la procedura di libreria.

Di fatto in questo primo caso dovrebbe bastarti una sola chiamata.

Puoi verificare la correttezza della tua riduzione come segue:

```bash
rtal connect -e knapsack dec2opt -- python my_algo.py
```
Il servizio presenterà un'istanza $I$ del problema di decisione e rimarrà in ascolto di tue istanze per il problema di ottimizzazione. Quando sarai pronto, concluderai il dialogo immettendo la tua risposta ('Y' o 'N') per l'istanza I del problema di decisione, ossia con la risposta alla prima ed unica domanda che il servizio ci ha rivolto in apertura del canale. 

Puoi alzare l'asticella con:

```bash
rtal connect -e knapsack dec2opt -a goal=one_single_oracle_call  -- python my_algo.py
```

Diventa più interessante elaborare l'algoritmo che dimostra la riduzione inversa (dove vanno invertiti i ruoli dei due problemi nei punti 1 e 2 dello schema dato sopra), per dimostrare che l'esistenza di un algoritmo polinomiale per il problema di decisione implica l'esistenza di un algoritmo polinomiale per il problema di ottimizzazione.
Ne consegue che la forma di decisione e la forma di ottimizzazione di questo problema sono computazionalmente equivalenti, e cioè:

1. non puoi sperare di risolvere il problema di ottimizzazione se prima non risolvi il (più semplice) problema di decisione;
2. scoprirai che risolvere il problema di decisione ti consentirà di risolvere anche il (più difficile) problema di ottimizzazione. 

In particolare per la riduzione dal problema di ottimizzazione a quello di decisione (la più interessante), ti suggeriamo di utilizzare anche il servizio di valutazione per assicurati che la tua riduzione sia effettivamente polinomiale e non solo pseudo-polinomiale. Anche la tecnica che utilizzerai in questa è pervasiva e di validità generale. 

# Algoritmi polinomiali e pseudo-polinomiali

Non dovrebbe essere difficile scrivere una procedura che risolva il problema di ottimizzazione Knapsack avendo libero accesso ad un oracolo che risolva la forma decisionale del problema. Ti verrà naturale individuare innanzitutto una soluzione che impieghi $opt(C,n,w,v) +1$ chiamate.

Si noti però che un algoritmo che effetua $opt(C,n,w,v) +1$ chiamate non è a rigore polinomiale nel numero di bit necessari per descrivere l'istanza in input in quanto i numeri $v_i$ e $w_i$, $i\in \mathbf{N}_n$, saranno stati convenientemente scritti in binario, utilizzando al più $O(n \log \sum_{i\in \mathbf{N}_n} v_i + w_i)$ inchiostro.
Perchè la nostra riduzione sia davvero polinomiale e non solo pseudo-polinomiale, e per poter quindi concludere sull'equivalenza polinomiale dei due problemi e derivarne correttamente le implicazioni metodologiche su come affrontarne lo studio, alziamo allora l'asticella col seguente goal:

    avvalersi di al più $\log_2 \sum_{i\in \mathbf{N}_n} v_i$ chiamate all'oracolo.

# E il problema di costruzione?

Proseguendo con l'esercizio, potrai esibire una riduzione dal problema di ottimizzazione al problema di costruzione ed anche la riduzione inversa. Poiché queste riduzioni sono componibili,avrai così dimostrato l'equivalenza di questi 3 problemi. 
La tecnica è molto generale.
Scoprirai come per costruire in semplicità e a colpo sicuro una soluzione ottima potranno bastare $n+1$ chiamate all'oracolo per la forma di ottimizzazione del problema Knapsack. 
La metodologia che ti stiamo esibendo è semplice, ma porta lontano.

In realtà nelle applicazioni non siamo tanto interessati solo a scoprire il valore di una soluzione ottima. Ciò che vorremo è che una soluzione ottima ci venisse consegnata.
Vorremmo cioè un algoritmo che ci restituisca un sottoinsieme $S$ di $\mathbf{N}_n$ che è soluzione ammissibile per il problema (ossia $\sum_{i\in S} w_i \leq C$) e per il quale si abbia $\sum_{i\in S} v_i = opt(C,n,w,v)$.

Un tale algoritmo risolverebbe la versione di costruzione del problema, ancora un attimo più ambiziosa della forma di ottimizzazione.
Perché in casi come questo si considera legittimo concentrarsi sulle forme di ottimizzazione o di decisione quando quella che ci interessa è in fondo la forma di costruzione?
Ora conosci la risposta a questa domanda. Inoltre, il tuo stesso modo di approcciarti ai problemi potrà essere più robusto. 


# Considerazioni Conclusive

Poichè crediamo che P $\neq$ NP, ossia che per mettere un problema in P esso debba averci della magia e noi si debba svelarla (ossia si debba arrivare a leggere la struttura sottostante, essenziale e talvolta più o meno invisibile agli occhi almeno finché *lux fuit*). In questo contesto, le riduzioni di cui sopra ci indicano molto chiaramente che possiamo concentrarci sulla versione del problema che ci pare più semplice, con buona aspettativa che quando avremo saputo accendere la luce in quella stanza essa si propagherà in tutta la casa che è nostro compito esplorare (liberamente preso dalla metafora di Andrew Wiles https://www.youtube.com/watch?v=zhpTtJDBFg4). Partiamo dal locale dove ci appare più probabile riuscire a trovare un primo interruttore.
Una nostra tesi in questo percorso didattico è che la fucina metodologica della complessità computazionale è un grandioso strumento anche per guidare i nostri passi e le nostre scelte in queste esplorazioni, e dovrebbe pertanto essere ben conosciuta e praticata da ogni matematico ed informatico.

