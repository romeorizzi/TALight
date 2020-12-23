# Uova di Pasqua (uova)

![image](../figs/eggs.jpeg)

Ogni anno Willy Wonka produce delle uova di Pasqua da lacio dall'ascnsore di vetro.
Il lancio può avvenire da uno qualsiasi di 100 diversi livelli. Le uova di una stessa annata sono tutte uguali, nel senso che per tutte il minimo livello di rottura è lo stesso. Le uova potrebbero non rompersi quando lanciata da livello alcuno, ma, se si rompono da un crto livello, allora si rompono anche quando lanciate dai livelli supriori. 
Ogni anno Willy ci riserva due delle uova della produzione perchè noi si stabilisca il minimo piano di rottura, o si stabilisca la loro indistruttibilità.

Quale è il minimo numero di lanci che dobbiamo fare per assicurare la risposta corretta? Ossia: quale è il più piccolo numero $m$ tale che esista una strategia che assicura di giungere sempre a conoscere il piano di rottura impigando al più $m$ lanci? 

##Servizi offerti:

```
> TAlight confirm_min_lanci --min=m --n_piani=n --n_uova=u
```
con n, m ed u numeri naturali compresi tra 1 e 100 (con u di default a 2 ed n a 100) ritorna una stringa in {"SI", "SERVONO PIU' LANCI", "BASTANO MENO LANCI"}.

```
> TAlight opt_move --n_piani=n --n_uova=u
```
con n ed u numeri naturali compresi tra 1 e 100 (con u di default a 2 ed n a 100) risponde un piano da cui non è sbagliato lanciare il primo uovo.

#### Verifica della tabella delle risposte

```
> TAlight check_table --n_piani=n --n_uova=u  table.txt
```
con n ed u numeri naturali compresi tra 0 e 100 (con u di default a 2 ed n a 100) controlla la correttezza della tabella contenuta nel file `table.txt`. La tabella ha $u$ righe ciascuna di $n$ numeri interi separati da spazio.
Nella riga $i$ e colonna $j$ è scritto il minimo numero di lanci eseguiti nel caso peggiore da una strategia ottima, quando si parta con $i$ uova su un palazzo di $j$ piani.

#### Gioco interattivo

```
> TAlight connectexe mangage.py --n_piani=n --n_uova=u
```
con n ed u numeri naturali compresi tra 0 e 100 (con u di default a 2 ed n a 100) avvia una possibile storia che si svolge secondo il seguente protocollo:


Esempio di interazione (nell'esempio, le righe che iniziano con "S> " sono quelle inviate dal server, mentre quelle inviate dal tuo dispositivo locale sono prefissate con "L> "):

```
L> 50
S> CRASH! Now you are left with 1 egg! 
L> 25
S> CRASH! Now you are left with 0 eggs! 
L> 12
S> !Sorry, you do not have any eggs left! 
```

Esempio di interazione con 2 piani e 1 uovo
```
L> 1
S> BOUNCH! You still have 1 egg left! 
L> 2
S> CRASH! Now you are left with 0 eggs! 
L> answ 2
S> !Correct! The critical floor is 2. This time it took you 3 lounches to find it out. 
```

Esempio di risposta sbagliata (interazione con 2 piani e 1 uovo)
```
L> 1
S> BOUNCH! You still have 1 egg left! 
L> 2
S> CRASH! Now you are left with 0 eggs! 
L> answ 1
S> !Wrong answer! 
```

Esempio con nessun piano di rottura (interazione con 2 piani e 1 uovo)
```
L> 1
S> BOUNCH! You still have 1 egg left! 
L> 2
S> BOUNCH! You still have 1 egg left! 
L> answ 3
S> !Correct! The critical floor is 2. This time it took you 3 lounches to find it out. 
```

#### Gioca tu nel ruolo di Murphy

```
> TAlight connectexe murphy.py --n_piani=n --n_uova=u
```
Esempio
```
S> 50
L> CRASH! lounches done: 1, eggs left: 1 
S> 25
L> CRASH! lounches done: 1, eggs left: 1
L> ! you are dead. Could be any floor in the range [1,24] and you have no eggs! 
```
