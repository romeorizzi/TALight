#include <cassert>
#include <iostream>

using namespace std;

const int MAX_N = 1000000;

int flipped_risp[MAX_N]; int posW = 0;

void scrivi_flipped_mirrortree() {
  int n_figli; cin >> n_figli;
  for(int i = n_figli; i ; i--)
    scrivi_flipped_mirrortree();
  flipped_risp[posW++] = n_figli;
}



int main() {

  scrivi_flipped_mirrortree();

  do {
    posW--;
    cout << flipped_risp[posW] << " ";
  } while ( posW > 0 );
  cout << endl;

  return 0;
}

