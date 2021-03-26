# sum

Questo è il primo problema del tutorial che intende illustare l'uso di `TALight` sia ai problem solvers (apprendisti) che ai problem makers (addstratori a competenze).
La competenza richiesta dal problema `sum` è di saper trovare due numeri con una certa somma (ed eventualmente il cui prodotto sia massimo), oppure con somma e prodotto (oppure somma e differenza) assegnati.
Come tale potrebbe essere orientativamente adatto per la fascia di età 8-15 oppure anche prima nei suoi subtask più elementari su cui offre comunque del dialogo.

## sui problemi in `TALight`

Un problema curato in `TALight` è un giocattolo ben congegnato che viene con dei servizi di corredo progettati e ralizzati dal problem maker per offrire all'apprendista delle occasioni di sperimentazione autonoma. Tali servizi offrono feedback, indirizzano la curiosità e gli approcci di soluzione, e supportano dei dialoghi che coinvolgano il problem solver in una sfida e lo volgano ad un approccio attivo all'apprendimento. L'attivazione, sviluppo e consolidamento delle potenzialità prime di apprendimento e crescita, il loro eterno recupero a partire dalle motivazioni, sono ancor più irrinuciabili nel contesto attuale, e ci riguardano tutti, dal neet al ricercatore affermato che comunque deve saper reinventarsi ed ampliarsi sempre più velocemente.

## struttura generale dei dialoghi offerti dai servizi `TALight`

Indipendentemente dal fatto che siano inviate dal server (S) al dispositivo in locale (L) oppure viceversa, le righe che iniziano col carattere cancelletto '#' sono commenti, e possono essere inviate in modo del tutto asincrono.
Quando il server invia una riga che inizia col carattere '!' comunica la chiusura del canale per terminare un'interazione che si è svolta nel rispetto del protocollo sotteso, la riga può proseguire con un commento.
L'interazione può essere altresì interrotta da S quando L non rispetta il protocollo o le tempistiche, o in caso di problemi di connessione. Se riscontrate comportamenti che si discostano da questi segnalateceli opportunamente documentati e circostanziati.
Voi problem solvers, o il bot che dovesse agire in vostra vece, sul canale potete fare quello che volete, per meglio sperimentare, il che include la possibilità di commettere errori. Se l'errore comporta una violazione del protocollo il server chiuderà il canale senza garantire ulteriore feedback. Lo saprete perché l'ultima riga ricevuta da S non inizia in '!'. 

## problema `sum`, cenni sul protocollo sotteso

Quando S intende porre una domanda, invia una riga che inizia in '?' cui segue un numero naturale $s$ (nei servizi `sum_and_difference` e `sum_and_product` i numeri saranno due e separati da spazio).  
A questo punto L può rispondere inviando sul canale due numeri naturali $a$ e $b$, che vorrebbero offrire una scomposizione di $s$ come $s=a+b$.
Se la risposta non ha questo formato allora S chiuderà il canale senza porre altre domande.
Se la risposta ha questo formato allora S, prima di porre altre domande, invierà una riga che inizia con la stringa "ok!" se invero $s=a+b$ o con la stringa "no!" in caso contrario, la riga può proseguire con un commento od una spiegazione.
Il server invierà sul canale un certo numero di domande e le inframmezzerà con righe di altri commenti.
Siamo convinti che, e l'idea è anche che, il protocollo (sotteso) si chiarisca meglio e più efficacemente attraverso la sperimentazione diretta
di dialoghi coi servizi offerti.

Per questo primo esempio forniamo comunque degli esempi irrealistici (ma che in realtà un problem maker motivato avrebbe tutti gli strumnti per poter supportare entro `TALight`) di come potrebbero svolgersi dei dialoghi.


## Esempio di interazione

Nei seguenti esempi, le righe che iniziano con "S> " sono quelle inviate dal server, mentre quelle inviate dal tuo dispositivo locale sono prefissate con "L> "):

