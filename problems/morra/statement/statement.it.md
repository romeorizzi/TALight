# morra

![image](../figs/Boys_playing_Morra_Old_postcard.jpg)

Sia $G$ un insieme di giocatori $g_1, g_2, \ldots, g_n$. In un giro di morra tra questi giocatori essi si coordinano affinchè, il più simultaneamente possibile, ciascun giocatore $i$ generi ed invii a tutti gli altri due numeri naturali $m_i\in [0,4]$ ed $s_i\in [0,4n]$.
A seguito di un tale giro di morra viene accreditato un punto a ciascun giocatore $i$ per cui risulti $s_i = \sum_{i=1}^n m_i$.

Cominciamo con l'implementare questo meccanismo fondamentale per il caso di due giocatori ($n=2$), uno è il server del servizio (S) realizzato dal problem maker (e potrà girare nel cloud oppure sulla tua macchina), mentre l'altro (L) opera sempre in locale sulla macchina del problem-solver e potrà essere un umano (il problem-solver/giocatore/studente stesso) oppure il bot da lui realizzato per giocare la partita in sua vece. Gli agenti S ed L comunicano su un [canale bidirezionale TAlight](https://github.com/romeorizzi/TAlight/wiki) attraverso il protocollo che ci limitiamo ad abbozzare di seguito (i dettagli sono largamente inessenziali e possono trovare precisazione ultima sperimentando direttamente i servizi interattivi [TAalight](https://github.com/romeorizzi/TAlight) offerti dal problema):
> Per realizzare il requisito fondamentale di simultaneità, senza il quale verrebbe meno lo stesso senso del gioco, il protocollo attua un meccanismo secondo il quale ogni giocatore imbusta la sua giocata e la comunica in forma criptata. Solo quando ogni giocatore ha ricevuto le buste degli altri $n-1$ giocatori distribuisce il segreto che consente la decriptazione.

Il framework di criptazione/decriptazione deve ovviamente essere condiviso tra tutti i giocatori. Chi volesse poggiare su tecnologia reale, od operasse da linguaggi come `python` o `java` che offrono conveniente supporto per queste cose, potrà optare per l'impiego di SHA-1. Per chi operasse da altri linguaggi dove l'integrazione di queste tecnologie richiedesse delle installazioni che non si desideri affrontare, proponiamo noi una hash function $h$ di cui forniamo lo pseudo-codice oltre che delle implementazioni nei linguaggi più diffusi.
Di $h$ dovrebbe bastarti sapere che quando $s$ è una stringa in $\{0,1,2,3,4,5,6,7,8,9\}^{64}$ allora $h(s)$ è la codifica decimale di un numero naturale di al più $20$ cifre.

:stuck_out_tongue_winking_eye: *Nota:* se l'implementazione nel tuo linguaggio non è attualmente presente nel [repo pubblico](https://github.com/romeorizzi/TAlight) puoi codificarla traducendo lo pseudo-codice fornito. Verificato che funziona correttamente tramite servizio apposito, puoi contribuirla al repo con una pull request. Per altro questo è lo spirito di `collaborative learning+teaching+making` che con `TAlight` ci prefiggiamo di portare nelle classi ed in altri contesti di approfondimento o ricerca.


Indipendentemente dal fatto che siano inviate dal server (S) al dispositivo in locale (L) oppure viceversa, le righe che iniziano col carattere cancelletto '#' sono commenti, e possono essere inviate in modo del tutto asincrono.
Quando il server invia una riga che inizia col carattere '!' comunica la chiusura del canale per terminare un'interazione che si è svolta nel rispetto del protocollo sotteso, la riga può proseguire con un commento.
L'interazione può essere altresì interrotta da S quando L non rispetta il protocollo o le tempistiche, o in caso di problemi di connessione. Se riscontrate comportamenti che si discostano da questi segnalateceli opportunamente documentati e circostanziati.
Voi problem solvers, o il bot che dovesse agire in vostra vece, sul canale siete ovviamente liberi di sperimentare, il che include la possibilità di commettere errori. Se l'errore comporta una violazione del protocollo il server chiuderà il canale senza garantire ulteriore feedback. Lo saprete perché l'ultima riga ricevuta da S non inizia in '!'.

Per proporre un giro di morra S invia una riga col solo carattere '?'.
In seguito, senza un ordine stabilito, ciascun X in {S,L} genera una stringa random di $60$ caratteri, e invia sul canale l'hash di un messaggio $m_X$ che inizia con le due cifre $m\in [0,4]$ ed $s\in [0,8]$, ciascuna seguita da uno spazio, cui segue la stringa random di 60 caratteri generata al momento.
Dopo aver ricevuto l'hash prodotto dall'avversario, ciascun giocatore espone in chiaro il proprio messaggio $m_X$ di cui aveva precedentemente inviato l'hash. In questo modo è possibile verificare, da parte di entrambi i giocatori, che le giocate di morra sono state una indipendente dall'altra.
Viene accreditato un punto a quel giocatore che ha offerto un $s$ pari alla somma dei due $m$ prodotti, uno da sè stesso e l'altro dall'avversario.


## Esempio di interazione

Nell'esempio, le righe che iniziano con "S> " sono quelle inviate dal server:

```t
S> # buongiorno!
S> ?
S> h("4_7_867398183749348592620358775940598729403682050358306360870255")
L> h("4_8_123456789012345678901234567890123456789012345678901234567890")
S> 4_7_867398183749348592620358775940598729403682050358306360870255
L> 4_8_123456789012345678901234567890123456789012345678901234567890
S> # questo giro lo hai vinto tu. 
S> # punti miei = 0, punti tuoi = 1, mani giocate = 1 
S> ?
S> h("3_6_398183749348592620358775940598729403682050358306360870255421")
L> h("2_3_123456789012345678901234567890123456789012345678901234567890")
L> 2_3_123456789012345678901234567890123456789012345678901234567890
S> 3_6_398183749348592620358775940598729403682050358306360870255421
S> # punti miei = 0, punti tuoi = 1, mani giocate = 2 
S> ! :)
```

## Servizi offerti:

```t
> TAlight connect -a num_rounds=10 morra player
```
Per farsi una partitina di 10 raggi. Per meglio conoscere i parametri di questo servizio:  
```t
rtal list -v morra 
```
Per scoprire come far giocare un bot al proprio posto:
```t
rtal connect --help
```
Per verificare se la propria codifica delle funzione di hash $f$ funziona correttamente:

```t
> TAlight connect -a 4_8_123456789012345678901234567890123456789012345678901234567890 morra compute_hash
```
oppure, magari tramite un bot, avvalersi del servizio:
```t
> TAlight connect -a 4_8_123456789012345678901234567890123456789012345678901234567890 -a 2750235103 morra verify_hash
```
