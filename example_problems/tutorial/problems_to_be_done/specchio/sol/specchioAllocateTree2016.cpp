#include <cassert>
#include <iostream>
#include <fstream>
#include <deque>

using namespace std;

const int MAX_N = 1000000;

ifstream fin;

int num_figli[MAX_N +1];
int vett[MAX_N +1];
deque<int> lista_figli[MAX_N +1];

int leggi_input(int v) {
// setta num_figli e lista_figli per ogni nodo del sottoalbero radicato in v
// ritorna il primo nodo che fuorisce dal sottoalbero (potrebbe essere n+1)
  assert( v >= 1 );
  fin >> num_figli[v];
  int z = v+1; // identita' dell'eventuale prossimo figlio
  for(int i = 1; i <= num_figli[v]; i++) {
    lista_figli[v].push_back(z); 
    z = leggi_input( z );
  }
  return z;
}

void print_tree(int v) {
// stampa la codifica del sottoalbero radicato in v.
  assert( v >= 1 );
  cout << num_figli[v] << " ";
  for(int i = 0; i < num_figli[v]; i++)
    print_tree( lista_figli[v][i] );
}

void print_mirrortree(int v) {
// stampa la codifica del sottoalbero radicato in v, rovesciato nello specchio.
  assert( v >= 1 );
  cout << num_figli[v] << " ";
  for(int i = num_figli[v] -1; i >= 0; i--)
    print_mirrortree( lista_figli[v][i] );
}



int main() {
  fin.open("input.txt"); assert( fin );

  int n = leggi_input( 1 ) -1;

  print_tree( 1 ); cout << endl;

  print_mirrortree( 1 ); cout << endl;

  return 0;
}

