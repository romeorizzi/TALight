// problem: lightCoin, Romeo Rizzi Jan 2015
#include "ourLibToPlay.h"

void individua(long int n) {
  long int min = 0, max = n-1, i, last_left, first_right;
  for(i = 0; i<n; i++)
      collocaMoneta(i, NONE);
  while (min < max) {
    long int nAlive = max - min +1;
    for(i = 0; i < (nAlive+1)/3; i++) {
	collocaMoneta(min+i, LEFT);
        last_left = min+i;
	collocaMoneta(max-i, RIGHT);
        first_right = max-i;
    }
    int risp =  piatto_con_peso_maggiore();
    for(i = 0; i < (nAlive+1)/3; i++) {
        collocaMoneta(min+i, NONE);
        collocaMoneta(max-i, NONE);
    }
    if(risp == NONE) { // allora la moneta e' tra quelle non pesate
      min = last_left +1;
      max = first_right -1;
    }
    if(risp == LEFT) { // la moneta leggera e' tra quelle sul piatto RIGHT
      min = first_right;
    }
    if(risp == RIGHT) { // la moneta leggera e' tra quelle sul piatto LEFT
      max = last_left;
    }
  }
  denuncia(min);
}

