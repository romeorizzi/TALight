// problem: lightCoin, Romeo Rizzi Jan 2015
#include "ourLibToPlay.h"

void individua(long int n) {
  long int min = 0, max = n-1, i;
  for(i = 0; i<n; i++)
      collocaMoneta(i, NONE);
  while (min < max) {
    long int nAlive = max - min +1;
    for(i = 0; i < nAlive/2; i++) {
	collocaMoneta(min + i, LEFT);
	collocaMoneta(max - i, RIGHT);
    }
    if(n%2) collocaMoneta(min +nAlive/2, NONE);
    int risp =  piatto_con_peso_maggiore();
    for(i = 0; i < nAlive/2; i++) {
        collocaMoneta(min + i, NONE);
        collocaMoneta(max - i, NONE);
    }
    if(risp == NONE) // allora la moneta e' quella non pesata
      denuncia(min +nAlive/2);
    if(risp == LEFT) { // la moneta leggera e' tra quelle sul piatto RIGHT
      min = min +nAlive/2 + n%2;
    }
    if(risp == RIGHT) { // la moneta leggera e' tra quelle sul piatto LEFT
      max = min +nAlive/2 -1;
    }
  }
  denuncia(min);
}
