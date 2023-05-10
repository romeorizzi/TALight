import sys

H = 0   # horizontal placement of a tile
V = 1   # vertical placement of a tile

def is_tilable(m, n):
   return 1 - (m%2)*(n%2)

def compose_tiling(m, n, place_tile):
   assert m*n >= 2
   if n >= m:
       if n==2:
          place_tile(m,1,H)
          place_tile(m,1,H)
       else:
          place_tile(m,n//2,H)
          place_tile(m,n//2+1,H)
   else:   # m > n
       if m==2:
          place_tile(1,n,V)
          place_tile(1,n,V)
       else:
          place_tile(m//2,n,V)
          place_tile(m//2+1,n,V)
