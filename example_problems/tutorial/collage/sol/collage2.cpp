#include <cassert>
#include <iostream>
#include <map>
#include <list>
#include <algorithm>
#include <fstream>

using namespace std;

#ifdef EVAL
ifstream in("input.txt");
ofstream out("output.txt");
#else
istream &in(cin);
ostream &out(cout);
#endif

const int MAXN = 1000000;
const int MAXF = 1000;
const int MAXC = 256;

int strisce[MAXF];
int N;
map< int, map<int, int> > cache[MAXF];
list<int> pos[MAXC];

void leggi();
void risolvi();
int ottimizza( int start, int end, int segcol );

int main()
{
  leggi();
  risolvi();
}

void leggi()
{
  int last = 0, prev = -1;
  in >> N;
  assert( ( N > 0 ) && ( N <= MAXN ) );

  // legge eliminando i doppioni consecutivi
  for( int i = 0; i < N; ++i ) {
    int num;
    in >> num;
    if( num != prev ) {
      prev = num;
      strisce[last] = num;
      pos[num].push_back( last );
      ++last;
    }
  }
  N = last;
}

void risolvi()
{
  out << ottimizza( 0, N, -1 ) << endl;
}

int ottimizza( int start, int end, int segcol )
{
  assert( ( start >= 0 ) && ( start <= N ) );
  assert( ( end >= 0 ) && ( end <= N ) );
  assert( start <= end );
  assert( ( segcol >= -1 ) && ( segcol < MAXC ) );

  if( start == end )
    return 0;

  int col1, col2;
  col1 = strisce[start];
  col2 = strisce[end];

  // se e` rimasto un solo elemento:
  if( start == ( end-1 ) ) {
    if( col1 != segcol )
      return 1;
    else
      return 0;
  }

  // verifica se e` gia presente in cache, se si` allora
  // esce
  if( cache[start].count( end ) ) {
    if( cache[start][end].count( segcol ) ) {
#ifndef NDEBUG
	  //cerr << start << " - " << end << " | " 
	  //	   << segcol << " = CACHE!" << endl;
#endif
      return cache[start][end][segcol];
    }
  }

  // se la prima striscia ha gia` il colore del segmento sottostante
  // allora la salta
  if( col1 == segcol ) {
    int ott = ottimizza( start + 1, end, segcol );
    cache[start][end][segcol] = ott;
    return ott;
  }

  // altrimenti si ottimizza provandole tutte
  int ott = N;
  for( list<int>::iterator curr = find( pos[col1].begin(), 
					pos[col1].end(), start );
       ( curr != pos[col1].end() ) && ( *curr < end ); ++curr ) {
    assert( *curr >= start );
    int res = ottimizza( start, *curr + 1, col1 )
      + ottimizza( *curr + 1, end, segcol ) + 1;
    if( res < ott )
      ott = res;
  }
#ifndef NDEBUG
  //cerr << start << " - " << end << " | " << segcol << " = " << ott << endl;
#endif
  cache[start][end][segcol] = ott;
  
  return ott;
}
