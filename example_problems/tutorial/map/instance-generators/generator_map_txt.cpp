/*
 * GENERATORE task mappa
 */ 

#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;


int N, M;
int D[1005][1005];
bool visited[1005][1005];
bool inside(int x, int y){
    return (x >= 1) && (x <= N) && (y >= 1) && (y <= N);
}
bool dfs(int a, int b){
   // cout << a << " " << b << endl;
    visited[a][b] = 1;
    if(a == N && b == N) return true;
    bool can = false;
    for(int i = 0; i < 3; ++i)
        for(int j = 0; j < 3; ++j)
            if(inside(a+i-1,b+j-1))
                if(!visited[a+i-1][b+j-1])
                    if(D[a+i-1][b+j-1] == 0)
                        can |= dfs(a+i-1,b+j-1);
    return can;
}

int main(int argc, char** argv) {
    N = atoi(argv[1]);
    int no_mines = atoi(argv[2]); // if no_mines = 1 then we place no mine
    int seed = atoi(argv[3]);
    srand(seed);
    int THRESHOLD = 40;
    if(no_mines == 1)
      THRESHOLD = 100;
    bool check;
    do{
        for(int i = 1; i <= N; ++i)
            for(int j = 1; j <= N; ++j)
                visited[i][j] = 0;
        for(int i = 1; i <= N; ++i)
            for(int j = 1; j <= N; ++j){
                int q = rand() % 100;
                if(q <= THRESHOLD)
                    D[i][j] = 0;
                else D[i][j] = 1;
            }
        D[1][1] = D[N][N] = 0;
        check = dfs(1,1);
    }while(!check);


    cout << N << endl;
    for(int i = 1; i <= N; ++i){
       for(int j = 1; j <= N; ++j)
           cout  << D[i][j] << " ";
       cout << endl;
    }
    return 0;
}
