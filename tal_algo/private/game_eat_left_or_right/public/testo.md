# Il gioco di mangiarsi una fila indiana da uno dei due estremi

Due giocatori si alternano di turno su una fila indiana di $n$ cioccolatini, scegliendo ad ogni loro mossa quale cioccolatino mangiare da uno dei due estremi della fila. I cioccolatini, si sà, non sono tutti uguali, ma assumiamo che il loro valore di bontà sia espresso con dei numeri naturali. Ciascun giocatore è interessato a massimizzare la somma di tali valori presa sui cioccolatini da lui mangiati. Vince il giocatore la cui somma dei numeri presi è maggiore.

Di fronte alla generica istanza di questo problema (una fila indiana di $n$ numeri naturali) ti è concesso di scegliere se vuoi essere il primo o il secondo a muovere. Dopo aver comunicato questa tua scelta al server, gioca ogni tua mossa rispettando i turni, assicurandoti di non perdere la partita! (Si veda la Nota 1.)


## Interazione
Il tuo programma interagirà col server leggendo dal proprio canale `stdin` e scrivendo sul proprio canale `stdout`.
La prima riga di `stdin` contiene $T$, il numero di partite che verrà giocato.
All'inizio di ogni partita, trovi sulla prossima riga di `stdin` un numero intero $n$, e la riga successiva contiene $n$ numeri naturali separati da spazio.
A questo punto devi dichiarare se preferisci giocare per primo (scrivere $1$ su `stdout`) oppure per secondo (scrivere $2$ su `stdout`). Dopo di chè inizia la partita vera e propria, che inizia con una mossa da parte del giocatore che tu hai stabilito muova per primo, e poi i giocatori si alternano a giocare finché la fila indiana non si è svuotata completamente. Ad ogni mossa, il giocatore di turno scrive `L` o `R` in base a se vuole scegliere il numero più a sinistra o quello più a destra della fila. 

**Nota 1:** Sarà nostra accortezza che, per ogni istanza/partita proposta, la somma dei numeri disposti nella fila indiana iniziale sia sempre dispari. In questo modo, potendo tu scegliere chi debba giocare per primo, potrai sempre vincere ogni partita, indipendentemente da quello che farà l'avversario.

**Nota 2:** Ogni tua comunicazione verso il server deve essere collocata su una riga diversa di `stdout` e ricordati di forzarne l'invio immediato al server effettuando un flush del tuo output! 

**Nota 3:** Puoi assumere che il valore di nessun cioccolatino ecceda $10^5$-

## Esempio

Le righe che iniziano con `>` sono quelle inviate dal server, quelle che iniziano con `<` sono quelle inviate dal client. (Ignora però i commenti, ossia quella parte della riga che comincia col primo carattere di cancelletto '#' in essa eventualmente contenuto). 

```
> 2     # numero di testcase/istanze/partite
> 4     # nella prima partita si parte da un vettore $n=4$ elementi
> 0 8 5 4    # il vettore proposto dal server come campo di gioco
< 2     # il problem solver (o il programma che gioca per lui) sceglie di muovere per secondo
< R     # il server muove prelevando il numero sull'estremo destro
> R     # il problem solver muove prelevando il numero sull'estremo destro
< R
> L     # il problem solver preleva il numero sull'estremo sinistro. Il vettore è ora vuoto e la partita termina.
> 4     # nella seconda partita si parte da un vettore $n=4$ elementi
> 7 4 5 3    # il vettore proposto dal server come campo di gioco
< 1     # il problem solver sceglie di muovere per primo
> R
< L
> R
< L     # il server preleva l'ultimo numero e la partita termina.
```

## Subtask

Il tempo limite per istanza (ossia per ciascun testcase) è sempre di $1$ secondo.

I testcase sono raggruppati nei seguenti subtask.

* **[10 istanze] small:**  $n \leq 6$
* **[20 istanze] medium:** $n \leq 10$
* **[20 istanze] big:**    $n \leq 100$

In generale, quando si richiede la valutazione di un subtask vengono valutati anche i subtask che li precedono, ma si evita di avventurarsi in subtask successivi fuori dalla portata del tuo programma che potrebbe andare in crash o comportare tempi lunghi per ottenere la valutazione completa della sottomissione. Ad esempio, chiamando:

```
    rtal -s wss://ta.di.univr.it/algo  connect -a size=medium  game_eat_left_or_right -- python my_solution.py
```

vengono valutati, nell'ordine, i subtask:

**small**, **medium**.

Il valore di default per l'argomento **size** è **big** che include tutti i testcase.