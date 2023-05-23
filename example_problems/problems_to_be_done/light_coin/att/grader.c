// problem: lightCoin, Romeo Rizzi Jan 2015

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#define NONE  0
#define LEFT  -1
#define RIGHT  1

extern void individua(long int n);

static FILE *file;
static long int nMonete;
static long int lightCoin;
static long int nLeft, nRight, nPesate;
static long int maxPesate;
static int subtask;
static long int min(long int a, long int b) { return a < b ? a : b; }
static long int max(long int a, long int b) { return a > b ? a : b; }

static int piatto[1000000];

static int mylog(int b, long int n) {
  int risp = 0;
  long int reached = 1;
  while(reached < n) { risp++; reached *= b; }
  return risp;
}

void collocaMoneta(long int moneta, int piatto_target) {
  if( piatto[moneta] == LEFT) nLeft--;
  if( piatto[moneta] == RIGHT) nRight--;
  piatto[moneta] = piatto_target;
  if( piatto[moneta] == LEFT) nLeft++;
  if( piatto[moneta] == RIGHT) nRight++;
}

int piatto_con_peso_maggiore() {
  //long int i;
  //for(i = 0; i < nMonete; i++) 
  //   fprintf(file, "%d ", piatto[i]);
  //fprintf(file, "\n");

  nPesate++;
  if(nLeft > nRight) return LEFT;
  if(nRight > nLeft) return RIGHT;
  if(piatto[lightCoin] == NONE) return NONE;
  if(piatto[lightCoin] == LEFT) return RIGHT;
  if(piatto[lightCoin] == RIGHT) return LEFT;
  assert( 0 );
}

void denuncia(long int risp) {
  fprintf(file, "%ld %ld %ld\n", risp, nPesate, maxPesate);
  exit(0);
}

int main() {
  srand(8753);
  nLeft = nRight = nPesate = 0;

#ifdef EVAL
  file = fopen("input.txt", "r");
#else
  file = stdin;
#endif

  fscanf(file, "%ld %ld %d", &lightCoin, &nMonete, &subtask);
  fclose(file);

#ifdef EVAL
  file = fopen("output.txt", "w");
#else
  file = stdout;
#endif

  maxPesate = 10*nMonete;
  if(subtask == 2) { assert(nMonete==7); maxPesate = 6; }
  if(subtask == 3) { assert(nMonete==7); maxPesate = 4; }
  if(subtask == 4) { assert(nMonete==7); maxPesate = 3; }
  if(subtask == 5) { assert(nMonete==8); maxPesate = 3; }
  if(subtask == 6) maxPesate = nMonete-1;
  if(subtask == 7) maxPesate = nMonete/2;
  if(subtask == 8) maxPesate = mylog(2,nMonete);
  if(subtask == 9) maxPesate = mylog(3,nMonete);

  individua(nMonete);
  fclose(file);
}
