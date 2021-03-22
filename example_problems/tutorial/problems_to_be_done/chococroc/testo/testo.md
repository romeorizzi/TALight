# Due amici ed una barretta di cioccolato (chococroc)
## liberamente preso dalle iOi 2005 (Polonia)

Questo problema propone di analizzare il seguente gioco a due giocatori.  

La Pimpa ed il suo amico Armando sono andati a scalare la cima di una montagna.
Si sono portati dietro Maria, una tavoletta di cioccolato di $m \times n$ quadretti (Luca, Gianni, Michele, ... ).
All'inizio della scalata Maria è nello zaino di Pimpa e le racconta una storia.
Ad ogni momento della scalata,
chi dei due amici dovesse avere Maria nel proprio zaino, può effettuare la seguente mossa:

> *spezza la tavoletta in due, lungo uno dei due lati a scelta, mangia il pezzo più piccolo (o quantomeno non il più grade dei due), e ripone il pezzo rimanente di Maria nella tasca dietro dello zaino del compagno di scalata.*

La regola di cortesia vuole che chi si ritrova con un solo quadratino cade in imbarazzo, non sa più cosa fare (anche perchè Maria non ha ancora finito di raccontare la sua storia), e reputa pertanto di avere perso una sorta di gioco da sempre in corso tra i due amici.

Nella sua storia Maria offriva la seguente formalizzazione del problema: ogni singola mossa può trasfore una coppia ordinata di numeri naturali $(m,n)$ in una coppia $(m',n)$ con $m'\geq m/2$
oppure in una coppia $(m,n')$ con $n'\geq n/2$.
Ma se $m=n=1$ mica puoi mangiarmi tutta, no?

## Input:

Da stdin.
Il primo numero (0 o 1) dice se devi solo determinare chi vince (1 o 2) oppure anche la mossa vincente.

Poi, nella seconda e terza riga, due stringhe di cifre (la prima diversa da zero) che codificano m ed n in decimale.

## Output:

Scrivere su stdout:  
- Nella prima riga metti 1 se vince la Pimpa (che farà la prima mossa), 2 se vince Armando.
- Se vince la Pimpa e in input veniva richiesta anche la mossa vincente, stampare nelle successive due righe le dimensioni del pezzo di cioccolata che viene passato ad Armando.

## Assunzioni:

- $m, n \geq 1$
- in tutte le istanze sia $m$ che $n$ trovano piena rappresentazione entro un normale `int32`

## Esempi

| input from stdin | &nbsp;&nbsp;&nbsp;&nbsp; | output to stdout |
| ---------------- | ------------------------ | ---------------- |
| 0<br>10<br>10    | &nbsp;                   | 2                |
| &nbsp;           | &nbsp;                   | &nbsp;           |
| 1<br>11<br>10    | &nbsp;                   | 1<br>10<br>10    |
| &nbsp;           | &nbsp;                   | &nbsp;           |
| 1<br>10<br>10    | &nbsp;                   | 2                |





### Subtask
- **Subtask 1 [ 0 punti]**: il tuo programma deve risolvere correttamente i casi d'esempio qui sopra.
- **Subtask 2 [15 punti]**: determinare correttamente chi vince, va bene anche se in tempo esponenziale in $m$ ed $n$.
- **Subtask 3 [15 punti]**: come sopra, ma in tempo $O(nm)$, ossia in tempo pseudo-polinomiale, (esponenziale nella lunghezza del binary encoding di $m$ ed $n$, puoi quindi esplorare/etichettare l'intero grafo delle configurazioni).
- **Subtask 4 [20 punti]**: come sopra, ma in tempo fortemente polinomiale.
- **Subtask 5 [15 punti]**: in configurazioni vincenti, dare la mossa corretta, va bene anche se in tempo esponenziale in $m$ ed $n$.
- **Subtask 6 [15 punti]**: come sopra, ma in tempo $O(nm)$, ossia in tempo pseudo-polinomiale, (esponenziale nella lunghezza del binary encoding di $m$ ed $n$, puoi quindi esplorare/etichettare l'intero grafo delle configurazioni).
- **Subtask 7 [20 punti]**: come sopra, ma in tempo fortemente polinomiale.

