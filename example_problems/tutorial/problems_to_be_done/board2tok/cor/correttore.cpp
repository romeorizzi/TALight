/*
  Romeo Rizzi
 */

// Assume file di input e file di output non malformati.
#include <cassert>
//#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <fstream>

using namespace std;

ifstream *fin;
ifstream *fcor;
ifstream *fout;


const int MAXK = 10;
const int MAXN = 1024;
const char good[] = "01234NESW";
const int nGoods = 9;
int n, k, hole_row, hole_col;
char board[MAXN][MAXN]; // rows and columns are numbered starting from 0.

int pow2(int exp) {
  assert( exp >= 0 );
  if( exp == 0 ) return 1;
  return 2*pow2( exp -1 );
}


void ex(const char *msg, float res)
{
  if(msg) {
    fprintf(stderr, "%s ", msg);
  }
  printf("%f\n", res);
  exit(0);
}

int num_char_read = 0;
char safe_read_char()
{
  // Legge in maniera sicura un carattera entro l'alfabeto atteso
  char tmp;
  bool done = false;
  while(!done) {
    if (fout->eof()) {
       cerr << "letti e riconosciuti " << num_char_read << " caratteri" << endl;       ex("Fine del file prematura.\n", 0.0f);
 
    }   
    *fout >> tmp;
    if (fout->fail()) {
	cerr << "letti e riconosciuti " << num_char_read << " caratteri" << endl; 
        ex("Output file malformato (safe_read_char)", 0.0f);
    }   
    for(int i = 0; i<nGoods; i++)
       if (tmp == good[i])
          done = true;
    if ( done == false && tmp >= 'a' && tmp <= 'Z') {
	cerr << "letti e riconosciuti " << num_char_read << " caratteri" << endl;
        ex("Output file fuori standard (safe_read_char)", 0.0f);
    }   
  }	
  return tmp;
}

void
check_fine_file()
{
  string x;

  if (fout->eof())
    return;

  *fout >> x;
  if (x != "" || !fout->eof())
    ex("Output malformato (check fine file)", 0.0f);
}


int main(int argc, char *argv[])
{
  if(argc < 4)
    {
      cerr << "Usage: " << argv[0] << " <input> <correct output> <test output>" << endl;
      return 1;
    }

  fin = new ifstream(argv[1]);
  fcor = new ifstream(argv[2]);
  fout = new ifstream(argv[3]);

  if(fin->fail())
    {
      cerr << "Impossibile aprire il file di input " << argv[1] << "." << endl;
      ex("Impossibile aprire il file di input ", 0.0f);
      return 1;
    }
  if(fcor->fail())
    {
      cerr << "Impossibile aprire il file di output corretto " << argv[2] << "." << endl;
      ex("Impossibile aprire il file di output corretto ", 0.0f);
      return 1;
    }
  if(fout->fail()) {
    ex("Impossibile aprire il file di output generato dal codice sottoposto al problema.", 0.0f);
      return 1;
    }

  int k, r, c;
  *fin >> k >> hole_row >> hole_col;
  int n = pow2(k);

  for(int i = 0; i < n; i++)
    for(int j = 0; j < n; j++) {
      board[i][j] = safe_read_char();
      num_char_read++;
    }  

  for(int i = 0; i < n; i++)
    for(int j = 0; j < n; j++) {
      if(i==hole_row && j==hole_col && board[i][j] != '0')
        ex("Non hai lasciato scoperta la cella (r,c) come prescritto.", 0.0f);	
      if( board[i][j] == '0' && (i!=hole_row  || j!=hole_col) )
        ex("Hai lasciato scoperta una cella che dovei coprire.", 0.0f);	
      if( board[i][j] == '1' && board[i][j+1] != 'E' )
        ex("Centro di tipo 1 non trova la sua periferia Est.", 0.0f);	
      if( board[i][j] == '1' && board[i-1][j] != 'N' )
        ex("Centro di tipo 1 non trova la sua periferia Nord.", 0.0f);	
      if( board[i][j] == '2' && board[i][j+1] != 'E' )
        ex("Centro di tipo 2 non trova la sua periferia Est.", 0.0f);	
      if( board[i][j] == '2' && board[i+1][j] != 'S' )
        ex("Centro di tipo 2 non trova la sua periferia Sud.", 0.0f);	
      if( board[i][j] == '3' && board[i][j-1] != 'W' )
        ex("Centro di tipo 3 non trova il suo West.", 0.0f);	
      if( board[i][j] == '3' && board[i+1][j] != 'S' )
        ex("Centro di tipo 3 non trova la sua periferia Sud.", 0.0f);	
      if( board[i][j] == '4' && board[i][j-1] != 'W' )
        ex("Centro di tipo 4 non trova il suo West.", 0.0f);	
      if( board[i][j] == '4' && board[i-1][j] != 'N' )
        ex("Centro di tipo 4 non trova la sua periferia Nord.", 0.0f);	
      if( board[i][j] == 'N' && board[i+1][j] != '4' && board[i+1][j] != '1' )
        ex("Periferia di tipo Nord non riconosciuta dal centro.", 0.0f);	
      if( board[i][j] == 'E' && board[i][j-1] != '1' && board[i][j-1] != '2' )
        ex("Periferia di tipo Est non riconosciuta dal centro.", 0.0f);	
      if( board[i][j] == 'S' && board[i-1][j] != '2' && board[i-1][j] != '3' )
        ex("Periferia di tipo Sud non riconosciuta dal centro.", 0.0f);	
      if( board[i][j] == 'W' && board[i][j+1] != '3' && board[i][j+1] != '4' )
        ex("Periferia di tipo Ovest non riconosciuta dal centro.", 0.0f);	
    }    

  // Se arriva qui la risposta e' corretta.
  
  ex("Corretto", 1.0f);

  return 0;
}
