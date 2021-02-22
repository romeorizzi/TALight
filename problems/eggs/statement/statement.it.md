# Uova di Pasqua (eggs)

![image](../figs/eggs.jpeg)

Quest'anno Willy Wonka ha prodotto delle uova di Pasqua speciali, progettate appositamente per essere lanciate dall'ascensore di vetro.
Il lancio può avvenire da uno qualsiasi di $100$ diversi piani, numerati da $1$ a $100$. Sappiamo che le uova presentano tutte lo stesso piano di rottura: se un uovo si rompe quando lanciato da un certo piano allora tutte le altre uova si rompono anche esse se lanciate da quel piano o da piani superiori. 
Willy ci riserva due delle uova della produzione perché noi si stabilisca il minimo piano di rottura delle uova, oppure si stabilisca la loro infrangibilità (potrebbe anche essere il caso che le uova non si rompano qualsiasi sia il piano da cui vengono lanciate).

Quale è il minimo numero di lanci che dobbiamo fare per assicurare la risposta corretta? Ossia: quale è il più piccolo numero $m$ tale che esista una strategia che assicura di giungere sempre a conoscere il piano di rottura impiegando al più $m$ lanci?

Più in generale, ti proponiamo di studiare la funzione $m=m(u,n)$ dove $n$ è il numero di piani e $u$ è il numero di uova inizialmente messe a disposizione da Willy.


## Servizi offerti

```
> rtal connect -a min=m -a n_floors=n -a n_eggs=u eggs confirm_min_throws
```
con $m$, $n$ ed $u$ numeri naturali compresi tra $1$ e $100$ (con $u$ di default a $2$ ed $n$ a $100$) ritorna:
  $0$ se $m$ è il valore corretto per il minor numero possibile di lanci che, ove ben spesi, consentano di determinare sempre il piano di rottura.
  $1$ se più di $m$ lanci possono rivelarsi necessari qualunque sia la nostra strategia con cui condurre gli esperimenti.
  $-1$ se anche nel caso peggiore meno di $m$ lanci sono sempre sufficienti a determinare il piano di rottura pur di impiegarli al meglio.


```
> rtal connect -a n_floors=n -a n_eggs=u eggs opt_move
```
con $n$ ed $u$ numeri naturali compresi tra $1$ e $100$ (con $u$ di default a $2$ ed $n$ a $100$) ritorna un numero che corrisponde ad un piano dal quale non è sbagliato lanciare il primo uovo.

#### Verifica della tabella delle risposte

In questo servizio veniamo a scoprire la nostra priam TALutil.
Se lanciamo il segunte servizio:

```
> rtal connect eggs check_table
```
ci viene chiesto di inserire una tabella rettangolare di numeri naturali. Possiamo scegliere noi il numero di righe $U$ (quando non vogliamo introdurre ulteriori righe inseriamo la stringa "#end" per chiudere la fase di immissione) ed il numero di colonne $N$ (lo stabilisce la prima riga). Il servizio controlla che la tabella ricomprenda precisamente i numeri $m=m(u,n)$ con $u$ ed $n$ numeri naturali compresi tra $1$ e $100$.
Se la tabella è grande potrete procedere di Ctrl-C da file e Ctrl-Shift-V sul terminale (sul terminale le combinazioni per il copy&paste sono  e Ctrl-Shift-C e Ctrl-Shift-V).
Il servizio di default richiede che nella tabella i numeri siano dgli interi separati da spazi. Ma potete impostare altri separatori (anche stringhe) avvalendovi dei paramtri del servizio.
Potreste quindi mandare la tabella scritta in formato .csv.
Nella riga $i$ e colonna $j$ della tablla è scritto $m(i,j)$, ossia il più piccolo numero $m$ per cui, quando si parta con $i$ uova su un palazzo di $j$ piani, esista una strategia che consenta di determinare il piano critico impiegando al più $m$ lanci nel caso peggiore.

Potete prima testare il servizio con tabelle molto piccle che potet immettere a mano, e poi gestire tabelle più grandi con (Shift)-Ctrl-C Shift-Ctrl-V. 
Ma quando $U$ ed $N$ dovessro essere grandi anche il copia incolla non sarà adatto.
Supponiamo che la tabella sia contenuta nel file `bots/python/table_2_100.txt`. Possiamo allora inviarlo al servizio con l'aiuto della TALutil `TA_send_txt_file` come segue:

```bash
rtal connect -e -a separator=, eggs check_table -- ~/TAlight/TAL_utils/TA_send_txt_file.py table_2_100.csv
```

Un altro servizio che, in qusto problema, sfrutta questa stssa TALutil è:


```bash
rtal connect -e eggs eval_strategy_table -- ~/TAlight/TAL_utils/TA_send_txt_file.py strategy_table.csv
```

oppure

```bash
rtal connect -e -aseparator=, eggs eval_strategy_table -- ~/TAlight/TAL_utils/TA_send_txt_file.py strategy_table.csv
```


#### Gioco interattivo

```
> rtal connect -a n_floors=n -a n_eggs=u eggs play
```
con $n$ ed $u$ numeri naturali compresi tra $1$ e $100$ (con $u$ di default a $2$ ed $n$ a $100$) avvia una possibile storia che si svolge secondo il protocollo così esemplificato (negli esempi di interazione, le righe che iniziano con "S> " sono quelle inviate dal server, mentre quelle inviate dal tuo dispositivo locale sono prefissate con "L> "):

Esempio 1 (`rtal connect play`)

```
L> 50
S> CRASH! Now you are left with 1 egg! 
L> 25
S> CRASH! Now you are left with 0 eggs! 
L> 12
S> !Sorry, you do not have any eggs left! 
```

Esempio 2 (`rtal connect -a n_floors=2 -a n_eggs=1 play`)
```
L> 1
S> BOUNCH! You still have 1 egg left! 
L> 2
S> CRASH! Now you are left with 0 eggs! 
L> answ 2
S> !Correct! The critical floor is 2. This time it took you 3 lounches to find it out. 
```

Esempio di risposta sbagliata (`rtal connect -a n_floors=2 -a n_eggs=1 play`)
```
L> 1
S> BOUNCH! You still have 1 egg left! 
L> 2
S> CRASH! Now you are left with 0 eggs! 
L> answ 1
S> !Wrong answer! 
```

Esempio con nessun piano di rottura (`rtal connect -a n_floors=2 -a n_eggs=1 play`)
```
L> 1
S> BOUNCH! You still have 1 egg left! 
L> 2
S> BOUNCH! You still have 1 egg left! 
L> answ 3
S> !Correct! The critical floor is 2. This time it took you 3 lounches to find it out. 
```

Per inserire un tuo bot che giochi al posto tuo la sintassi corretta è:

```
> rtal connect eggs --n_floors=n --n_eggs=u play  -- mybot.py
```
Il bot deve essere un eseguibile coi permessi di esecuzione settati, ma può essere stato scritto in un qualsiasi linguaggio.


## Adds up all'esercizio

1. Come cambiano le cose se ciò che vogliamo minimizzare è il numero atteso di lanci assumendo che ogni possibili verità sia equiprobabile?

 

#### Gioca tu nel ruolo di Natura

```
> rtal connect -a n_floors=100 -a n_eggs=3 eggs play_nature
```
Esempio
```
S> 50
L> CRASH! lounches done: 1, eggs left: 1 
S> 25
L> CRASH! lounches done: 1, eggs left: 1
L> ! you are dead. Could be any floor in the range [1,24] and you have no eggs! 
```
