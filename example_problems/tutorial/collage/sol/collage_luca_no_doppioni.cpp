//MODIFICATA PER FUNZIONARE ANCHE CON N 1000000
#include <iostream>
#include <fstream>
#include <climits>

using namespace std;

const int NMAX=1000;

int m[NMAX][NMAX];
int col[NMAX];

int main()
{
#ifdef EVAL
  ifstream in("input.txt");
  ofstream out("output.txt");
  cin.rdbuf(in.rdbuf());
  cout.rdbuf(out.rdbuf());
#endif
  int i,j,k,min,a,n;
  cin>>n;
  int old = 256;
  for(i=0,j=0;i<n;i++)
  {
      cin >> k;
      if ( k != old ) {
          col[j] = k;
          m[0][j++]=1;
          old = k;
      }
  }
  n = j;
  for(i=1;i<n;i++)
      for(j=0;j<n-i;j++)
	{
	  min=INT_MAX;

	  for(k=1;k<=i;k++)
	    if ((a=(m[k-1][j]+m[i-k][j+k]-((col[j]==col[j+i])?1:0)))<min)
	      min=a;
	  m[i][j]=min;
	}
  cout<<m[n-1][0]<<endl;
}
