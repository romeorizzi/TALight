#include <stdio.h>
#include <assert.h>

#define MAXN 1000000

int N, T;
int acceso[MAXN + 1], pulsante[MAXN + 1];


void Accendi(int N, int acceso[], int pulsante[]) {
  for(int i=N; i>=1; i--) {
    for(int m=2*i; m<=N; m+=i)
      if(pulsante[m]==1)
	acceso[i] = 1 - acceso[i];
    pulsante[i] = 1 - acceso[i];
  }
}


int main() {
  assert(1 == scanf("%d", &T));
  for (int t=1; t<=T; t++) {
    fprintf(stderr, "Testcase %d:\n", t);
    assert(1 == scanf("%d", &N));
    for (int i=1; i<=N; i++)
      assert(1 == scanf("%d", acceso + i));

    Accendi(N, acceso, pulsante);

    printf("1\n");
    for (int i=1; i<=N; i++)
      printf("%d ", pulsante[i]);
    printf("\n");
    fflush(stdout);
  }
  return 0;
}
