/*
Problema degli Asteroidi, originalmente introdotto per il corso di Mathematics for Decisions,
rivisto come problema di modellazione matematica.
Questo modello GMPL e' stato creato da Romeo Rizzi (romeo.rizzi@univr.it) a scopi didattici.
*/

param M integer, >= 1;  # Numero di righe del asteroid
param N integer, >= 1;  # Numero di colonne del asteroid

set Rows := 1..M;  # Insieme degli indici di riga
set Cols := 1..N;  # Insieme degli indici di colonna

param ASTEROID{Rows, Cols} binary; # 0 = cella spenta, 1 = accesa.

var AzionareR{Rows} binary; # 0 = non azionare, 1 = azionare l'interruttore.
var AzionareC{Cols} binary; # 0 = non azionare, 1 = azionare l'interruttore.

# Definizione della funzione obiettivo:
minimize numAzioni:
         sum{i in Rows} AzionareR[i] + sum{j in Cols} AzionareC[j];

subject to destroy_asteroid{(i,j) in {Rows, Cols} : ASTEROID[i,j] = 1}: 
        AzionareR[i] + AzionareC[j] >= 1;


# comandi utili per debugging:
#display M;
#display N;
#display Rows;
#display Cols;
#display ASTEROID;
#display numAzioni;

# lanciamo il Solver:
solve;

# printing the solution:
printf "" > "solution.txt";
for{i in Rows} {
   printf "%d ", AzionareR[i] >> "solution.txt";
}
printf "\n" >> "solution.txt";
for{j in Cols} {
   printf "%d ", AzionareC[j] >> "solution.txt";
}
printf "\n" >> "solution.txt";

