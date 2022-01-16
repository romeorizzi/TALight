#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

int main() {
  const size_t BUFFER_SIZE = 4096;
  char line[BUFFER_SIZE];
  int s, d, x1, x2;
  setvbuf(stdout, NULL, _IOLBF, BUFFER_SIZE);
  while(true) {
    fgets(line, BUFFER_SIZE, stdin);
    fprintf(stderr, "# BOT> got line= %s", line);
    if(strncmp(line, "# WE HAVE FINISHED", 18) == 0) {
      break;
    } else if(strlen(line) == 0 || line[0] == '#') {
      continue;
    } else {
      sscanf(line, "%d %d", &s, &d);
      x1 = (s + d) / 2;
      x2 = (s - d) / 2;
      printf("%d %d\n", x1, x2);
    }
  }
  return 0;
}
