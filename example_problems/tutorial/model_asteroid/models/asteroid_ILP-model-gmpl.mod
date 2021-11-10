/*
Problema degli Asteroidi, originalmente introdotto per il corso di Mathematics for Decisions.
Questo modello GMPL e' stato creato da Romeo Rizzi (romeo.rizzi@univr.it) a scopi didattici.
*/

param M integer, >= 1;  # Numero di righe del asteroid
param N integer, >= 1;  # Numero di colonne del asteroid

set Rows := 1..M;  # Insieme degli indici di riga
set Cols := 1..N;  # Insieme degli indici di colonna

param ASTEROID{Rows, Cols} binary; # 0 = non c'è asteroide, 1 = la cella ospita un asteroide.

var LaserR{Rows} binary; # 0 = non sparare, 1 = sparare il laser.
var LaserC{Cols} binary; # 0 = non sparare, 1 = sparare il laser.

# Definizione della funzione obiettivo:
minimize numSpari:
         sum{i in Rows} LaserR[i] + sum{j in Cols} LaserC[j];

subject to destroy_asteroid{(i,j) in {Rows, Cols} : ASTEROID[i,j] = 1}: 
        LaserR[i] + LaserC[j] >= 1;


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
   printf "%d ", LaserR[i] >> "solution.txt";
}
printf "\n" >> "solution.txt";
for{j in Cols} {
   printf "%d ", LaserC[j] >> "solution.txt";
}
printf "\n" >> "solution.txt";

