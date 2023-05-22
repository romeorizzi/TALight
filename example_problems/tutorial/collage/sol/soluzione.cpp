/*
solution to arcobaleno that we started to develope together in the class of Algorithms 2020-05-07
memory: O(opt^2)
time: O(opt^3) 
*/

#include<cassert>
#include<iostream>
#include<fstream>

using namespace std;

#ifdef EVAL
ifstream in("input.txt");
ofstream out("output.txt");
#else
istream &in(cin);
ostream &out(cout);
#endif

const int MAXN = 1000000;
const int MAXopt = 150;
const int MAXn = min(MAXN, 2*MAXopt +1); // massima lunghezza della sequenza compressa.

int N, n, seq[MAXn];

int memo[MAXn][MAXn];

int Min(int i, int j) {
  /* ritorna il minimo numero di fogli per comporre l'arcobaleno seq[i...j] (estremi inclusi)
   */
  //out << "i=" << i << "j=" j << endl;
  //printf("i=%d\tj=%d", i,j);
  assert(i >= 0);
  assert(j >= i-1);
  assert(j <= n-1);
  if (i > j) return 0;
  if (i == j) return 1;
  if (memo[i][j] > 0) return memo[i][j];
  int ret;  // devo trovare il meglio sulle varie ipotesi di dove riaffiora il primo foglio
  ret = 1 + Min(i+1,j); // se il foglio non raffiora piu'
  for(int ii= i+1; ii <= j; ii++) {
    if(seq[ii]==seq[i]) {  // se il foglio riaffiora in ii per la prima volta
	   ret = min(ret,
		     Min(i + 1, ii - 1) + Min(ii, j));
    }
  } 
  return memo[i][j] = ret;
}


int PD() {
// ritorna il minimo numero di fogli per comporre l'arcobaleno seq
    for(int i=n-1; i>=0; i--)
        for(int j=i-1; j<n; j++) {
  	    if (i > j) memo[i][j] = 0;
	    else if (i == j) memo[i][j] = 1;
	    else {
	    	memo[i][j] = 1 + memo[i+1][j]; // se il foglio non raffiora piu'
	    	for(int ii= i+1; ii <= j; ii++) {
	    		if(seq[ii]==seq[i]){  // se il foglio riaffiora in ii per la prima volta
	    			memo[i][j] = min(memo[i][j],
	    				memo[i + 1][ii- 1] + memo[ii][j]);
	    		}
	    	}
	    } 
        }
    return memo[0][n-1];
}


int main() {
  //leggo lunghezza della sequenza
  in >> N;
  assert((N > 0) && (N <= MAXN));
  //memorizzo in un array la sequenza eliminando i colori uguali consecutivi
  int tmp, prev = -1;
  n = 0;
  for(int i = 0; i < N; ++i) {
    in >> tmp;
    if (tmp != prev) {
      seq[n++] = tmp;
      prev = tmp;
    }
  }
  int risp = Min(0,n-1);
  out << risp << endl;
  assert(risp == PD());
  return 0;
}

