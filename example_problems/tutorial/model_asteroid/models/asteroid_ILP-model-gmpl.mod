/*
Problema degli Asteroidi, originalmente introdotto per il corso di Mathematics for Decisions,
rivisto come problema di modellazione matematica.
Questo modello GMPL e' stato creato da Romeo Rizzi (romeo.rizzi@univr.it) a scopi didattici.
*/

param M integer, >= 1;  # Numero di righe del pirellone
param N integer, >= 1;  # Numero di colonne del pirellone

set Rows := 1..M;  # Insieme degli indici di riga
set Cols := 1..N;  # Insieme degli indici di colonna

param ASTEROID{Rows, Cols} binary; # 0 = cella spenta, 1 = accesa.

var AzionareR{Rows} binary; # 0 = non azionare, 1 = azionare l'interruttore.
var AzionareC{Cols} binary; # 0 = non azionare, 1 = azionare l'interruttore.
var Fixer binary; # usata per garantire la feasibility. 0 = feasible, 1 = non feasible.

# Definizione della funzione obiettivo:
minimize numAzioni:
         (M+N)*Fixer + sum{i in Rows} AzionareR[i] + sum{j in Cols} AzionareC[j];

subject to turn_off{(i,j) in {Rows, Cols} : ASTEROID[i,j] = 1}: 
        AzionareR[i] + AzionareC[j] + Fixer = 1;

subject to keep_off{(i,j) in {Rows, Cols} : ASTEROID[i,j] = 0}: 
        AzionareR[i] = AzionareC[j];


# comandi utili per debugging:
#display M;
#display N;
#display Rows;
#display Cols;
#display ASTEROID;
#display numAzioni;

# lanciamo il Solver:
solve;

printf "Fixer = %d ", Fixer;

# printing the solution:
printf "" > "solution.txt";
for {{0}: Fixer == 1}{         # IF condition THEN
   printf "NO SOLUTION" > "solution.txt";
} for {{0}: Fixer != 1} {  # ELSE
   for{i in Rows} {
      printf "%d ", AzionareR[i] >> "solution.txt";
   }
   printf "\n" >> "solution.txt";
   for{j in Cols} {
      printf "%d ", AzionareC[j] >> "solution.txt";
   }
}                             # ENDIF
printf "\n" >> "solution.txt";

