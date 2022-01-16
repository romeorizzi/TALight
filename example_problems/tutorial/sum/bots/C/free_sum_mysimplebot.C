#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main() {
   char *spoon = NULL;  /* forces getline to allocate with malloc */ 
   size_t len = 0;     /* ignored when line = NULL */
   while(1) {
      free(spoon);
      spoon = NULL;  /* forces getline to allocate with malloc */
      ssize_t read = getline(&spoon, &len, stdin);
      //printf("# BOT: spoon='%s'\n", spoon);
      if(spoon[0] == '#') {  // spoon contains a commented line from the service server
         spoon[18] = '\0';
         if(strcmp(spoon, "# WE HAVE FINISHED") == 0)
            return 0;   // exit upon termination of the service server
      }
      else {
         int n = atoi(spoon);
         printf("%d 0\n", n);
      }
  }
}

