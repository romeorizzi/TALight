
Documento di statement.md

# Magic Indexes

### Nostre prime riflessioni sul problema:

PROBLEMA PROPOSTO:
    Input: un vettore ordinato A di n numeri interi distinti
    Def:  ogni posizione i=0, ..., n-1, tale che A[i]=i è un magix-index.
    Task: trovare i magic index/il magic index se ce ne sono.

    Voglia di log n checks

    se ce ne sono formano un intervallo consecutivo, vorremo individuare gli estremi di tale intervallo o risondere NONE

==================================================================
Puzza che in testa conviene riferirsi ad un "modello" come questo:

PROBLEMA/MODELLO DA RICERCA BINARIA cui ci si potrebbe riferire:

Input: ho un vettore di palline bianche e nere dove a sinista di una pallina nera tutte le palline sono nere.

Trovare dove avvine l'eventuale transizione.

==================================================================

Nel vettore avete che i numeri sono disposti in modo ordinato e sono numeri interi diversi (tra uno e l'altro c'è un salto di almeno uno). Questo implioa che:

    Lemma: Valgono le seguenti proprietà:
        1. se per un certo i vale che A[i] < i allora A[j] < j per ogni j <= i
        2. se per un certo i vale che A[i] > i allora A[j] > j per ogni j >= i
        3. se A[i] = i  e  A[j] = j allora  A[k] = k  per ogni k nell'interallo [i,j]   (e quindi gli eventuali magic-index formano un intervallo)

Il modello da adottare potrebbe essere:
    INPUT: abbiamo accesso tramite query su singolo elemento ad un vettore monotonamente riempito coi valori -1,0,1
    TASK:   identificare l'intervallo di zeri. (Trovare la prima ed ultima  posizione a 0, oppure NONE)

A[i] = -1   se  A[i] < i
A[i] =  0  se  A[i] = i
A[i] =  1   se  A[i] > i

=======

CON RIFERIMENTO AL GIOCO OTTIMO:
1. data una configurazione, saper individuare una mosa ottima secondo vari criteri tra cui sicuramente (partiamo con) il criterio di MINIMIZZARE IL NUMERO DI QUESRY NEL CASO PEGGIORE
2. data una configurazione, saper produrre una mossa ottima
3. data una configurazione, saper dire quali mosse siano ottime
4. data una configurazione, saper dire quale sia il numero di mosse per risolverla nel caso peggiore  

OSSERVIAMO relezion9 tra questi obiettivi:
    se ho in tasca l'obiettivo 4, allora ho in tasca l'obiettivo 3
    se ho in tasca l'obiettivo 3, allora ho in tasca l'obiettivo 2
    se ho in tasca l'obiettivo 2, allora ho in tasca l'obiettivo 1

Gli obiettivi 1 e 2 sono equivalenti
2 non è chiaro a priori che implichi 3
3 è parecchia strada (problem dependent) che implichi 4  (che non vuol dire che risolto 4 poi non segua anche 3)

