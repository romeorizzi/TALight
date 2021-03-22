#include<cassert>
#include<iostream>

using namespace std;

//##########################################
// BEGIN: modifica entro quest'area

int num_mosse(int n) {
    return 43;
}

int mossa(int n) {
  assert(n > 0);
  return 1;
}

// END: modifica entro quest'area
// ################################################


int main() {
  int p, n;
  cin >> p >> n;
  assert(p >= 1);
  assert(p <= 2);
  assert(n >= 0);
  if(p  == 1)
    cout << num_mosse(n)) << endl;
  if(p  == 2)
    cout << mossa(n)) << endl;

  return 0;
}
