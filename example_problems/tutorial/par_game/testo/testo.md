# Giochiamo a Rimuovi Parentesi (gioco\_parentesi)

La seguente è una _formula ben formata di parentesi (FBF)_:
```
(()(()()))((()))
```
ossia una qualsiasi stringa sull'alfabeto $\{'(',')'\}$ ottenibile partendo dal simbolo non-terminale $S$, previa applicazione delle regole:
1. $S \mapsto \varepsilon$
2. $S \mapsto (S)S$
dove al solito $\varepsilon$ indica la stringa vuota.
Si noti che in ogni FBF il numero $N$ di parentesi aperte eguaglia il numero di quelle chiuse e di fatto esse nascono a coppie ad ogni applicazione della regola~2. Di fatto una stringa $f$ su $\{'(',')'\}$ è una FBF $f$ se e solo se esiste una corrispondenza biunivoca tra le parentesi aperte e quelle chiuse tale che per ogni coppia $f_i='('$ e $f_j=')'$ che si corrispondono allora $i<j$
ed è una FBF la stringa ottenuta da $f$ rimuoviamo tutto quanto ricompreso tra $f_i$ ed $f_j$, inclusi $f_i$ ed $f_j$.
Questa operazione è chiamata _rimozione di una sotto-FBF_ e consegna sempre una nuova FBF con un numero strettamente inferiore di parentesi.


Per giocare a _Rimuovi Parentesi_, Jake e Finn chiedono a Bimo di generare per loro una FBF,
e poi, a turno, con Jake che parte, effettuano la seguente mossa:

> scelta e rimozione di una sotto-FBF della FBF corrente
Quando la FBF corrente è vuota, si è perso non potendo più muovere e dovendo abbandonare quindi questa avventura.



## Input:

Da `stdin`. La prima riga contiene un numero intero $N$, che rappresenta la lunghezza della stringa $f$ generata dall'amico Bimo.  
La seconda riga contiene esclusivamente tale FBF, seguita dai caratteri per l'andata a capo e/o per la fine del file.

## Output:

Su `stdout` si scriva$~1$ se Jake può vincere, $0~$altrimenti.
Se Jake può vincere,
nella seconda riga di `stdout` vanno inoltre riportati, nell'ordine,
due numeri $i$ e $j$ con $0\leq i < j < N$ tali che $f_i$ ed $f_j$ si corrispondano
e la rimozione da $f$ della sotto-FBF ricompreso tra $f_i$ ed $f_j$ (inclusi) consegni a Finn una posizione "chi tocca perde".

## Esempi

| input from `stdin` | &nbsp;&nbsp;&nbsp;&nbsp; | output to `stdout` |
| ------------------ | ------------------------ | ------------------ |
| 2<br>()            | &nbsp;                   | 1<br>0 1           |
| &nbsp;             | &nbsp;                   | &nbsp;             |
| 4<br>()()          | &nbsp;                   | 0                  |
| &nbsp;             | &nbsp;                   | &nbsp;             |
| 4<br>(())          | &nbsp;                   | 1 0 3              |
| &nbsp;             | &nbsp;                   | &nbsp;             |
| 100<br>((()()())((())())(()())((())())(()()))((()()()())()(()))((()())(()()())(()())(())()())(()())(()()())        | &nbsp;                 | 1<br>1 8            |

## Assunzioni:
- $2 \leq N \leq 1\,000\,000$
- $N$ pari.

### Subtask
- **Subtask  1 [ 1 punto]**: risolvere correttamente i casi d'esempio quì sopra nel testo.
- **Subtask  2 [ 4 punti]**: $f$ della forma $(^n)^n$, dove $n = N/2$. Ossia $f=\underbrace{((\ldots((}_{n}\,\underbrace{))\ldots))}_{n}$.
---
- **Subtask  3 [ 5 punti]**: $f$ è concatenazione di stringhe tutte della forma $(^n)^n$, $N \leq 20$.
- **Subtask  4 [ 5 punti]**: $f$ è concatenazione di stringhe tutte della forma $(^n)^n$, $N \leq 50$.
- **Subtask  5 [ 5 punti]**: $f$ è concatenazione di stringhe tutte della forma $(^n)^n$, $N \leq 100$.
- **Subtask  6 [ 5 punti]**: $f$ è concatenazione di stringhe tutte della forma $(^n)^n$, $N \leq 1000$.
- **Subtask  7 [ 5 punti]**: $f$ è concatenazione di stringhe tutte della forma $(^n)^n$.
---
- **Subtask  8 [15 punti]**: $N \leq 20$.
- **Subtask  9 [20 punti]**: $N \leq 50$.
- **Subtask 10 [20 punti]**: $N \leq 1000$.
- **Subtask 11 [15 punti]**: nessuna assunzione particolare.
