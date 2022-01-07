#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include "hash_rabin_karp.h"


int main() {
   char* ENV_lang = getenv("TAL_lang");
   char* ENV_white_string = getenv("TAL_white_string");
   char* ENV_hash_type = getenv("TAL_hash_type");
   int   ENV_colored_feedback = (getenv("TAL_META_TTY") == "1");

   // Da aggiugere libreria per supporto dei colori e multilinga ...
   
   if(ENV_white_string!=NULL) {
     uint64_t h = rabin_karp(ENV_white_string);
     printf("%" PRIu64 "\n", h);
   }
   else {
     char str[100];
     printf("Poichè non hai specificato il parametro 'white_string', ti chiediamo di immettere ora la stringa in chiaro, di cui computare l'hash:\n");
     // scanf("%s",str);  but safer w.r.t. possible attacks:
     fgets(str,100,stdin);
     if(str[strlen(str)-1] == '\n')
       str[strlen(str)-1] = '\0';
     if(strlen(str)>64) {
       fprintf(stderr, "Hai immesso una stringa più lunga di 64 caratteri.\n");
       exit(0);
     }
     uint64_t h = rabin_karp(str);
     printf("h(%s) = %" PRIu64 "\n", str, h);
   }
   exit(0);
}
