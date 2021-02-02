#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <inttypes.h>

uint64_t rabin_karp(const char* ASCII_string) {
    uint64_t hash = 0;
    size_t size = strlen(ASCII_string);
    for(size_t i = 0; i < size; i++) {
        hash = hash * 257ULL + ASCII_string[i];
    }
    return hash;
}

int main() {
   char* ENV_s = getenv("TAL_clean_string");
   if(ENV_s!=NULL) {
     printf("h(%s)=\n", ENV_s);
     uint64_t h = rabin_karp(ENV_s);
     printf("%" PRIu64 "\n", h);
   }
   else {
     char str[100];
     printf("Poichè non hai specificato il parametro 'clean_string', ti chiediamo di immettere ora la stringa in chiaro, di cui computare l'hash:\n");
     scanf("%s",str);
     printf("h(%s)=\n", str);
     uint64_t h = rabin_karp(str);
     printf("%" PRIu64 "\n", h);
   }
   exit(0);
}
