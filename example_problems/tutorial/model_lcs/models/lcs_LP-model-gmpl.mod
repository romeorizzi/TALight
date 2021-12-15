/*
Problema di Longest Common Subsequence rivisto come problema di modellazione matematica.
Questo modello GMPL e' stato creato a scopi didattici.
*/

param M integer, >= 1;  # Number of characters of the first string s
param N integer, >= 1;  # Number of characters of the second string t

set S_indexes := 1..M;  # Set of indexes for the first string s
set T_indexes := 1..N;  # Set of indexes for the second string t

set STRINGS;
param S_STRING {STRINGS} symbolic;
param T_STRING {STRINGS} symbolic;

set PD_S_indexes := 1..M+1;  # Set of indexes for the first string
set PD_T_indexes := 1..N+1;  # Set of indexes for the second string

var PD{PD_S_indexes, PD_T_indexes}, >= 0;

# Definizione della funzione obiettivo:
minimize numMatches:
	PD[1,1];

subject to fun_1{ (i,j) in {S_indexes, T_indexes} : S_STRING[i] == T_STRING[j]}:
	PD[i,j] >= PD[i+1,j+1] + 1;

subject to fun_2{(i,j) in {S_indexes, T_indexes} : S_STRING[i] != T_STRING[j]}:
    PD[i,j] >= PD[i,j+1];
    # PD[i,j] >= PD[i+1,j];

subject to fun_2_1{(i,j) in {S_indexes, T_indexes} : S_STRING[i] != T_STRING[j]}:
    PD[i,j] >= PD[i+1,j];
        
subject to fun_3{j in {PD_T_indexes} }:
    PD[M,j] <= 0;

subject to fun_4{i in {PD_S_indexes} }:
	PD[i,N] <= 0;


# lanciamo il Solver:
solve(timelimit=30);

# comandi utili per debugging:
display M;
display N;
display S_indexes;
display T_indexes;
display PD_S_indexes;
display PD_T_indexes;
display numMatches;
display PD;

# printing the solution:
printf "" > "solution.txt";
for{i in S_indexes} {
    for{j in T_indexes} {
        printf "%d ", PD[i,j] >> "solution.txt";
    }
	printf "\n" >> "solution.txt";
}

