// Prende due estremi dello stesso colore e traccia una striscia,
// quindi procede ricorsivamente nell'intervallo delineato dai due
// estremi e nella parte ancora non colorata.
// Velocissimo ed anche un'intuizione che puo` venire subito,
// chiaramente pero` fa schifo e nelle mie prove non ha mai preso
// piu` di 5 input su 20 :)
//
// Maurizio

#include <iostream>
#include <fstream>
#include <vector>
#include <cassert>

using namespace std;

const int MAXN = 1000000;
const int MAXC = 256;

int strisce[MAXN];
vector<int> pos[MAXC];

int N;

int colora( int a, int b, int col );

int main()
{
 #ifdef EVAL
  ifstream in("input.txt");
  ofstream out("output.txt");
  cin.rdbuf(in.rdbuf());
  cout.rdbuf(out.rdbuf());
#endif  
  cin >> N;
  int prev, last;
  last = 0;
  prev = -1;
  for( int i = 0; i < N; ++i ) {
    int num;
    cin >> num;
    if( num != prev ) {
      prev = num;
      strisce[last] = num;
      pos[num].push_back( last );
      ++last;
    }
  }
  N = last;

  cout << colora( 0, N-1, -1 ) << endl;
}

int colora( int a, int b, int col )
{
  assert( a >= 0 && b < N );
  while( strisce[a] == col && a <= N ) {
    ++a;
  }
  while( strisce[b] == col && b >= 0 ) {
    --b;
  }
  if( b < a ) {
    return 0;
  } else if( b == a ) {
    return 1;
  }

  int estremo_destro = a;
  for( size_t i = 0; i < pos[strisce[a]].size(); ++i ) {
    if( pos[strisce[a]][i] < a ) {
      continue;
    }
    if( pos[strisce[a]][i] < b
	&& pos[strisce[a]][i] > estremo_destro ) {
      estremo_destro = pos[strisce[a]][i];
    }    
  }

  return 1 + colora( a+1, estremo_destro-1, strisce[a] )
    + colora( estremo_destro+1, b, col );
}
