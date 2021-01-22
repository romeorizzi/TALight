# sum

Indipendentemente dal fatto che siano inviate dal server (S) al dispositivo in locale (L) oppure viceversa, le righe che iniziano col carattere '!' comunicano la chiusura del canale, la riga può proseguire con un commento.
Le righe che iniziano col carattere cancelletto '#' sono commenti, e possono essere inviati in modo del tutto asincrono.
Quando S intende porre una domanda, invia una riga che inizia in '?' cui segue un numero naturale $n$.  
A questo punto L può rispondere inviando sul canale due numeri naturali $a$ e $b$, che vorrebbero offrire una scomposizione di $n$ come $n=a+b$.
Se la risposta non ha questo formato allora S chiuderà il canale senza porre altre domande.
Se la risposta ha questo formato allora S, prima di porre altre domande, invierà una riga che inizia col carattere 'y' se invero $n=a+b$ o col carattere 'n' in caso contrario, la riga può proseguire con un commento.
Il server invierà sul canale un certo numero di domande e le inframmezzerà con righe di altri commenti.

## Esempi di interazione

Nei seguenti esempi, le righe che iniziano con "S> " sono quelle inviate dal server, mentre quelle inviate dal tuo dispositivo locale sono prefissate con "L> "):

```t
S> # buongiorno!
S> ? 42
L> 11 31
S> y vero! 42=11+31
S> # io avrei risposto 42=42+0
S> ? 22
L> 11 31
S> n falso: 11+31=42, mica 22
S> # ma va là, mica vero! 11+31= 42, forse sei rimasto impiantato su domanda precedente?
S> ? 12
L> # questa volta vedrai che non mi sbaglio, prima avevo fatto apposta
L> 1 11
S> y
S> # ho troppo carico ora per tenere in piedi questa piacevolissima conversazione! ciao ciao ciao ...
S> ! :)
```

## Servizi offerti

Assumendo di aver collocato nella propria variabile di ambiente `PATH` la cartella `$TAlight/rtal/target/debug/rtal`, dove $TAlight indichi il percorso al repo git dove TAlight è stato collocato,
l'elenco dei servizi offerti per il problema `sum` può essere ottenuto invocando a riga di comando il comando:
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
Scopriamo ad esempio che il servizio `sum` prevede il supporto per due lingue (italiano ed inglese) e consente, attraverso il parametro `numbers`, la richiesta di lavorare con numeri di una sola cifra oppure più grossi (non meglio specificato il range), mentre `twodigits` è il valore di default per questo parametro.
La lingua di default è l'italiano. Tutti i valori di default sono settati dal docente nel file `meta.yaml` del problema. Anche un problem-solver (studente) potrà operare questa modifica e personalizzazione se ha scaricato l'intero problema in locale: lanciato il server `rtald` in locale e modificando il file `meta.yaml` nella sua copia del problema `sum` potrà riconfigurare ogni comportamento ed esplorare nuove possibilità.
Lasciamo a tè di riscontrare come vadano interpretate le ulteriori informazioni reperite dal file `meta.yaml`. Un punto importante è: `TAlight` è stato progettato per promuovere possibilità di esplorazione autonoma e ciò che noi chiamiamo brake-on-through-to-the-other-side, ossia la transizione da problem-solver a problem-maker.

Quando hai compreso la challenge che spesso resta sottostante ad un servizio, ed individuato un tuo metodo generale per la soluzione del problema, puoi costruire un tuo bot che sostenga in tua vece il dialogo col server.

Puoi poi metterlo in campo con:

```bash
rtal connect -a numbers=big sum sum_and_product  -- sum_and_product_mysolution.py
```
Ovviamente il file `sum_and_product_mysolution.py` dovrà avere i permessi settati per poter essere eseguito, non è invece importante il linguaggio che hai scelto per produrre un tale eseguibile.
Se vuoi puoi osservare da vicino come avvenga l'interazione tra il tuo bot `sum_and_product_mysolution.py` ed il servizio `sum_and_product` da noi offerto per il problema `sum`, ti basta aggiungere il paramtro `-e` come segue: 


```bash
rtal connect -e -a numbers=big sum sum_and_product  -- sum_and_product_mysolution.py
```

Menzioniamo infine che nella cartelle `applets` del progetto `TAlight`, il file `sum-protoapplet.html` esemplifica le basi su come realizzare l'interazione entro un browser. Puoi vederlo in azione ad esempio con

```bash
~/TAlight/applets$ google-chrome sum-protoapplet.html
```
