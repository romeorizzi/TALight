/* An instance (in dat format) generator for the pirellone problem
   Usage:
   ./generator <M> <N> <solvable> <seed>
   where
      M is the number of rows
      N is the number of colums
      if solvable = 1 the Pirellone can be solved, use solvable = 0 for an unsolvable instance
      seed  is the random seed for the pseudo-random generation process,
*/

#include <cassert>
#include <stdio.h>
#include <stdlib.h>

#define  MaxM   1000
#define  MaxN   1000

void usage() {
  printf("This program is an instance (in dat format) generator for the Pirellone problem.\n");
  printf(" Usage:\n");
  printf("   ./generator <M> <N> <solvable> <seed>\n");
  printf("   where:\n");
  printf("      M is the number of rows\n");
  printf("      N is the number of colums\n");
  printf("      - use solvable = 1 to get a Pirellone that can be solved\n");
  printf("      - use solvable = 0 for an unsolvable instance\n");
  printf("      seed  is the random seed for the pseudo-random generation process.\n");
}

char P[MaxM][MaxN];     // Luci del Pirellone
char R[MaxM], C[MaxN];  // Interruttori di riga e colonna
int M, N, solvable, seed;

void invert_row(int i) {
  for (int j=0; j < N; j++)
    P[i][j] = 1-P[i][j];
}

void invert_col(int j) {
  for (int i=0; i < M; i++)
    P[i][j] = 1-P[i][j];
}

int main(int argc, char *argv[]) {
  if ( argc != 5 ||
       sscanf(argv[1], " %d", &M) != 1 ||
       sscanf(argv[2], " %d", &N) != 1 ||
       sscanf(argv[3], " %d", &solvable) != 1 ||
       sscanf(argv[4], " %d", &seed) != 1 ) {
    usage();
    return 1;
  }

  srand( seed );
  
  assert( 1 <= M && M <= MaxM );
  assert( 1 <= N && N <= MaxN );

  for (int i=0; i < M/2; i++)
    R[ rand() % M ] = 1;
  for (int j=0; j < N/2; j++)
    C[ rand() % N ] = 1;

  for (int i=0; i < M; i++)
    if (R[i])
      invert_row( i );

  for (int j=0; j < N; j++)
    if (C[j])
      invert_col( j );

  if (!solvable) {
    int i = rand() % M;
    int j = rand() % N;
    P[i][j] = 1-P[i][j];
  }

  printf("param M := %d;  # Number of rows\n", M);
  printf("param N := %d;  # Number of columns\n", N);
  printf("param PIRELLONE :  ");
  for(int j = 1; j <= N; ++j) printf("%d ", j);
  printf(":=\n"); 
  for(int i = 1; i <= M; ++i){
     printf("           %d   ", i);
     for(int j = 1; j <= N; ++j)
         printf("%d ", P[i-1][j-1]);
     if( i == M) printf(";\n");
     printf("\n");
  }
  printf("end;\n");

  return 0;
}
