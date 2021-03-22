// problem: lightCoin, Romeo Rizzi Jan 2015
#include "ourLibToPlay.h"

void individua(long int n) {
  long int i;
  for(i = 0; i < n; i++)
     collocaMoneta(i, NONE);
  collocaMoneta(0, LEFT);
  for (i=1; i<n-1; i++) {
    collocaMoneta(i, RIGHT);
    int risp =  piatto_con_peso_maggiore();
    collocaMoneta(i, NONE);
    if(risp == RIGHT) denuncia(0);
    if(risp == LEFT) denuncia(i);
  }
  denuncia(n-1);
}
