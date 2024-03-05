#include <stdio.h>
#include <assert.h>

#define MAXN 1000000

static int N, T;
static int acceso[MAXN + 1], pulsante[MAXN + 1];


void Accendi(int N, int acceso[], int pulsante[]) {
  for(int i=N; i>=1; i--)
    if(acceso[i]==0) {
      pulsante[i] = 1;
      for(int j=1; j<=i; j++)
        if(i%j == 0)
          acceso[j] = 1-acceso[j];
    } else pulsante[i] = 0;
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
