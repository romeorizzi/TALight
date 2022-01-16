#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

int main() {
  const size_t BUFFER_SIZE = 4096;
  char line[BUFFER_SIZE];
  int n;
  setvbuf(stdout, NULL, _IOLBF, BUFFER_SIZE);
  while(true) {
    fgets(line, BUFFER_SIZE, stdin);
    fprintf(stderr, "# BOT> got line=%s", line);
    if(strncmp(line, "# WE HAVE FINISHED", 18) == 0) {
      break;
    } else if(strlen(line) == 0 || line[0] == '#') {
      continue;
    } else {
      sscanf(line, "%d", &n);
      printf("%d 0\n", n);
    }
  }
  return 0;
}
