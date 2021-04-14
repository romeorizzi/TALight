/*
Problem: the Miky Mouse map, originally proposed at the Italian Olympiads of Informatics (OII), and here revised and casted as a mathematical modeling problem for didactical purposes.
Romeo Rizzi (romeo.rizzi@univr.it)
*/

param N integer, >= 1;  # number of rows and columns of the map

set Rows := 1..N;  # the set of row indexes
set Cols := 1..N;  # the set of column indexes

param MAP{Rows, Cols} binary; # 0 = free cell, 1 = cell containing a trap.

set CELL := {Rows, Cols};  # the set of cells comprising the map (which is practice is a square checkboard)    
set CELL_GOOD := { (i,j) in CELL : MAP[i,j] = 0 };
set CELL_BAD := { (i,j) in CELL : MAP[i,j] = 1 };

var dist{CELL} >= 1; to every cell we associate a real variable expressing its distance from cell (1,1) in the map

# objective function definition:
maximize Distanza:
         dist[N,N];
# fix the distance of the starting cell (1,1) to 1:
subject to fixDistHOME: 
        dist[1,1] = 1;

# fix also the distances of all forbidden cells (the ones with a trap):
subject to fixDistBAD{(i,j) in CELL_BAD}: 
        dist[i,j] = 1;

# upper bound triggered by the north cell just above:
subject to UpperBoundDistN{(i,j) in CELL_GOOD :  i > 1 and (i-1,j) in CELL_GOOD}:
        dist[i,j] <= dist[i-1,j] + 1;

# upper bound triggered by the south cell just below:
subject to UpperBoundDistS{(i,j) in CELL_GOOD : i < N and (i+1,j) in CELL_GOOD}:
        dist[i,j] <= dist[i+1,j] + 1;

# upper bound triggered by the east cell just to the right:
subject to UpperBoundDistE{(i,j) in CELL_GOOD : j < N and (i,j+1) in CELL_GOOD}:
        dist[i,j] <= dist[i,j+1] + 1;

# upper bound triggered by the west cell just to the left:
subject to UpperBoundDistO{(i,j) in CELL_GOOD : j > 1 and (i,j-1) in CELL_GOOD}:
        dist[i,j] <= dist[i,j-1] + 1;

# upper bound triggered by the north-east cell, adjacent along the diagonal:
subject to UpperBoundDistNE{(i,j) in CELL_GOOD :  i > 1 and j < N and (i-1,j+1) in CELL_GOOD}:
        dist[i,j] <= dist[i-1,j+1] + 1;

# upper bound triggered by the north-west cell, adjacent along the diagonal:
subject to UpperBoundDistNO{(i,j) in CELL_GOOD :  i > 1 and j > 1 and (i-1,j-1) in CELL_GOOD}:
        dist[i,j] <= dist[i-1,j-1] + 1;

# upper bound triggered by the south-est cell, adjacent along the diagonal:
subject to UpperBoundDistSE{(i,j) in CELL_GOOD :  i < N and j < N and (i+1,j+1) in CELL_GOOD}:
        dist[i,j] <= dist[i+1,j+1] + 1;

# upper bound triggered by the south-west cell, adjacent along the diagonal:
subject to UpperBoundDistSO{(i,j) in CELL_GOOD :  i < N and j > 1 and (i+1,j-1) in CELL_GOOD}:
        dist[i,j] <= dist[i+1,j-1] + 1;


# load the instance data:
data input.txt;  

# commands useful in debugging and/or other experimenting:
# display N;
# display MAP;
# display CELL;
# display CELL_GOOD;
#for {(i,j) in CELL_GOOD : i > 1 and (i-1,j) in CELL_GOOD}
#     expand UpperBoundDistN[i,j];

# run the Solver:
option solver cplex; # in AMPL posso scegliere il Solver da utilizzare
option solver_msg 0; # silent mode per il solver (AMPL specific)
solve > /dev/null; # per non visualizzare nemmeno la versione (AMPL specific)

# print the optimum solution value in the file output.txt:
printf "%d\n", Distanza > "output.txt";
# in AMPL potevo piu' semplicemente scrivere: print Distanza > output.txt;

end;

