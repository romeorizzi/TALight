#include <stdio.h>

void individua(long long int n) {
  fscanf(fopen("input.txt", "r"), "%lld", &n);
  denuncia(n);
}
