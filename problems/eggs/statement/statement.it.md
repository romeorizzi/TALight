# Uova di Pasqua (eggs)

![image](../figs/eggs.jpeg)

Quest'anno Willy Wonka ha prodotto delle uova di Pasqua speciali, progettate appositamente per essere lanciate dall'ascensore di vetro.
Il lancio può avvenire da uno qualsiasi di $100$ diversi piani, numerati da $1$ a $100$. Sappiamo che le uova presentano tutte lo stesso piano di rottura: se un uovo si rompe quando lanciato da un certo piano allora anche tutte le altre uova si rompono se lanciate da quel piano o da piani superiori. Ma potrebbe anche essere il caso che le uova non si rompano quando lanciate da piano alcuno. 
Willy ci riserva due delle uova della produzione perché noi si stabilisca il minimo piano di rottura delle uova, oppure si stabilisca la loro infrangibilità.

Quale è il minimo numero di lanci che dobbiamo fare per assicurare la risposta corretta? Ossia: quale è il più piccolo numero $m$ tale che esista una strategia che assicura di giungere sempre a conoscere il piano di rottura impiegando al più $m$ lanci?

Più in generale, ti proponiamo di studiare la funzione $m=m(u,n)$ dove $n$ è il numero di piani e $u$ è il numero di uova inizialmente messe a disposizione da Willy.

## Servizi offerti

```
> rtal -a min=m -a n_floors=n -a n_eggs=u connect confirm_min_throws
```
con $m$, $n$ ed $u$ numeri naturali compresi tra $1$ e $100$ (con $u$ di default a $2$ ed $n$ a $100$) ritorna:
  $0$ se $m$ è il valore corretto per il minor numero possibile di lanci che, ove ben spesi, consentano di determinare sempre il piano di rottura.
  $1$ se più di $m$ lanci possono rivelarsi necessari qualunque sia la nostra strategia con cui condurre gli esperimenti.
  $-1$ se anche nel caso peggiore meno di $m$ lanci sono sempre sufficienti a determinare il piano di rottura pur di impiegarli al meglio.


```
> rtal -a n_floors=n -a n_eggs=u opt_move
```
con $n$ ed $u$ numeri naturali compresi tra $1$ e $100$ (con $u$ di default a $2$ ed $n$ a $100$) ritorna un numero che corrisponde ad un piano dal quale non è sbagliato lanciare il primo uovo.

#### Verifica della tabella delle risposte

```
> rtal -a n_floors=n -a n_eggs=u check_table < table.txt
```
con $u$ ed $n$ numeri naturali compresi tra $1$ e $100$ (con $u$ di default a $2$ ed $n$ a $100$) controlla la correttezza della tabella contenuta nel file `table.txt`. La tabella ha $u$ righe ciascuna di $n$ numeri interi separati da spazio.
Nella riga $i$ e colonna $j$ è scritto $m(i,j)$, ossia il più piccolo numero $m$ per cui, quando si parta con $i$ uova su un palazzo di $j$ piani, esista una strategia che consenta di determinare il piano critico impiegando al più $m$ lanci nel caso peggiore.

#### Gioco interattivo

```
> rtal connect play --n_floors=n --n_eggs=u
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
> rtal connect --n_floors=n --n_eggs=u play  -- mybot.py
```
Il bot deve essere un eseguibile coi permessi di esecuzione settati, ma può essere stato scritto in un qualsiasi linguaggio.



#### Gioca tu nel ruolo di Murphy

```
> rtal connect --n_floors=n --n_eggs=u play_murphy
```
Esempio
```
S> 50
L> CRASH! lounches done: 1, eggs left: 1 
S> 25
L> CRASH! lounches done: 1, eggs left: 1
L> ! you are dead. Could be any floor in the range [1,24] and you have no eggs! 
```
