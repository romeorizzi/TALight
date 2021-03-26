# Indovina il codice segreto! (mastermind)

Immaginati nelle vesti di un _decodificatore_.
Il tuo avversario, un _codificatore_, ha scritto un codice segreto di quattro cifre, ognuna delle quali può assumere un valore tra $0$ e $5$.

Per vincere la sfida, devi scrivere una procedura che individui il suo codice segreto, effettuando il minor numero di tentativi.
Ad ogni tentativo riceverai un feedback che ti consentirà di ricevere informazioni sul codice segreto impostato dall'avversario.
Una prima funzione di valutazione ritorna tanti pioli neri quante sono le posizioni in cui ìl codice segreto e quello da tè sottomesso presentano lo stesso colore. Una seconda funzione (chiamare la quale non viene conteggiato come ulteriore tentativo se la chiami sullo stesso codice che hai appena passato alla funzione sopra) ti ritorna tanti pioli bianchi quanti sono gli ulteriori colori indovinati, ma collocati fuori posto.

Le regole ti verranno forse più chiare dopo qualche partita giocata online meglio ancora tramite TALight stesso (usa 6 colori su 4 posizioni, possibilmente ripetuti):

[un player esterno, online](http://www.webgamesonline.com/mastermind/index.php)

## Competenza 1 - saper punteggiare correttamente un tentativo

Assicuriamoci innanzitutto di aver compreso le regole del gioco:
ove tu conoscessi il codice segreto e ti venisse esibito un tentativo, saprsti valutarlo restituendo il numero corretto di pioli neri e bianchi?

Si assuma che il codice sia di $n$ cifre, dove ogni cifra è un numero da $1$ a $m$.

I seguenti subtask e servizi, oggetto di feedback, potranno confermarti di aver compreso correttamente le regole del gioco.

* [servizio tell_score:] puoi sottomettere una coppia di codici (quello segreto e un tentativo), per richiedere quale sia la valutazione corretta per quella coppia.

```t
rtal connect mastermind -a secret_code="2 2 1 4" -a probing_code="2 3 1 3" tell_score 
```

* [servizio check_scoring_competence:] mira a convalidare la tua comptnza nel punteggiare un codice tentativo. Ti viene fornita una serie di coppie di codici (segreto e tentativo) e per ciascuna di esse esprimi la tua puntggiatura. Ti verrà segnalato ogni errore riscontrato.

```t
rtal connect mastermind -a num_questions=50 -a num_pegs=5 -a num_colors=8 check_scoring_competence
```
Oltre che poter sprimere tu stesso la competnza, a questo servizio potrai sottomettere un tuo bot che ti rapprsenti:

```t
rtal connect mastermind -a num_questions=50 -a num_pegs=5 -a num_colors=8 check_scoring_competence -- python mybot.py
```

Il tuo file eseguibile sarà un programma che gioca per tè oppure un applt attraverso cui potrai giocare. In entrambi i casi dovrà rispettare il seguente protocollo di comunicazione:

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


## Competenza 2 - saper ricostruire il codice segreto

In questo caso il nostro servizio principale (e più atteso) si baserà su un'interazione tra tè stesso od un tuo programma che esguirai in locale (un applet entro il quale giocare tu oppure un programma che giochi per tè) ed un nostro codice sul server che giocherà nel ruolo del detentore del segreto.
Una volta lanciato il comando:

```t
TALight ask --problem=mastermind --goal=2 --subtask=SUBTASK_NUMBER  tuo_file_eseguibile 
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


==Goals==
Goal 1: $n=4$, $m=5$, nessuna limitazione sul numero di tentativi
Goal 2: $n=4$, $m=5$, hai a disposizione al più 10 tentativi
Goal 3: $n=4$, $m=5$, hai a disposizione al più 6 tentativi
Goal 4: $n\leq 4$, $m\leq 5$, minimizza il numero di tentativi nel caso peggiore
Goal 5: $n\leq 4$, $m\leq 5$, minimizza il numero di tentativi nel caso medio, sotto ipotesi di codice random con distribuzione di probabilità uniforme.
Goal 6: $n\leq 4$, $m\leq 5$, gioco ottimo contro avversario altrettanto ottimo.
Goal 7: $n=4$, $m=5$, nessuna limitazione sul numero di tentativi
Goal 8: $n=4$, $m=5$, hai a disposizione al più $mn$ tentativi
Goal 9: $n=4$, $m=5$, hai a disposizione al più $m+n\log n$ tentativi
 
