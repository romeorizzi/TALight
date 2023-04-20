#define NDEBUG
#include<cassert>
#include<fstream>
#ifndef NDEBUG
   #include<iostream>
#endif

using namespace std;

const int MAX_N = 1000;
int outputString[MAX_N]; int posW = 0;

ifstream fin;

void specchio() {
  /*
    Quando la funzione specchi viene chiamata, io sono in un punto qualsiasi della sequenza in input che codifica l'albero in input come da specifiche del problema. Il primo numero ancora da leggere, e' il numero di figli di un certo nodo v. Sia T_v is sottoalbero radicato in v dell'albero in input. I suoi nodi parleranno (dichiarando i figli all'anagrafe) da ora fino ad esurimento (ossia sono su un intervallo contiguo della sequenza in input, e questo sottointervallo inizia proprio ora).
    Al solito, sono esigente con la fatina ricorsina:
    Chiedo a questa procedura di gestire questo intero sottointervallo, accorgendosi lei stessa di quando esso finisca, e di produrre la codifica di T_v nello specchio. Voglio che questa codifica (una sequenza di numeri) venga scritta, rovesciata alla Leonardo,, entro il buffer "outputString" partendo dalla posizione corrente. 
  */
/* se non facessi scrivere la risposta rovesciata, la struttura ricorsiva del problema, dove v e' il nodo radice di T_v e T_1, T_2 e T_3 rappresentano i sottoalberi radicati nei figli,  sarebbe:
   f( v T_1 T_2 T_3) =  v f(T_3) f(T_2) f(T_1) 
  per questioni di efficienza, la sequenza di output la computo rovesciata alla Leonardo, e quindi ho la ricorrenza:

   f^L( v T_1 T_2 T_3) =  f^L(T_1) f^L(T_2) f^L(T_3) v 
*/

  int num_figli_di_v;  fin >> num_figli_di_v;

  //cout << "num_figli_di_v: " << num_figli_di_v << ",  posW = " << posW << endl; 

  for( int i = 0; i < num_figli_di_v; i++)
      specchio();

  outputString[posW++] = num_figli_di_v; 
}

int main() {
  fin.open("input.txt"); assert( fin );
  specchio();
  fin.close();

  ofstream fout("output.txt"); assert( fout );
  while( posW > 0 )
    fout << outputString[--posW] << " ";
  fout << endl;
  fout.close();

  return 0;
}
