#include <cassert>
#include <iostream>
#include <vector>

using namespace std;

const int MAXN = 1000000;
bool seen[MAXN];

void dfs(int u, bool seen[], vector<int> nei[], vector<int> C[], int c) {
  if(!seen[u]) {
    C[c].push_back(u);
    seen[u] = true;
    for(unsigned int i = 0; i < nei[u].size(); i++) {
      dfs(nei[u][i], seen, nei, C, c);
    }
  }
}

int main() {
  int T; cin >> T;
  for(int t=0; t<T; t++) {
    cerr << "Testcase " << t << ":" << endl;
    int n, m; cin >> n >> m;
    cerr << "n = " << n << ", m = " << m << endl;
    vector<int> nei[n]; // per ogni nodo v, nella lista nei[v] sono contenuti i vicinini di v
    for(int i=0; i<m; i++) {
      int a,b; cin >> a >> b; cerr << "a = " << a << ", b = " << b << endl;
      nei[a].push_back(b);
      nei[b].push_back(a);
    }
    vector<int> CC[n]; // lista delle componenti connesse (ciascuna una lista di nodi)
    for(int v=0; v<n; v++)  
      seen[v] = false;
    int c = 0;
    for(int v=0; v<n; v++)  
      if(not seen[v]) {
	dfs(v, seen, nei, CC, c++);
      }
    cout << c << endl;
    for(unsigned int k = 0; k < c; k++) {
      cout << CC[k][0] << " ";
    }
    cout << endl;
  }
  return 0;
}