Sulle equivalenze già dimostrate gioca che:
    su ogni configurazione, il numero di possibili mosse per il giocatore guesser è al più polinomiale (questo ci consegna ad esempio l'implicazione da 4 a 3)
    nel caso del nostro puzzle è vero anche che, in ogni situazione in cui è chiamato a muover, il giocatore puzzle poser ha al più O(1) opzioni. Questo può far ben sperare che anche l'obiettivo 4 sia raggiungibile, se il 3 è raggiungibile. Di certo 3 + 3' implicherebbero 4:

        3'. data una situzione per il giocatore puzzle poser, saper dire quale sia l'opzione che mantiene alto il numero di mosse nel caso peggiore

       Nota: vorremmo quindi avere sia la competenza 3 che la competenza 3', e si noti che 4 le implica entrambe.

        URGE CHIARIRSI LE IDEE SU COSA INTENDIAMO PER CONFIGURAZIONE (posta al guesser) O SITUAZIONE (posta al puzzle poser)

        1. CONFIGURAZIONE INIZIALE (posta al guesser):  sò che gli indici del vettore vanno da pos_begin a pos_end   (nella vera configurazione iniziale probabilmente avremo pos_begin=0  a pos_end=N-1).
           Possiamo identificarla ("pescarla") con un solo paramentro  n := pos_end - pos_begin
           Possiamo vedere n come "su quante celle di vettore contigue si estende la mia candida ignoranza".

           f(n) := opt_pessimistic_blank(n: number of unknown)    (con questa portiamo a casa l'obiettivo 4, ossia tutti (per quanto riguarda il criterio del caso peggiore))
           ...   (eventulmente poi altre per altri criteri/obiettivi)      

        2. CONFIGURAZIONE DOPO PRIMA MOSSA (posta al guesser):  sò che gli indici del vettore vanno da pos_begin a pos_end   e che A[pos_begin] = 0  (per simmetria)

          g(n) := opt_pessimistic_knowing_only(n: number of unknown)


     f(n)  dovrà dipendere dà sia da f che da g

     g(n)  dovrà dipendere solo dà  g

    CALCOLIAMO PRIMA g

    n  0 1 2 3 4 5 6 7 8 9 0 1
    g  0 1 2 2 3


    0 1 2 3 4 5 <-- indici di posizione
    0 ? ? ? ? ? <-- configurazione/situazione  (quando n=5)
          ^
    for ^ over all possibilities (or maybe we can take in consideration just the middle one)
    min_{over ^} ( max( CASE1 for the answer, CASE2 for the answer) ), dove

    CASE1: se ? = 1
           return 1+g(^)
    CASE2: se ? = 0
           return 1+g(n-^)
    Quindi:
        return 1 + max(g(^), g(n-^)), dove ^ = n//2

    CALCOLIAMO QUINDI f

    n  0 1 2 3 4 5 6 7 8 9 0 1
    f  0 1 2 3 4 5 5

    1 2 3 4 5 6 <-- indici di posizione
    ? ? ? ? ? ? <-- configurazione/situazione  (quando n=6)
        ^
    for ^ over all possibilities (or maybe we can take in consideration just the middle one)
    min_{over ^} ( max( CASE1 for the answer, CASE2 for the answer) ), dove

    CASE-11: se ? = -1
           return 1+ f(n-^)
    CASE0: se ? = 0
           return 1+ g(^-1) + g(n-^)
    CASE1: se ? = 1
           return 1+ f(^-1)
    Quindi:
        return 1 + max(f(^-1), f(n-^), g(^-1) + g(n-^)) = 1 + max(f(max(^-1, n-^)), g(^-1) + g(n-^)), dove ^ = n//2

# ANALISI DI COSA SO' DEL VETTORE IN MEZZO AD UNA PARTITA:

    Abbiamo chiarito che vogliamo consentire all'utente di ripartira da una configurazione di gioco intermedia.
    Essa può essere specificata con la seguente rappresentazione:

    0 1   2 3 4 5 6   7 8 9  10 11  12 13 14
    ? ? num ? ? ? ? num ? ? num  ? num  ?  ?

    e possiamo anche dare un servizio che da questa rappresentazione ne fornisca una strutturale semplice o potenziata:

    0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
    ? ? < ? ? ? ? = ? ?  =  ?  >  ?  ?   (strutturale semplice)

    0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
    < < < ? ? ? ? = = = = ? > > >   (strutturale potenziata)

    3< 4? 4= 1? 3>   (strutturale potenziata compatta), ossia esattamente 5 numeri

     ^((num (<|=|>|?))*)$  <-- questa è un opzione
     ^(num<num?num=num?num>)$ <-- questa allo studente rischia di arrivare come deus ex-machina

    3 4 4 1 3  <-- ALCUNI DI QUESTI NUMERI POSSONO ESSERE 0  (possiamo lasciare i caratteri impliciti, oppure esplictarli. Se implicit: < ? = ? > )

L'utente potrà chiedere di giocare una partita partendo da una tale configurazione (specificando il ruolo scelto per i due giocatori).

Per i servizi di gioco e di eval gioco tra gli argomenti del servizio dobbiamo dare la possibilità di scegliere se avere la configurazione selezionata ad ogni mossa e in quale formato.

Probabilmente:
    per n < 50 possiamo consentire di optare per ogni rappresentazione
    per n in [50,100] possiamo consentire le rappresentazioni strutturali
    per n > 100 solo la strutturale compatta
