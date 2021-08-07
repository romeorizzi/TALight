#include <bits/stdc++.h>
#include <cassert>
using namespace std;

int move(int row, int col) {
    if (col < row) swap(col, row);
    while (row < (col+1)/2)
        row = row * 2 + 1;
    return col - row;
}

int win_from(int n, int m) {
    return move(n, m) > 0;
}

int cut_direction(int n, int m) {
    return (n < m) ? 1 : 0;
}

int eat_size(int n, int m) {
    return move(n, m);
}

int main(int argc, char** argv) {

    int action, m, n;
    cin >> action >> m >> n;
    assert(!cin.fail());
    assert(action == 0 || action == 1);
    assert(m > 0 && n > 0);
    
    auto res = eat_size(m, n);
    cout << (res > 0 ? 1 : 2) << endl;

    if(action && res > 0) { //anche la mossa
        if(cut_direction(m,n)) {
            cout << m       << endl << n - res << endl;
        } else {
            cout << m - res << endl << n       << endl;
        }
    }

    return 0;
}
