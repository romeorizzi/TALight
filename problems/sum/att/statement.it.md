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

Esempio di interazione che prende avvio da terminale ma poi richiede coinvolgimento di programma P in locale:

```t
S> # buongiorno!
S> ? 42
L> 11 31
S> y vero! 42=11+31
S> ? 22
L> # clone streams my_excutable_program
L> 22 0
L> Ctrl-D
S> ? 33
P> ! 33 0
```


## Servizi offerti

I servizi offerti per questo problema, e relativi parametri di utilizzo,
sono rilevabili dall'apposito comando di `TAlight`:

```bash
> rtal/target/debug/rtal list sum -v
```
Leggendo ed interpretando l'output di questo comando scopriamo diverse cose.
I servizi offerti sono due: `sum` e `sum_and_product`.
Un'informazione non direttamente deducibile è che il primo servizio è inteso a condurre il dialogo di cui sopra, mentre il secondo conduce un analogo dialogo dove il server, ad ogni query, prescrive non solo la somma ma anche il prodotto dei due numeri da ritornargli.
Scopriamo che attualmente entrambi i servizi prevedono il supporto per due lingue (italiano ed inglese) e consentono la richiesta di lavorare con numeri più grossi (non meglio specificato il range) attraverso il parametro `numbers`. Si noti che `small` è il valore di default per questo parametro. Settando opportunamente il valore di default per il parametro `lang` nel file `meta.yaml` del problema il docente imposta la lingua di default. Anche un problem-solver (studente) potrà operare questa modifica e personalizzazione se lavora in locale, ossia lanciando il server `rtald` in locale e modificando il file `meta.yaml` nella sua copia del problema `sum` che si è scaricato in locale.
Lasciamo a tè l'esplorazione su come vadano interpretate le ulteriori informazioni reperite dal file `meta.yaml`. Un punto importante è: `TAlight` è stato progettato per promuovere possibilità di esplorazione autonoma e ciò che noi chiamiamo brake-on-through-to-the-other-side, ossia la transizione da problem-solver a problem-maker.

Quando hai compreso la challenge che spesso resta sottostante ad un servizio, individuando un tuo metodo generale, puoi costruire un tuo bot che sostenga in tua vece il dialogo col server.

Puoi poi metterlo in campo con:

```bash
rtal connect -a numbers=small sum sum_and_product  -- sum_and_product_mysolution.py
```
Se vuoi poi osservare da vicino come avvenga l'interazione tra il tuo bot `sum_and_product_mysolution.py` ed il servizio `sum_and_product` da noi offerto per il problema `sum`, ti basta aggiungere il paramtro `-e` come segue: 


```bash
rtal connect -e -a numbers=small sum sum_and_product  -- sum_and_product_mysolution.py
```

Menzioniamo infine che nella cartelle `applets` del progetto `TAlight`, il file `sum-protoapplet.html` esemplifica le basi su come realizzare l'interazione entro un browser. Puoi vederlo in azione ad esempio con

```bash
~/TAlight/applets$ google-chrome sum-protoapplet.html
```
