#include <stdio.h>
#include <stdlib.h>

static const int H = 0;

static const int V = 1;


int is_tilable(int m, int n);

void compose_tiling(int m, int n, void place_tile(int row, int col, int dir));


int main() {
    // checkpoint
    printf("%d\n", 0);
    // read m, n
    static int n;
    static int m;
    fflush(stdout);
    scanf("%d%d", &m, &n);
    // call res = is_tilable(m, n)
    static int res;
    res = is_tilable(m, n);
    // write res
    printf("%d\n", res);
    // if res {...}
    if (res) {
        // read choice
        static int choice;
        fflush(stdout);
        scanf("%d", &choice);
        // if choice {...}
        if (choice) {
            // read m1, n1
            static int m1;
            static int n1;
            fflush(stdout);
            scanf("%d%d", &m1, &n1);
            // call compose_tiling(m1, n1) callbacks {...}
            {
                void place_tile(int row, int col, int dir) {
                    // callback place_tile
                    printf("%d %d\n", 1, 0);
                    // write row, col, dir
                    printf("%d %d %d\n", row, col, dir);
                }
                compose_tiling(m1, n1, place_tile);
            }
            // no more callbacks
            printf("%d %d\n", 0, 0);
        }
    }
    // exit
    exit(0);
}
