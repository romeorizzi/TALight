/* Translates an instance of the pirellone problem in dat format
   Usage:
     works in streaming: reads from stdin and writes to stdout.
*/

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define  MaxN   1000

void usage() {
  printf("This program translates an instance of the pirellone problem in dat format.");
  printf(" Usage:");
  printf("      works in streaming: reads from stdin and writes to stdout.");
  printf("      takes no input parameters.");
}

int main(int argc, char *argv[]) {
  if ( argc != 1 ) {
    usage();
    return 1;
  }

  int M, N;
  scanf("%d %d", &M, &N);
  printf("param M := %d;  # Number of rows\n", M);
  printf("param N := %d;  # Number of columns\n", N);
  printf("param PIRELLONE :  ");
  for(int j = 1; j <= N; ++j) printf("%d ", j);
  printf(":=\n");

  for(int i = 0; i < M; ++i) {
     printf("           %d   ", i+1);
     for(int j = 0; j < N; ++j) {
       int ele;
       scanf("%d", &ele);
       printf("%d ", ele);
     }
     if(i == M-1)
       printf(";\n");
     printf("\n");
  }
  printf("end;\n");

  return 0;
}
