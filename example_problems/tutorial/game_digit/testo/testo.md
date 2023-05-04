# Giochiamo a Sottrai 09 (gioco\_cifre)

Martina e Luigi si sfidano al gioco "Sottrai la cifra".  
Il gioco è così descritto:
- Inizialmente viene generato casualmente un numero intero positivo $N$. Esso rappresenta il numero con cui inzierà la partita.
- In ogni turno il giocatore sceglie una cifra del numero attuale diversa da $0$ e ne sottrae il valore dal numero stesso.
- Ha l'ultima parola e vince il giocatore che con la propria mossa dovesse riuscire a generare il numero $0$.

### Esempio

Ipotizziamo che dopo un numero finito di turni il numero sia 7083. Le __uniche__ mosse valide sono:
- Sottraggo 3, ottenendo 7080 
- Sottraggo 8, ottenendo 7075
- Sottraggo 7, ottenendo 7076

Non potrei quindi sottrarre un 2 poichè non compare tra le cifre di 7083.

Martina inizia sempre per prima.
Si vuole sapere se Martina, giocando ottimamente, potrà vincere.

## Input

Da `stdin`.
Un unico numero intero $N$, che indica il numero iniziale.

## Output

Su `stdout` scrivi $1$ se Martina può vincere, $0$ altrimenti.
Se hai risposto che Martina può vincere,
nella seconda riga di `stdout` devi indicare il valore di una cifra che Martina possa andare a sottrarre dal numero senza compromettere il suo vantaggio.


## Assunzioni
- $1 \leq N \leq 10\,000\,000$

## Esempi

| input from stdin | &nbsp;&nbsp;&nbsp;&nbsp; | output to stdout |
| ---------------- | ------------------------ | ---------------- |
| 16               | &nbsp;                   | 1                |
|                  | &nbsp;                   | 6                |

## Subtask

- **Subtask 1 [ 0 punti]**: il tuo programma deve risolvere correttamente i casi d'esempio qui sopra.
- **Subtask 2 [20 punti]**: $N \leq 10$
- **Subtask 3 [20 punti]**: $N \leq 100$
- **Subtask 4 [20 punti]**: $N \leq 1000$
- **Subtask 5 [20 punti]**: $N \leq 100\,000$
- **Subtask 6 [20 punti]**: $N \leq 10\,000\,000$

Footer
