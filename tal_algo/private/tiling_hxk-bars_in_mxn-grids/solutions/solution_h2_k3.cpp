#include<cassert>

static const int H = 0; // horizontal placement of a tile
static const int V = 1; // vertical placement of a tile

int is_tilable(int m, int n, int h, int k) {
  assert(h<=k);
  if( (m < h) || (n < h) )
    return 0;
  if( (m*n) % (h*k) )
    return 0;
   return 1;
} 

void compose_tiling(int m, int n, int h, int k, void place_tile(int row, int col, int dir)) {
  if( (n%2 == 0) && (m%3 == 0) )
    for(int i = 1; i < m; i+=3) //for every strip of 3 raws (deal each strip separately)
        for(int j = 1; j < n; j += 2)
           place_tile(i,j,V);
   else if( (n%3 == 0) && (m%2 == 0) )
       for(int i = 1; i < m; i += 2) //for every strip of 2 raws (deal each strip separately)
         for(int j = 1; j < n; j += 3)
           place_tile(i,j,H);
  // MANCANO ANCORA DEI CASI
}
