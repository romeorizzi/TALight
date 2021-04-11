#!/usr/bin/env python3
import random 

def recognize(tiling, TAc, LANG):
    #print(f"tiling={tiling}")

    pos = 0
    n_tiles = 0
    while pos < len(tiling):
        if tiling[pos] != '[':
            TAc.print(tiling, "yellow", ["underline"])
            TAc.print(LANG.render_feedback("wrong-tile-opening", f'No. The tile in position {n_tiles+1} does not start with "[" (it starts with "{tiling[pos]}" instead). Your tiling is not correctly encoded.'), "red", ["bold"])
            return False
        n_tiles += 1
        if tiling[pos+1] == ']':
            pos += 2
        else:
            if pos+3 < len(tiling) and tiling[pos+3] != ']':
                TAc.print(tiling, "yellow", ["underline"])
                TAc.print(LANG.render_feedback("wrong-tile-closing", f'No. The tile in position {n_tiles}, starting with {tiling[pos:pos+3]}, does not end wih "]" (it ends with "{tiling[pos+3]}" instead). Your tiling is not correctly encoded.'), "red", ["bold"])
                return False
            for pos_fill in {pos+1,pos+2}:
                if tiling[pos_fill] in {'[',']'}:
                    TAc.print(tiling, "yellow", ["underline"])
                    TAc.print(LANG.render_feedback("wrong-tile-filling", f'No. The tile in position {n_tiles}, starting with {tiling[pos:pos+4]}, has a forbidden filling character (namely, "{tiling[pos_fill]}"). Your tiling is not correctly encoded.'), "red", ["bold"])
                    return False
            pos += 4
    return True

class Par:
    def __init__(self, MAX_N_PAIRS,  nums_modulus=0):
        self.MAX_N_PAIRS = MAX_N_PAIRS
        self.num_wffs = [1]*(MAX_N_PAIRS+1) 
        for n_tiles in range(2,MAX_N_PAIRS+1):
           self.num_wffs[n_tiles] = self.num_wffs[n_tiles-1] + self.num_wffs[n_tiles-2]
           if nums_modulus > 0:
                    self.num_wffs[n_tiles] %= nums_modulus

    def num_sol(self,n_tiles ):
        assert n_tiles  <= self.MAX_N_PAIRS
        return self.num_wffs[n_tiles ]


    def unrank(self,n_tiles):
        if self.num_sol(n_tiles )==1:
            return ['[]']
        if self.num_sol(n_tiles )==2:
            return ['[][]', '[--]']
        solu1=[]
        solu2=[]
        for i in range(self.num_sol(n_tiles -1)):
            solu1.append('[]' + self.unrank(n_tiles -1)[i])
        for j in range(self.num_sol(n_tiles -2)):
            solu2.append('[--]' + self.unrank(n_tiles-2)[j])
        return solu1 + solu2

    def rank(self, wff):
        if wff == "":
            return 0
        n_tiles = len(wff)//2
        pos=self.unrank(n_tiles).index(wff)
        return pos

    def rand_gen(self, n_tiles, seed=None):
        """ritorna una wff pseudo-rando di n-pairs parentesi. Il seed la determina univocamente."""
        random.seed(seed)
        r = random.randrange(self.num_sol(n_tiles))
        return self.unrank(n_tiles)[r]

    def next(self, wff, sorting_criterion):
        n_tiles = len(wff)//2
        r = self.rank(wff)
        if sorting_criterion=='loves_short_tiles':
            solu=self.unrank(n_tiles)[r+1]
        elif sorting_criterion=='loves_long_tiles':
            solu=self.unrank(n_tiles)[r-1]
        return solu

if __name__ == "__main__":
    p = Par(1000)
