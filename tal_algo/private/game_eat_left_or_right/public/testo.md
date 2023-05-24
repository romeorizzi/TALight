# Il gioco di Anna e Barbara

Anna e Barbara hanno scoperto un nuovo gioco: si gioca su un vettore $V$ di $n$
numeri naturali. Il primo giocatore scegliere un numero da un estremo e lo,
poi il secondo giocatore fa lo stesso, e il gioco continua così finché il
vettore non si svuota. Vince il giocatore la cui somma dei numeri presi è
maggiore.

Ad Anna piace sempre giocare come il primo giocatore, mentre Barbara vuole
sempre andare seconda. Tu vuoi fare una partita, ma hai già visto il vettore
che verrà usato. Usa questa informazione per scegliere contro chi giocare in
modo da essere sicuro di non perdere e vinci la partita!

## Assunzioni

Sono presenti le seguenti `size`, dove il default è `big`:

* `small`: $n \leq 8$, $\max(V) \leq 20$
* `big`: $n \leq 50$, $\max(V) \leq 10^6$

La somma dei valori di $V$ è sempre dispari.

Il tempo limite per testcase è di $5$ secondi.

## Interazione
La prima riga contiene $T$, il numero di partite che verrà giocato.
In ogni partita ti vengono dati sulla prima riga $n$, e sulla seconda riga
il vettore $V$ di naturali separati da spazio. A questo punto tocca a te,
scrivi 0 se vuoi giocare per primo, o 1 se vuoi giocare per secondo.
La partita inizia dal primo giocatore e alterna i giocatori finché tutti
i numeri non sono stati presi. Il giocatore a cui tocca deve scrivere `L`
o `R` seguito da un a capo in base a se vuole scegliere il numero più
a sinistra o quello più a destra.

Per ottenere `AC` devi vincere la partita. È sempre possibile vincere
la partita per una qualche scelta di che giocatore essere e delle mosse
da effettuare, indipendentemente da quello che farà l'avversario.


## Esempio

Le righe che iniziano con `<` sono quelle inviate dal server, quelle che
iniziano con `>` sono quelle inviate dal client.

```
< 2
< 4 
< 0 8 5 4
> 0
> R
< R
> R
< L
< 4
< 7 4 5 3
> 1
< R
> L
< R
> L
```
