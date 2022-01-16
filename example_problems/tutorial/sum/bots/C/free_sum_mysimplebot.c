#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

int main() {
    const size_t BUFFER_SIZE = 4096;
    char buffer[BUFFER_SIZE];
    int n;
    setvbuf(stdout, NULL, _IOLBF, BUFFER_SIZE);
    while(true) {
        fgets(buffer, BUFFER_SIZE, stdin);
        if(strncmp(buffer, "# WE HAVE FINISHED", 18) == 0) {
            break;
        } else if(buffer[0] == '#') {
            continue;
        } else {
            sscanf(buffer, "%d", &n);
            printf("%d 0\n", n);
        }
    }
    return 0;
}
