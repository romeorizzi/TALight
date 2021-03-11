# Indovina il codice segreto! (mastermind)

Immaginati nelle vesti di un _decodificatore_.
Il tuo avversario, un _codificatore_, ha scritto un codice segreto di quattro cifre, ognuna delle quali può assumere un valore tra $0$ e $5$.

Per vincere la sfida, devi scrivere una procedura che individui il suo codice segreto, effettuando il minor numero di tentativi.
Ad ogni tentativo riceverai un feedback che ti consentirà di ricevere informazioni sul codice segreto impostato dall'avversario.
Una prima funzione di valutazione ritorna tanti pioli neri quante sono le posizioni in cui ìl codice segreto e quello da tè sottomesso presentano lo stesso colore. Una seconda funzione (chiamare la quale non viene conteggiato come ulteriore tentativo se la chiami sullo stesso codice che hai appena passato alla funzione sopra) ti ritorna tanti pioli bianchi quanti sono gli ulteriori colori indovinati, ma collocati fuori posto.

Le regole ti verranno forse più chiare dopo qualche partita giocata online meglio ancora tramite TAlight stesso (usa 6 colori su 4 posizioni, possibilmente ripetuti):

[un player esterno, online](http://www.webgamesonline.com/mastermind/index.php)

## Goal 1 - saper punteggiare correttamente un tentativo

Assicuriamoci innanzitutto di aver compreso le regole del gioco:
ove tu conoscessi il codice segreto e ti venisse esibito un tentativo, saprsti valutarlo restituendo il numero corretto di pioli neri e bianchi?

Si assuma che il codice sia di $n$ cifre, dove ogni cifra è un numero naturale grande al più $m$.

I seguenti subtask e servizi, oggetto di feedback, potranno confermarti di aver compreso correttamente le regole del gioco.

* [servizio:] ottieni_valutazione: puoi sottomettere una coppia di codici (quello segreto e un tentativo), per richiedere quale sia la valutazione corretta per quella coppia.

```t
TAlight ask --problem=mastermind -check_evaluation m n codice_segreto codice_tentativo  
```

dove $m$ ed $n$ sono due numeri naturali positivi e `codice_segreto` e `codice_tentativo` sono due sequenze di $n$ numeri naturali nell'intrvallo $[0,m]$ separati da spazio.

1. [subtask 1:](https://per-ora-costruiamo-qusti-URL-a-mano-ma-sarebbe-utile-costruzione-dinamica-e/o-da-problm.yaml) valuta tu un tentativo, $n=4$ e $m = 5$

2. [subtask 2:](https://per-ora-costruiamo-qusti-URL-a-mano-ma-sarebbe-utile-costruzione-dinamica-e/o-da-problm.yaml) valuta tu un tentativo, $n$ ed $m$ generici

### Get feedback
Puoi ottenere del feedback sia dalla riga di comando con:

```t
TAlight ask --problem=mastermind --goal=1 --subtask=SUBTASK_NUMBER  tuo_file_eseguibile 
```

Il tuo file eseguibile sarà un programma che gioca per tè oppure un applt attraverso cui potrai giocare. In entrambi i casi dovrà rispettare il sguente protocollo di comunicazione:

1. nella prima riga di `stdout` si scriva:
START

2. si leggano dalla prima riga di `stdin` due numeri interi separati da spazio:
   i valori di $m$ ed $n$

3. si legga il codice segreto dalla seconda riga di `stdin`:
   $n$ interi separati da spazi, tutti compresi nell'intervallo $[0,m]$

4. si legga il codice tentativo dalla terza riga di `stdin`:
   $n$ interi separati da spazi, tutti compresi nell'intervallo $[0,m]$

5. si riporti la valutazione sulla seconda ed ultima riga di `stdout`:
   due interi $N$ e $B$ separati da spazi: $N=$il numero di pioli neri, $B=$il numero di pioli bianchi.


## Goal 2 - saper ricostruire il codice segreto

In questo caso il nostro feedback si baserà su un'interazione tra un tuo programma che esguirai in locale (un applet entro il quale giocare tu oppure un programma che giochi per tè) ed un nostro codice sul server.
Una volta lanciato il comando:

```t
TAlight ask --problem=mastermind --goal=2 --subtask=SUBTASK_NUMBER  tuo_file_eseguibile 
```

Il protocollo da rispettare è il seguente:

1. nella prima riga di `stdout` si scriva:
START

a fronte di questa azione il server elabora un codice segreto, dove $m$ d $n$ saranno stati scelti coerentemente al subtask scelto od a tue prescrizioni più specifiche 

2. si leggano dalla prima riga di `stdin` due numeri interi separati da spazio:
   i valori di $m$ ed $n$

3. si dia avvio al ciclo di gioco, così strutturato:

3.1. se si intende sottoporre un codice di tentativo,
     nella prossima riga di `stdout` si scriva il carattere 'T' seguito da $n$ interi separati da spazi

     se invece si è ora certi di quale sia il codice segreto e si intenda sottometterlo, nella prossima riga di `stdout` si scriva il carattere 'S' seguito da $n$ interi separati da spazi

3.2. nel primo caso si legga da `stdout` la valutazione del codice tentativo:
   due interi $N$ e $B$ separati da spazi: $N=$il numero di pioli neri, $B=$il numero di pioli bianchi.
     nel secondo caso si attenda la conferma od altro feedback.


==Subtask==
Subtask 1: $n=4$, $m=5$, nessuna limitazione sul numero di tentativi
Subtask 2: $n=4$, $m=5$, hai a disposizione al più 10 tentativi
Subtask 3: $n=4$, $m=5$, hai a disposizione al più 6 tentativi
Subtask 4: $n\leq 4$, $m\leq 5$, minimizza il numero di tentativi nel caso peggiore
Subtask 5: $n\leq 4$, $m\leq 5$, minimizza il numero di tentativi nel caso medio, sotto ipotesi di codice random con distribuzione di probabilità uniforme.
Subtask 6: $n\leq 4$, $m\leq 5$, gioco ottimo contro avversario altrettanto ottimo.
Subtask 7: $n=4$, $m=5$, nessuna limitazione sul numero di tentativi
Subtask 8: $n=4$, $m=5$, hai a disposizione al più $mn$ tentativi
Subtask 9: $n=4$, $m=5$, hai a disposizione al più $m+n\log n$ tentativi
 
