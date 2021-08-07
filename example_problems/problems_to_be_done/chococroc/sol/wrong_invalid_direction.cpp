#include <bits/stdc++.h>

using namespace std;

int win_from(int n, int m) {
    return 1;
}

int cut_direction(int n, int m) {
    return 42;
}

int eat_size(int n, int m) {
    return 1;
}

int main(int argc, char** argv) {

    int action, m, n;
    cin >> action >> m >> n;
    assert(!cin.fail());
    assert(action == 0 || action == 1);
    assert(m > 0 && n > 0);
    
    auto res = win_from(m, n);
    cout << (res ? 1 : 2) << endl;

    if(action && res) { //anche la mossa
        auto direction = cut_direction(m,n);
        assert(direction == 0 || direction == 1);
        if(direction) {
            cout << m                  << endl << n - eat_size(m, n) << endl;
        } else {
            cout << m - eat_size(m, n) << endl << n                  << endl;
        }
    }

    return 0;
}
