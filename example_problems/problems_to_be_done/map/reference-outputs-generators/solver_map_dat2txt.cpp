/*
 * SOLUZIONE task mappa
 */ 
#include <iostream>
#include <fstream>
#include <list>
#include <cstdio>
#include <string>

using namespace std;

const int NMAX = 1005;
const int INFINITO = 1000000;
const int TRAB = 0;

//int mappa[NMAX][NMAX];
int dist[NMAX][NMAX];
int N;

typedef pair<int,int> ii;
// FIFO
list<ii> lista;

int main(int argc, char *argv[]) {
  if ( scanf("param N :=  %d;  # number of rows and columns of the map\n", &N) != 1 )  return 1;	

  char x;
  do {
    if( scanf("%c", &x) != 1 )  return 1;
    //printf("%c", x);
  } while(x != '\n');
  	
  int c;
  for (int i = 0; i < N; i++) {
  	cin >> c;
  	for (int j = 0; j < N; j++) {
  		cin >> c;
  		// se è 0 (zero) la distanza è infinita (= inesplorato)
  		if (c == 0) dist[i][j] = INFINITO;
  		// altrimenti è una trappola
  		else dist[i][j] = TRAB;
  	}
  }
  
  // segno la partenza a distanza 1 e inizio la BFS da lì
  lista.push_back(ii(0,0));
  dist[0][0] = 1;
  
  // finchè devo visitare altri nodi
  while (!lista.empty()) {
  	// estraggo il primo nodo inserito
  	ii coord = lista.front(); lista.pop_front();
  	int x = coord.first;
  	int y = coord.second;
  	// se è la destinazione mi fermo
  	if (x == N-1 && y == N-1) {
  		cout << dist[x][y] << endl;
  		return 0;
  	}
  	// scorro tutte le 9 celle attorno a quella attuale
  	// (il centro viene implicitamente ignorato dal secondo if)
  	for (int r = -1; r <= 1; r++)
  		for (int c = -1; c <= 1; c++)
  			// se sono ancora nella tabella
  			if (x+c>=0 && x+c<N && y+r>=0 && y+r<N) {
  				// se ho trovato una strada più corta
  				if (dist[x][y]+1 < dist[x+c][y+r]) {
  					// salvo la nuova distanza
  					dist[x+c][y+r] = dist[x][y]+1;
  					// faccio ripartire la visita dalla cella
  					lista.push_back(ii(x+c,y+r));
  				}
  			}
  }
  return 0;
}
