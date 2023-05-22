#!/usr/bin/env python3
import random 

def recognize(tiling, TAc, LANG):
    pos = 0
    n_tiles = 0
    while pos < len(tiling)-1:
        if tiling[pos] != '[':
            TAc.print(tiling, "yellow", ["underline"])
            TAc.print(LANG.render_feedback("wrong-tile-opening", f'No. The tile in position {n_tiles+1} does not start with "[" (it starts with "{tiling[pos]}" instead). Your tiling is not correctly encoded.'), "red", ["bold"])
            return False
        n_tiles += 1
        if tiling[pos+1] == ']':
            pos += 2
        else:
            if pos+3 < len(tiling) and tiling[pos+3] != ']':
                if tiling[pos+2] == ']':
                    TAc.print(tiling, "yellow", ["underline"])
                    TAc.print(LANG.render_feedback("wrong-tile-closing", f'No. The tile in position {n_tiles}, starting with "{tiling[pos:pos+2]}", can only be of the following type: "[]" or "[--]". Your tiling is not correctly encoded.'), "red", ["bold"])
                else:
                    TAc.print(tiling, "yellow", ["underline"])
                    TAc.print(LANG.render_feedback("wrong-tile-closing", f'No. The tile in position {n_tiles}, starting with {tiling[pos:pos+3]}, can only be of the following type: "[]" or "[--]". Your tiling is not correctly encoded.'), "red", ["bold"])
                return False
            for pos_fill in {pos+1,pos+2}:
                if tiling[pos_fill] in {'[',']'}:
                    TAc.print(tiling, "yellow", ["underline"])
                    TAc.print(LANG.render_feedback("wrong-tile-filling", f'No. The tile in position {n_tiles}, starting with "{tiling[pos:pos+2]}", can only be of the following type: "[]" or "[--]". Your tiling is not correctly encoded.'), "red", ["bold"])
                    return False
            pos += 4
    if pos+1==len(tiling):
        TAc.print(tiling, "yellow", ["underline"])
        TAc.print(LANG.render_feedback("wrong-tile-closing", f'No. The tile in position {n_tiles+1}, namely "{tiling[pos]}" must be deleted or replaced with suitable tiling ("[]" or "[--]").'), "red", ["bold"])
        return False
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

    def unrank(self,n_tiles,pos,sorting_criterion):
        assert pos>0 and pos<=self.num_sol(n_tiles), 'the position must be between 1 and '+str(self.num_sol(n_tiles))
        if n_tiles==0:
            return '-'
        if n_tiles==1:
            return '[]'
        if sorting_criterion=='loves_long_tiles':
            pos=self.num_sol(n_tiles)-pos+1
        count=n_tiles
        solu=''
        while count>1:
            if pos<=self.num_sol(count-1):
                solu+='[]'
                count-=1
            else:
                solu+='[--]'
                pos-=self.num_sol(count-1)
                count-=2
        if count%2==1:
            solu+='[]'
        return solu

    def rank(self, wff,sorting_criterion):
        count=len(wff)//2
        if count==0 or count==1:
            return 1
        pos=1
        a=0
        while pos<len(wff):
            if wff[pos]==']':
                pos+=2
                count-=1
            else:
                a+=self.num_sol(count-1)
                pos+=4
                count-=2
        if sorting_criterion=='loves_short_tiles':
            return a+1
        elif sorting_criterion=='loves_long_tiles':
            return self.num_sol(len(wff)//2)-a

    def rand_gen(self, n_tiles, seed=None):
        """ritorna una wff pseudo-rando di un corridoio 1 x n_tiles. Il seed la determina univocamente."""
        random.seed(seed)
        r = random.randrange(1,self.num_sol(n_tiles)+1)
        return self.unrank(n_tiles,r,'loves_short_tiles')

    def next(self, wff, sorting_criterion):
        n_tiles = len(wff)//2
        r = self.rank(wff,sorting_criterion)
        return self.unrank(n_tiles,r+1,sorting_criterion)

if __name__ == "__main__":
    p = Par(1000)
