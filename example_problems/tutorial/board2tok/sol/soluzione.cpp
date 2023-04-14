/*
 * SOLUZIONE UFFICIALE - board2tok
 * Soluzione ricorsiva
 * 
 * Romeo Rizzi
 */ 

#include <iostream>
#include <fstream>
#include <cassert>

using namespace std;

int pow2(int exp) {
  assert( exp >= 0 );
  if( exp == 0 ) return 1;
  return 2*pow2( exp -1 );
}

bool isPowerOf2(int n) {
  assert ( n > 0 );
  if( n == 1 ) return true;
  if( n % 2 ) return false;
  return isPowerOf2(n/2);
}

const int MAXK = 10;
const int MAXN = 1024;
int N, K, hole_row, hole_col;
char board[MAXN][MAXN]; // rows and columns are numbered starting from 0.

void fillBoard(int first_row, int first_col, int last_row, int last_col, int hole_row, int hole_col) {
  /* fills in the sub-board board[first_row ... last_row][first_col ... last_col] (always of size 2^k*2^k for some k <= K) leaving one single hole in the prescribed position (hole_row, hole_col) */
  //cout << first_row << " " << first_col << " " << last_row << " " << last_col << " " << hole_row << " " << hole_col << endl;
  assert( first_row <= hole_row ); assert( hole_row <= last_row );
  assert( first_col <= hole_col); assert( hole_col <= last_col );
  assert( last_row - first_row == last_col - first_col );
  int n = last_row - first_row + 1;
  assert( isPowerOf2(n) );
  if( n == 1) return;
  int n_halved = n/2;
  int firstRow[2][2], firstCol[2][2], lastRow[2][2], lastCol[2][2]; // the borders of the 4 sub-boards of the 4 inductive subproblems  
  int rowH[2][2], colH[2][2]; // row and column of the hole in each of the 4 inductive subproblems

  firstRow[0][0] = first_row; firstCol[0][0] = first_col;
  lastRow[0][0] = first_row + n_halved -1; lastCol[0][0] = first_col + n_halved -1;
  rowH[0][0] = first_row + n_halved -1; colH[0][0] = first_col + n_halved -1;
  if( (hole_row < first_row + n_halved) && (hole_col < first_col + n_halved) ) {
     rowH[0][0] = hole_row; colH[0][0] = hole_col;
     board[first_row + n_halved][first_col + n_halved] = '4';
     board[first_row + n_halved-1][first_col + n_halved] = 'N';
     board[first_row + n_halved][first_col + n_halved-1] = 'W';
  }

  firstRow[0][1] = first_row; firstCol[0][1] = first_col + n_halved;
  lastRow[0][1] = first_row + n_halved -1; lastCol[0][1] = last_col;
  rowH[0][1] = first_row + n_halved -1; colH[0][1] = first_col + n_halved;
  if( (hole_row < first_row + n_halved) && (hole_col >= first_col + n_halved) ) {
     rowH[0][1] = hole_row; colH[0][1] = hole_col;
     board[first_row + n_halved][first_col + n_halved-1] = '1';
     board[first_row + n_halved-1][first_col + n_halved-1] = 'N';
     board[first_row + n_halved][first_col + n_halved] = 'E';
  }

  firstRow[1][0] = first_row + n_halved; firstCol[1][0] = first_col;
  lastRow[1][0] = last_row; lastCol[1][0] = first_col + n_halved -1;
  rowH[1][0] = first_row + n_halved; colH[1][0] = first_col + n_halved -1;
  if( (hole_row >= first_row + n_halved) && (hole_col < first_col + n_halved) ) {
     rowH[1][0] = hole_row; colH[1][0] = hole_col;
     board[first_row + n_halved-1][first_col + n_halved] = '3';
     board[first_row + n_halved][first_col + n_halved] = 'S';
     board[first_row + n_halved-1][first_col + n_halved-1] = 'W';
  }

  firstRow[1][1] = first_row + n_halved; firstCol[1][1] = first_col + n_halved;
  lastRow[1][1] = last_row; lastCol[1][1] = last_col;
  rowH[1][1] = first_row + n_halved; colH[1][1] = first_col + n_halved;
  if( (hole_row >= first_row + n_halved) && (hole_col >= first_col + n_halved) ) {
     rowH[1][1] = hole_row; colH[1][1] = hole_col;
     board[first_row + n_halved-1][first_col + n_halved-1] = '2';
     board[first_row + n_halved][first_col + n_halved-1] = 'S';
     board[first_row + n_halved-1][first_col + n_halved] = 'E';
  }
  for(int i = 0; i<=1; i++)
    for(int j = 0; j<=1; j++)
      fillBoard(firstRow[i][j], firstCol[i][j], lastRow[i][j], lastCol[i][j], rowH[i][j], colH[i][j]);
}  


int main() {
   #ifdef EVAL
     freopen("input.txt", "r", stdin);
     freopen("output.txt", "w", stdout);
   #endif

   cin >> K >> hole_row >> hole_col;
   N = pow2( K );

   for(int i = 0; i<N; i++)
      for(int j = 0; j<N; j++)
	board[i][j] = '0';   // Character '0' labels the empty cells.

   fillBoard(0, 0, N-1, N-1, hole_row, hole_col);
   for(int i = 0; i<N; i++) {
     for(int j = 0; j<N; j++)
       cout << board[i][j];
     cout << endl;
   }  
}
