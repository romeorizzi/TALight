/* pirellone *
   super fast solver based on "all raws are equal up to inversion"
   reads whole lines for fast input
   Romeo Rizzi  2015-02-05
*/

#define NDEBUG
#include <cassert>
#include <stdio.h>
#include <string.h>

#define EVAL // to work with files also in local
#define  MaxM   1000
#define  MaxN   1000

// M = num righe, N = num colonne
// l'intervallo utile di una riga si compone pertanto di 2N+2 caratteri (per arrivare ad includere il newline)

char firstRow[2*MaxN +2];
char invFirstRow[2*MaxN +2];
char genRow[2*MaxN +2];
char firstCol[2*MaxM +2];

int M, N, solvable = 1;

int main(int argc, char *argv[]) {
#ifndef EVAL
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);
#endif
  int i, j;
  if ( scanf("%d", &M) != 1 )  return 1;
  if ( scanf("%d", &N) != 1 )  return 1;
  assert( 1 <= M && M <= MaxM );
  assert( 1 <= N && N <= MaxN );

  char ignore[2*MaxM+100];
  fgets(ignore, sizeof(ignore), stdin);
  //  printf(" ignore row: %s", ignore);

  fgets(firstRow, sizeof(firstRow), stdin);
  //  printf(" -- First row: %s", firstRow);

  for ( j = 0 ; j < N ; j++ ) {
    invFirstRow[2*j] = ( firstRow[2*j] == '1' ) ? '0' : '1';
    invFirstRow[2*j+1] = ' ';
  }
  invFirstRow[2*N] = '\n';
  //  printf("Inv first row: %s", invFirstRow);
  
  firstCol[0] = firstRow[0];
  firstCol[1] = ' '; // firstCol and firstRow are strings with spaces
  for ( i = 1; i < M; i++ ) {
    fgets(genRow, sizeof(genRow), stdin);
    //  printf("%s", genRow);
    firstCol[2*i] = genRow[0];
    firstCol[2*i+1] = ' ';
    if( firstCol[2*i] == firstCol[0]) {
      if(strncmp(genRow, firstRow, 2*N-1) != 0)  { solvable = 0; i = M; }
    }
    else 
      if(strncmp(genRow, invFirstRow, 2*N-1) != 0)  { solvable = 0; i = M; }
  }
  firstCol[2*M] = '\n';
//printf(" -- First col: %s", firstCol);

  if (!solvable){
    printf("0");
    for (i=1; i < M; i++)
      printf(" 0");
    printf("\n");
    printf("0");
    for (j=1; j < N; j++)
      printf(" 0");
    printf("\n");
  }
  else {
    printf("%s", firstCol);
    if(firstCol[0] == '0') 
      printf("%s", firstRow);
    else
      printf("%s", invFirstRow);
  }

  return 0;
}
