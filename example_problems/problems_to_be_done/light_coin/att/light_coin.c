//problem: lightCoin, example of a solution file, Romeo Rizzi Jan 2015
#include "ourLibToPlay.h"
void individua(long int n) {
  long int i;
  for(i = 0; i<n; i++) {
      if(i%3 == 1) collocaMoneta(i, LEFT);
      if(i%3 == 2) collocaMoneta(i, RIGHT);
  }
  int risp =  piatto_con_peso_maggiore();
  for(i = 0; i<n; i++)
     collocaMoneta(i, NONE);
  if(risp == NONE) denuncia(0); //potrebbe essere la moneta 0 (sul piatto NONE)
  if(risp == LEFT) denuncia(2); //potrebbe essere la moneta 2 (sul piatto RIGHT) 
  if(risp == RIGHT) denuncia(1); //potrebbe essere la moneta 1 (sul piatto LEFT)
}
