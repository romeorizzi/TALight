/*
Problema di Longest Common Subsequence rivisto come problema di modellazione matematica.
Questo modello GMPL e' stato creato a scopi didattici.
*/

param M integer, >= 1;  # Number of characters of the first string
param N integer, >= 1;  # Number of characters of the second string

set S_indexes := 1..M;  # Set of indexes for the first string
set T_indexes := 1..N;  # Set of indexes for the second string

set STRINGS;
param FIRST_STRING {STRINGS} symbolic;
param SECOND_STRING {STRINGS} symbolic;

var SelectedChar{S_indexes, T_indexes} binary;

# Definizione della funzione obiettivo:
maximize numChars:
	sum{i in S_indexes, j in T_indexes} SelectedChar[i,j];

subject to unselect{(i,j) in {S_indexes, T_indexes}, (h,k) in {S_indexes, T_indexes} : FIRST_STRING[i] == SECOND_STRING[j] and ((h < i and j < k))}: 
	SelectedChar[i,j] + SelectedChar[h,k] <= 1;



# lanciamo il Solver:
solve;

# comandi utili per debugging:
# display M;
# display N;
# display S_indexes;
# display T_indexes;
# display numChars;
# display SelectedChar;

# printing the solution:
printf "" > "solution.txt";
for{i in S_indexes} {
    for{j in T_indexes} {
        printf "%d ", SelectedChar[i,j] >> "solution.txt";
    }
	printf "\n" >> "solution.txt";
}

