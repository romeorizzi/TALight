#include <bits/stdc++.h>

using namespace std;

int win_from(int n, int m) {
	if (n < m) 
		swap(n, m);
   	return (n + 1) % (m + 1) != 0 || __builtin_popcount((n + 1) / (m + 1)) != 1;
}

int cut_direction(int n, int m) {
    // TODO
    return 42;
}

int eat_size(int n, int m) {
    // TODO
    return 42;
}

int main(int argc, char** argv) {

    int action, m, n;
    cin >> action >> m >> n;
    assert(!cin.fail());
    assert(action == 0 || action == 1);
    assert(m > 0 && n > 0);
    
    auto res = win_from(m, n);
    cout << (res > 0 ? 1 : 2) << endl;

    return 0;
}
