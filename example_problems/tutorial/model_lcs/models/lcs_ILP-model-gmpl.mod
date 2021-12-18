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

var SelectedMatch{S_indexes, T_indexes} binary;

maximize numMatches:
	sum{i in S_indexes, j in T_indexes} SelectedMatch[i,j];

subject to no_cross{(i,j) in {S_indexes, T_indexes}, (i2,j2) in {S_indexes, T_indexes} : ((i < i2 and  j2 < j))}: 
	SelectedMatch[i,j] + SelectedMatch[i2,j2] <= 1;

subject to i_monogamy{(i,j,j2) in {S_indexes, T_indexes, T_indexes} : (j < j2) }: 
	SelectedMatch[i,j] + SelectedMatch[i,j2] <= 1;

subject to j_monogamy{(i,j,i2) in {S_indexes, T_indexes, S_indexes} : (i < i2) }: 
	SelectedMatch[i,j] + SelectedMatch[i2,j] <= 1;    
    
subject to unmatch{(i,j) in {S_indexes, T_indexes} : S_STRING[i] != T_STRING[j]}: 
    SelectedMatch[i,j] = 0;


# lanciamo il Solver:
solve;

# # comandi utili per debugging:
# display M;
# display N;
# display S_indexes;
# display T_indexes;
# display numMatches;
# display SelectedMatch;

# printing the solution:
printf "" > "solution.txt";
for{i in S_indexes} {
    for{j in T_indexes} {
        printf "%d ", SelectedMatch[i,j] >> "solution.txt";
    }
	printf "\n" >> "solution.txt";
}

