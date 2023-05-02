import sys
import random


H = 0   # horizontal placement of a tile
V = 1   # vertical placement of a tile

def is_tilable(m, n):
   return 1 - (m%2)*(n%2)

def compose_tiling(m, n, place_tile):
   assert m*n >= 2
   violate_border = random.choice([N,S,W,E])
   if violate_border in [N,S]:
      violate_pos = random.randint(1, n)
      if violate_border == N:
          place_tile(-1,violate_pos,H)
      else:
          place_tile(m,violate_pos,H)
   if violate_border in [W,E]:
      violate_pos = random.randint(1, m)
      if violate_border == W:
          place_tile(violate_pos,-1,H)
      else:
          place_tile(violate_pos,n,H)
