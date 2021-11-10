/*
Problema degli Asteroidi, originalmente introdotto per il corso di Mathematics for Decisions,
rivisto come problema di modellazione matematica.
Questo modello AMPL e' stato creato da Romeo Rizzi (romeo.rizzi@univr.it) a scopi didattici.
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

subject to turn_off{(i,j) in {Rows, Cols} : ASTEROID[i,j] = 1}: 
        AzionareR[i] + AzionareC[j] = 1;

subject to keep_off{(i,j) in {Rows, Cols} : ASTEROID[i,j] = 0}: 
        AzionareR[i] = AzionareC[j];


# carichiamo i dati dell'istanza:
data input.txt;  

# comandi utili per debugging:
#display M;
#display N;
#display Rows;
#display Cols;
#display ASTEROID;
#display numAzioni;

# lanciamo il Solver:
option solver cplex; # in AMPL posso scegliere il Solver da utilizzare
option solver_msg 0; # silent mode per il solver (AMPL specific)
solve > /dev/null; # per non visualizzare nemmeno la versione (AMPL specific)

# Stampa della soluzione:

for{i in Rows} {
  if solve_result = "infeasible" then
     printf "0 " > "output.txt";
  else
     printf "%d ", AzionareR[i] > "output.txt";
}
printf "\n" > "output.txt";
for{j in Cols} {
  if solve_result = "infeasible" then
     printf "0 " > "output.txt";
  else
     printf "%d ", AzionareC[j] > "output.txt";
}
printf "\n" > "output.txt";

