/* FILE: randSpecchio.cpp   last change: 16-Sep-2013   author: Romeo Rizzi
 * This program generates a random rooted ordered tree on n nodes encoded as in the "specchio" string of 3 chars: '*', '(' and ')'problem.
 * Usage syntax:
 *   > randSpecchio.cpp n seed
 * 
 * Usage example:
 *   > randParenthMask 10 777
 */

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cassert>

using namespace std;

const int MAX_N = 1000000;
char s[2*MAX_N];
int tree[MAX_N];

int RandNumber(int min, int max) {
  /* returns an integer in [min, max]
   * see Stroustrup "The c++ Programming Language" 3th edition pg. 685
   * for comments on the following manipulation choice.
   * In particular, considerations on the bad quality of low bits come into account.
   */
  return min + (int) ( (max-min +1) * (double( rand()-0.000000000001 ) / RAND_MAX ) );
}

void randomParenth(int a, int b) {
  if (a >= b) return;
  assert( (a-b) % 2 );
  s[a] = '(';  s[b] = ')';
  int dist_mate_of_a_from_b = 2*RandNumber(0, (b-a)/2);
  if( dist_mate_of_a_from_b == 0 ) randomParenth(a+1, b-1);
  else {
    int c = b - dist_mate_of_a_from_b;
    s[c] = ')';
    s[c+1] = '(';
    randomParenth(a+1, c-1);
    randomParenth(c+1,b);
    // se vuoi generare solo parentesi corrispondenti ad alberi binari: randomParenth(c+2,b-1);
  }
}


int encodeRootedTree(int root_left, int posW) {
  // cout << "root_left = " << root_left << ",  posW = " << posW << endl;
  int num_children = 0; int root_right = 1 + root_left;
  while( s[root_right] == '(' ) {
    num_children++;
    root_right = 1 + encodeRootedTree(root_right, posW + (root_right-root_left +1)/2);
  }
  tree[posW] = num_children;
  return root_right;
}

int main(int argc, char** argv) {
  srand(time(NULL));
  int n = atoi(argv[1]);
  if(argc > 2) srand( atoi(argv[2]) );

  randomParenth(0, 2*n-3);
  // for(int i = 0; i < 2*n-2; i++) cout << i%10; cout << endl;
  // for(int i = 0; i < 2*n-2; i++)
  //   cout << s[i];
  // cout << endl;

  int root_right = encodeRootedTree(0, 1);
  int num_children = 1;
  while( root_right < 2*n-3) {
    num_children++;
    root_right = encodeRootedTree(root_right +1, 1+(root_right+1)/2);
  }
  tree[0] = num_children;

  for(int i = 0; i < n; i++)
    cout << tree[i] << " ";
  cout << endl;

  return 0;
}
