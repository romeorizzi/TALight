/* pirellone *
   solutore
   Romeo Rizzi  2015-02-05
*/

#define NDEBUG
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#define  MaxM   1000
#define  MaxN   1000

char R[MaxM], C[MaxN];  // Interruttori di riga e colonna
// M = num righe, N = num colonne
// interruttori di colonna = prima riga (quindi uno per colonna)
// interruttori di riga = prima colonna (a meno di inversione)
int M, N, solvable = 1;

inline void readDigitChar(char *var) {
  // reads the first digit. Also checks that the digit is either 0 or 1.
    do {
      if ( scanf("%c", var ) != 1 )  exit(1);
    } while( (*var < '0') || (*var > '9')  );
    assert( ( *var == '0' ) || ( *var == '1' ) );
}

int main(int argc, char *argv[]) {
  if ( scanf("param M := %d; # Number of rows\n", &M) != 1 )  return 1;
  if ( scanf("param N := %d; # Number of columns\n", &N) != 1 )  return 1;
  assert( 1 <= M && M <= MaxM );
  assert( 1 <= N && N <= MaxN );
  
  char x;
  do {
    if( scanf("%c", &x) != 1 )  return 1;
    //printf("%c", x);
  } while(x != '\n');
  int row_index;
  if( scanf("%d ", &row_index) != 1 )  return 1;
  //printf("\nrow index: %d\n", row_index);
  for (int j = 0 ; j < N ; j++ )
    readDigitChar( &C[j] );

  R[0] = '0';
  for (int i = 1; i < M; i++ ) {
    int row_index;
    if( scanf("%d ", &row_index) != 1 )  return 1;
    //printf("\nrow index: %d\n", row_index);
    readDigitChar( &R[i] );
    R[i] = ( C[0] == R[i] ) ? '0' : '1';
    if( R[i] == '0' )
       for (int j = 1 ; j < N ; j++ ) {
          readDigitChar( &x );
          if( x != C[j] ) { solvable = 0; i = M; j = N; }
       }
    else 
       for (int j = 1 ; j < N ; j++ ) {
          readDigitChar( &x );
          if( x == C[j] ) { solvable = 0; i = M; j = N; }
       }
  }

  if (!solvable){
    printf("0");
    for (int i=1; i < M; i++)
      printf(" 0");
    printf("\n");
    printf("0");
    for (int j=1; j < N; j++)
      printf(" 0");
    printf("\n");
  } else {
    printf("%c", R[0]);
    for (int i=1; i < M; i++)
      printf(" %c", R[i]);
    printf("\n");
    printf("%c", C[0]);
    for (int j=1; j < N; j++)
      printf(" %c", C[j]);
    printf("\n");
  }

  return 0;
}
