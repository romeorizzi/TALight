/*
Problema di Pirellone, originalmente della fase nazionale 2005 delle OII,
rivisto come problema di modellazione matematica.
Questo modello GMPL e' stato creato da Romeo Rizzi (romeo.rizzi@univr.it) a scopi didattici.
*/

param M integer, >= 1;  # Numero di righe del pirellone
param N integer, >= 1;  # Numero di colonne del pirellone

set Rows := 1..M;  # Insieme degli indici di riga
set Cols := 1..N;  # Insieme degli indici di colonna

param PIRELLONE{Rows, Cols} binary; # 0 = cella spenta, 1 = accesa.

var AzionareR{Rows} >= 0, <= 1; # 0 = non azionare, 1 = azionare l'interruttore.
var AzionareC{Cols} >= 0, <= 1; # 0 = non azionare, 1 = azionare l'interruttore.
var Fixer  >= 0, <= 1; # usata per garantire la feasibility. 0 = feasible, 1 = non feasible.

# Definizione della funzione obiettivo:
minimize numAzioni:
         1000*Fixer + sum{i in Rows} AzionareR[i] + sum{j in Cols} AzionareC[j];

subject to turn_off{(i,j) in {Rows, Cols} : PIRELLONE[i,j] = 1}: 
        AzionareR[i] + AzionareC[j] + Fixer = 1;

subject to keep_off{(i,j) in {Rows, Cols} : PIRELLONE[i,j] = 0}: 
        AzionareR[i] = AzionareC[j];


# comandi utili per debugging:
#display M;
#display N;
#display Rows;
#display Cols;
#display PIRELLONE;
#display numAzioni;

# lanciamo il Solver:
solve;

printf "Fixer = %d ", Fixer;

# printing the solution:
printf "" > "output.txt";
for{i in Rows} {
   printf "%d ", AzionareR[i] >> "output.txt";
}
printf "\n" >> "output.txt";
for{j in Cols} {
   printf "%d ", AzionareC[j] >> "output.txt";
}
printf "\n" >> "output.txt";

