#include"assert.h"
#include"stdio.h"

//##########################################
// BEGIN: modifica entro quest'area

int num_mosse(int n) {
    return 43;
}

int mossa(int n) {
  assert(n > 0);
  return 1;
}

// END: modifica entro quest'area
// ################################################


int main() {
  int p, n;
  scanf("%d %d",&p, &n);
  assert(p >= 1);
  assert(p <= 2);
  assert(n >= 0);
  if(p  == 1)
    printf("%d\n",num_mosse(n));
  if(p  == 2)
    printf("%d\n",mossa(n));

  return 0;
}
