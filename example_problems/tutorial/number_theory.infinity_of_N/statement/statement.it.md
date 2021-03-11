# infinity_of_N (l'infinità dei numeri naturali)
Gli algoritmi sono prove e le prove il più delle volte vengono fornite con algoritmi.


## Task 1:Implementare una macchina automatica (un codice eseguibile) che, in un ciclo senza fine, ogni volta che viene fornito in input un numero naturale, ne restituisca uno più grande

Questa macchina dimostrerà due cose:

1. non esiste una cosa come il numero naturale più grande;

2. c'è una quantità infinita di numeri naturali là fuori.

Input da `stdin` e output in` stdout`, ogni riga è solo un numero, il formato di ogni riga è una sequenza di cifre seguita da una nuova riga. La prima cifra potrebbe essere uno zero se e solo il numero rappresentato è zero.
### Services

Lancia i seguenti comandi:

```t
> rtal connect infinity_of_N bigge_and_bigger
```

Per giocare tu stesso al gioco a cui spara il più grande naturale contro la tua macchina.
Una sequenza di sorpassi inarrestabili in cui il server S dovrà gettare la spugna prima o poi (se non sbaglierai).

Per assicurarti di non poter commettere errori (cioè per ottenere una prova di qualcosa), puoi usare un tuo semplice bot con cui giocare al tuo posto

```t
> rtal connect infinity_of_N bigge_and_bigger -- my_bot.py
```

Qui `my_bot.py` è solo il nome completo di un eseguibile che si trova sulla tua macchina locale. Ciò coinvolgerà il tuo bot in una partita (potenzialmente) infinita contro S.

## Task 2: Dopo aver implementato la procedura di cui sopra, potresti anche essere tentato di provare il principio di Archimede che afferma che, dato un numero reale positivo $ \ varepsilon $, esiste un $ N_ \ varepsilon $ naturale tale che $ \ frac {1} {N_ \ varepsilon } <\ varepsilon $.

Implementare quindi una macchina automatica che, in un ciclo infinito, ogni volta che viene fornito in input un numero reale positivo $ \ varepsilon $, restituisca un $ N_ \ varepsilon $ così naturale che $ \ frac {1} {N_ \ varepsilon} <\ varepsilon $.
Input e output come sopra, solo quello nella rappresentazione di un numero reale, una singola occorrenza del carattere punto pieno '.' potrebbe intrufolarsi da qualche parte tra due cifre. La prima cifra potrebbe essere uno zero se e solo non è immediatamente seguita da un'altra cifra.

### Servizi

Abbiamo scelto di dare due nomi diversi a questo servizio:
usa `razionali_are_dense_into_reals` o` archimede`, a tuo piacimento,
e usa la sintassi flessibile del comando TAlight `rtal` introdotto sopra per chiamare questo servizio.
Se vuoi saperne di più sul lounch "rtal"
```t
> rtal --help
```
or 
```t
> rtal connect --help
```


Se vuoi saperne di più sui parametri dei servizi di un problema lancia
```t
> rtal list infinity_of_N - v
```

## Examples of interactions (possible plays)

Negli esempi, le righe inviate dal server del servizio progettato dall'autore del problema hanno il prefisso "S>", mentre quelle inviate dall'agente locale (o tu o il tuo bot) hanno il prefisso "L>"):


### Task 1

```t
S> # ciao! Giochiamo a chi spara il numero più grande!
S> #Sarò io a iniziare e poi ci alterneremo.
S> 42
L> 50
S> 55
L> 60
S> # bel colpo!
S> 1000
L> 2000
S> Complimenti mi stai stracciando!
S>! Butto la spugna. Bella partita :)
```
Come vedi, le righe che iniziano con "#" dovrebbero essere trattate come commenti e vengono semplicemente ignorate dai due principali agenti nella conversazione (i bot).
Una riga che inizia con "!" dal lato del server chiude la connessione quando non si verificano errori a livello di protocollo. Il resto di questa riga di chiusura può essere ancora una volta un commento arbitrario.

### Task 2
La struttura generale del protocollo è la stessa di cui sopra.

```t
S> # Ciao! Hai il compito di dimostrarmi che i razionali sono compresi nel reale. Potremmo lanciarlo sotto forma di un gioco. Ora è il momento di giocare!
S> # Sarò io a iniziare e poi a turno.
S> 42
L> 50
S> 55
L> 60
S> # bella mossa
S> 1000
L> 2000
S> ok! vero! 42=11+31
S> ! Getto la spugna,bella partita.
```





