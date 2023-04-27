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

const int MAXN = 100000;   int n;
const int MAXM = 1000000;   int m;

int first_node, last_node;
vector< pair<int,int> > neigh[MAXN+1]; // per ogni arco incidente si specifica l'altro estremo ed il nome dell'arco

stack<int> path;

bool used[MAXM];

int main(){
#ifdef EVAL
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);
#endif

  scanf("%d %d %d %d",&n,&m,&first_node, &last_node);

  for(int i=0; i<m; i++) {
    int a,b;
    scanf("%d %d",&a,&b);
    neigh[a].push_back(make_pair(b,i) );
    neigh[b].push_back(make_pair(a,i) );
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

  return 0;
}
