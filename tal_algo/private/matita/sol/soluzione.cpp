/*
  Romeo Rizzi e Andrea Cracco 2016

  Approccio DFS, ma senza ricorsione (uso stack).
*/

#include <cassert>
#include <cstdio>
#include <vector>
#include <stack>

using namespace std;

#define NONE -1


int main() {
  stack<int> path;
  int T; scanf("%d",&T);
  for(int t=0; t<T; t++) {  
    int n, m, first_node, last_node;
    scanf("%d %d %d %d", &n, &m, &first_node, &last_node);
    vector< pair<int,int> > neigh[n + 1]; // per ogni arco incidente si specifica l'altro estremo ed il nome dell'arco
    bool used[m];
    for(int i=0; i<m; i++) {
      int a,b;
      scanf("%d %d",&a,&b);
      neigh[a].push_back(make_pair(b,i) );
      neigh[b].push_back(make_pair(a,i) );
      used[i] = false;
    }
    int last_printed_node = NONE;
    path.push(last_node);
    do {
      int v = path.top();
      while( !neigh[v].empty() ) {
        if( used[neigh[v].back().second] )
	  neigh[v].pop_back();
        else {
	  int next_v = neigh[v].back().first;
	  int name_e = neigh[v].back().second;
	  neigh[v].pop_back();
	  used[name_e] = true; 
	  path.push(next_v);
	  v = next_v;
        } 
      }
      if ( last_printed_node == NONE )
	last_printed_node = v;
      else {
	printf("%d %d\n", last_printed_node, v );
	last_printed_node = v;
      }
      path.pop();
    } while( !path.empty() );
    /*
    for(int i=0; i<=n; i++)
      delete *neigh[i];
    */
  }
  return 0;
}
