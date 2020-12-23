# morra

![image](../figs/Boys_playing_Morra_Old_postcard.jpg)

Sia $G$ un insieme di giocatori $g_1, g_2, \ldots, g_n$. In un giro di morra tra questi giocatori essi si coordinano affinchè, il più simultaneamente possibile, ciascun giocatore $i$ generi ed invii a tutti gli altri due numeri naturali $m_i\in [0,4]$ ed $s_i\in [0,4n]$.
A seguito di un tale giro di morra viene accreditato un punto a ciascun giocatore $i$ per cui risulti $s_i = \sum_{i=1}^n m_i$.   

Cominciamo con l'implementare questo meccanismo fondamentale per il caso di due giocatori ($n=2$), uno è il server (S) e l'altro il dispositivo in locale (L) di un singolo studente. Essi comunicano su un canale bidirezionale secondo il seguente protocollo.
Per l'implemntazion del meccanismo ci avverremo di una hash function $h$ di cui forniamo lo pseudocodice oltre che implementazioni nei linguaggi più diffusi (se non c'è nel tuo linguaggio puoi codificarla traducendo lo pseutocodice e se funziona puoi contibuire con una pull request). Quando $s$ è una stringa in $\{0,1,2,3,4,5,6,7,8,9\}^{64}$ allora $h(s)$ è la codifica decimale di un numero naturale di al più $20$ cifre.

Indipendentemente dal fatto che siano inviate da S oppure da L, le righe che iniziano col carattere '!' comunicano la chiusura del canale, la riga può comunque proseguire con un commento.
Le righe che iniziano col carattere cancelletto '#' sono commenti, e possono essere inviati in modo del tutto asincrono.
Per proporre un giro di morra S invia una riga col solo carattere '?'.
In seguito, senza un ordine stabilito, ciascun X in {S,L} genera una stringa random di $60$ caratteri, e invia sul canale l'hash di un messaggio $m_X$ che inizia con le due cifre $m\in [0,4]$ ed $s\in [0,8]$, ciascuna seguita da uno spazio, cui segue la stringa random di 60 caratteri generata al momento.
Dopo aver ricevuto l'hash prodotto dall'avversario,
ciascun giocatore espone in chiaro il proprio messaggio $m_X$ di cui aveva precedentemente inviato l'hash.
In questo modo è possibile verificare, da parte di entrambi i giocatori, che le giocate di morra sono state una indipendente dall'altra.
Viene accreditato un punto a quel giocatore che ha offerto un $s$ pari alla somma dei due $m$ prodotti, uno da sè stesso e l'altro dall'avversario.   
Oltre a proporre un giro di morra il server può offrire il conteggio attuale dei punti, in questo caso invia una riga che invece che iniziare col carattere '?' inizia col carattere 'p' ed ha il formato:
```
p punti_di_S punti_di_L   
```

Esempio di interazione (nell'esempio, le righe che iniziano con "S> " sono quelle inviate dal server, mentre quelle inviate dal tuo dispositivo locale sono prefissate con "L> "):
```
S> # buongiorno!
S> ?
S> >h("4 7 867398183749348592620358775940598729403682050358306360870255")
L> >h("4 8 123456789012345678901234567890123456789012345678901234567890")
S> # questo giro lo hai vinto tù. 
S> ! :)
```

Servizi offerti:

```
> TAlight ...

```

Prego dettagliare i servizi offerti e la modalità per richiederli ...