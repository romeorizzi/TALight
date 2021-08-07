#include <cassert>
#include <iostream>
#include <fstream>

using namespace std;

const int MAX_N = 1000000;

ifstream fin;

int flipped_risp[MAX_N]; int posW = 0;

void scrivi_flipped_mirrortree() {
  int n_figli; fin >> n_figli;
  for(int i = n_figli; i ; i--)
    scrivi_flipped_mirrortree();
  flipped_risp[posW++] = n_figli;
}



int main() {
  fin.open("input.txt"); assert( fin );

  scrivi_flipped_mirrortree();

  do {
    posW--;
    cout << flipped_risp[posW] << " ";
  } while ( posW > 0 );
  cout << endl;

  return 0;
}

