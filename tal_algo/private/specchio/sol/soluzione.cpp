/* FILE: specchio.cpp   last change: 16-Sep-2013   author: Romeo Rizzi
 * a solver for problem specchio based on dynamic programming
 */

#include <iostream>

using namespace std;

const int MAX_N = 1000000;
int n;
int tree[MAX_N]; /*stores the original input tree encoded in the proprietary format of the problem, that is:
   tree[i] = number of children of node i.
 (Where the IDs of the nodes are the first n natural numbers assigned in DFS-preorder starting from the root as node 0). */
int mirror[MAX_N]; //stores the output tree encoded in the proprietary format of the problem.

int posW;
int mirrorSubtree(int root) {
// ritorna il numero di nodi n' del sotto-albero di tree radicato al nodo <root>.
// Inoltre, scrive la codifica dell'albero immagine riflessa di tale sottoalbero nel sotto-array mirror[posW -n' +1, posW]
  int num_descendants = 1; // ogni nodo ha quantomeno se stesso come discendente
  for(int i = 1; i <= tree[root]; i++)
    num_descendants += mirrorSubtree(root +num_descendants);
  mirror[posW--] = tree[root];
  return num_descendants;
}


int main() {
  int T;
  cin >> T;
  for(int i = 0; i<T; i++) {
    posW = 0;
    n = 0; // while reading the file input.txt, n will more precisely stand for the number of those nodes v for which tree[v] has already been read. 
    int declared = 1; // at least the root is out there.
    while( n < declared ) {
      cin >> tree[n];
      declared += tree[n];
      n++;
    }

    posW = n-1; mirrorSubtree(0);

    for(int i = 0; i < n; i++)  cout << mirror[i] << " ";
    cout << endl;
  }

  return 0;
}
