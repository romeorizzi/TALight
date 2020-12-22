# sum

Indipendentemente dal fatto che siano inviate dal server (S) al dispositivo in locale (L) oppure viceversa, le righe che iniziano col carattere '!' comunicano la chiusura del canale, la riga può proseguire con un commento.
Le righe che iniziano col carattere cancelletto '#' sono commenti, e possono essere inviati in modo del tutto asincrono.
Quando S intende porre una domanda, invia una riga che inizia in '?' cui segue un numero naturale $n$.  
A questo punto L può rispondere inviando sul canale due numeri naturali $a$ e $b$, che vorrebbero offrire una scomposizione di $n$ come $n=a+b$.
Se la risposta non ha questo formato allora S chiuderà il canale senza porre altre domande.
Se la risposta ha questo formato allora S, prima di porre altre domande, invierà una riga che inizia col carattere 'y' se invero $n=a+b$ o col carattere 'n' in caso contrario, la riga può proseguire con un commento.
Il server invierà sul canale un certo numero di domande e le inframmezzerà con righe di altri commenti. 

Esempio di interazione (nell'esempio, le righe che iniziano con "S> " sono quelle inviate dal server, mentre quelle inviate dal tuo dispositivo locale sono prefissate con "L> "):
```
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

Servizi offerti:

```
> TAlight ...

```

Prego dettagliare i servizi offerti e la modalità per richiederli ...