```t
S> # buongiorno!
S> ? 42
L> 11 31
S> ok! vero! 42=11+31
S> # io avrei risposto 42=42+0
S> ? 22
L> 11 31
S> no! falso: 11+31=42, mica 22
S> # ma va là, mica vero! 11+31= 42, forse sei rimasto impiantato su domanda precedente?
S> ? 12
L> # questa volta vedrai che non mi sbaglio, prima avevo fatto apposta
L> 1 11
S> ok!
S> # ho troppo carico ora per tenere in piedi questa piacevolissima conversazione! ciao ciao ciao ...
S> ! :)
```

## Servizi offerti

L'elenco dei servizi offerti per il problema `sum` può essere ottenuto invocando a riga di comando il comando:
```bash
> rtal list sum
```

Leggendo l'output di questo comando scopriamo che i servizi offerti sono tre: `sum`, `sum_and_difference` e `sum_and_product`.
Il servizio `sum` si presta alla conduzione del dialogo di cui sopra.
Il servizio `sum_and_difference` conduce un analogo dialogo dove il server, ad ogni query, prescrive non solo la somma ma anche il prodotto dei due numeri, ora univoci, da ritornargli.
In `sum_and_product` il server prescrive somma e prodotto dei due numeri da determinare.

Per ottenere informazioni più di dettaglio, quali i parametri di utilizzo dei servizi, si immetta:

```bash
> rtal list sum -v
```
Leggendo ed interpretando l'output di questo comando scopriamo diverse cose.
Scopriamo ad esempio che il servizio `sum` prevede il supporto per due lingue (italiano ed inglese, con l'italiano settato a default) e consente, attraverso il parametro `numbers`, la richiesta di lavorare con numeri di una sola cifra oppure più grossi (non meglio specificato il range), mentre `twodigits` è il valore di default per questo parametro.
Tutti i valori di default sono settati dal docente nel file `meta.yaml` del problema. Anche un problem-solver (studente) potrà operare questa modifica e personalizzazione se ha scaricato l'intero problema in locale: lanciato il server `rtald` in locale e modificando il file `meta.yaml` nella sua copia del problema `sum` potrà riconfigurare ogni comportamento ed esplorare nuove possibilità.
Lasciamo a tè di riscontrare come vadano interpretate le ulteriori informazioni reperite dal file `meta.yaml`. Un punto importante è: `TALight` è stato progettato per promuovere possibilità di esplorazione autonoma e ciò che noi chiamiamo brake-on-through-to-the-other-side, ossia la transizione da problem-solver a problem-maker.

Ma confrontati in un dialgo con uno dei servizi da noi predisposti per questo problema, ad esempio col servizio `sum` (omonimo del problema che lo ricomprende) così configurato:

```bash
rtal connect -a obj=max_product -a numbers=twodigits sum sum
```

Quando l'apprendista ha compreso la challenge che spesso resta sottostante ad un servizio, ed individuato un suo metodo generale per la soluzione del problema, può costruire un bot che sostenga in sua vece il dialogo col server.

Un bot `sum_and_product_mysolution.py` che affronti in nostra vece il dialogo supportato dal srvizio `sum_and_product` può essere messo in campo con:

```bash
rtal connect -a numbers=big sum sum_and_product  -- sum_and_product_mysolution.py
```
Ovviamente il file `sum_and_product_mysolution.py` dovrà avere i permessi settati per poter essere eseguito, non è invece importante il linguaggio scelto per produrre un tale eseguibile.
L'interazione che intercorre tra tuo bot `sum_and_product_mysolution.py` ed il servizio `sum_and_product` può essere osservata aggiungendo il paramtro `-e` come segue: 

```bash
rtal connect -e -a numbers=big sum sum_and_product  -- sum_and_product_mysolution.py
```

Menzioniamo infine che nella cartelle `applets` del progetto `TALight`, il file `sum-protoapplet.html` esemplifica le basi su come realizzare l'interazione entro un browser. Puoi vederlo in azione ad esempio con

```bash
~/TALight/applets$ google-chrome sum-protoapplet.html
```
