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
  printf("%d %d\n", M, N);
  
  char x;
  do {
    if( scanf("%c", &x) != 1 )  return 1;
    //printf("%c", x);
  } while(x != '\n');
  for (int i = 0; i < M; i++ ) {
    int row_index;
    if( scanf("%d ", &row_index) != 1 )  return 1;
    for (int j = 0 ; j < N ; j++ ) {
      readDigitChar( &x );
      printf("%c ", x);
    }
    printf("\n");
  }

  return 0;
}
