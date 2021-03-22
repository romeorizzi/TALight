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

bool isValidMove(int n, int m, int n_1, int m_1) {

    int deltaN = n - n_1;
    int deltaM = m - m_1;
    if(deltaN < 0) return false;
    if(deltaM < 0) return false;
    if(!((deltaN != 0) ^ (deltaM != 0))) return false;
    
    if(deltaN > n_1 || deltaM > m_1) return false;

    return true;
}

const string err_malformato = "Output malformato";
const string err_wrong_player = "Vincitore sbagliato";
const string err_invalid_move = "Mossa non valida";
const string err_wrong_move = "Mossa sbagliata";
const string err_correct = "Corretto";

bool readSuccess(ifstream& stream, int& toBeRead) {
    stream >> toBeRead;
    if(stream.fail()) {
        return false;
    } else {
        return true;
    }
}

void ex(const string& msg, float code) {
    cerr << msg << endl;
    cout << code << endl;
    exit(0);
}

void readAndFail(ifstream& stream, int& toBeRead, const string err = err_malformato) {
    if(!readSuccess(stream, toBeRead)) {
        ex(err, 0.0f);
    }
}



int main(int argc, char** argv) {
    assert(argc == 4);
    ifstream in(argv[1]);
    ifstream cor(argv[2]);
    ifstream out(argv[3]);
    assert(!(in.fail() || cor.fail() || out.fail()));


    int action, m, n;
    in >> action >> m >> n;

    int correctWinner, outWinner;
    cor >> correctWinner;
    readAndFail(out, outWinner);
    if(correctWinner != outWinner) {
        ex(err_wrong_player, 0.0f);
    }

    if(action == 1) {
        if(correctWinner == 1) {
            int m_1, n_1;
            readAndFail(out, m_1);
            readAndFail(out, n_1);
            if(!isValidMove(m, n, m_1, n_1)) {
                ex(err_invalid_move, 0.0f);
            }
            if(win_from(m_1,n_1)) {
                ex(err_wrong_move, 0.0f);
            }
        } else if(readSuccess(out, m)) {
            ex(err_malformato, 0.0f);
        }
    }

    ex(err_correct, 1.0f);

    return 0;
}
