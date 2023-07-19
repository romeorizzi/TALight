#!/usr/bin/env python3
from sys import stderr

def recognize(S, seq_of_indices, d=0):
    """If the subsequence of S defined by seq_of_indices is not an increasing sequence except d drops, then print out the reason and return False.
       Otherwise, return True."""
    assert type(seq_of_indices)==list
    assert type(S)==list
    assert type(d)==int
    if len(seq_of_indices) == 0:
        return True
    if len(seq_of_indices) > len(S):
        print("We have a problem: the lenght of your sequence of indexes exceeds the length of S.")
        return False
    drops = []
    if not 0 <= seq_of_indices[0] < len(S):
        print(f"We have a problem: the first index in your sequence of indexes is {seq_of_indices[0]}, which does not belong to the inteval [0,len(S)) = [0,{len(S)}).")
        return False
    curr_val = S[seq_of_indices[0]]
    for i in range(len(seq_of_indices) - 1):
        if not 0 <= seq_of_indices[i+1] < len(S):
            print(f"We have a problem: the {i+1}-th index in your sequence of indexes is {seq_of_indices[i+1]}, which does not belong to the inteval [0,len(S)) = [0,{len(S)}).")
            return False
        if S[seq_of_indices[i+1]] <= S[seq_of_indices[i]]:
            drops.append(f"S[seq_of_indices[{i+1}]]=S[{seq_of_indices[i+1]}]={S[seq_of_indices[i+1]]} <= {S[seq_of_indices[i]]}=S[{seq_of_indices[i]}]=S[seq_of_indices[{i}]]")
        if len(drops) > d:
            print(f"We have a problem: the subsequence of S defined by your sequence of indexes has more than d={d} drops. Namely: {', '.join(drops)}.")
            return False
    return True


class IncrSubseqs:
    def __init__(self, S, d=0):
        self.S = S
        self.d = d
        self.n = len(S)

        # num_starting_in[i], 0<=i<n, := number of increasing sequences of indexes defining an increasing subsequence of S starting in S[i] as their first element.
        # num_nonleft[num_pairs], 0<=i<n, := number of increasing sequences of indexes defining an increasing subsequence of S taking no element to the left of S[i].

        self.num_starting_in = [1] * self.n # while allocating we also set up the correct value for the base case
        self.num_nonleft = [2] * self.n # while allocating we also set up the correct value for the base case (2: the empty seq and the seq [n-1] starting in n-1)
        
        for i in range(self.n-2,-1,-1):
            self.num_starting_in[i] = 1 # just the seq [i]
            for j in range(self.n-1,i,-1):
                if S[j] > S[i]:
                    self.num_starting_in[i] += self.num_starting_in[j]
            self.num_nonleft[i] = self.num_nonleft[i+1] + self.num_starting_in[i]

                
    def rankShadow(self, seq_of_indices):
        r = 0
        last_taken = None
        for i in range(self.n):
            if last_taken is None or last_taken < self.S[i]:
                if i in seq_of_indices:
                    last_taken = self.S[i]
                else:
                    r += self.num_starting_in[i]
        #print(f"rankShadow returns {r=} for {seq_of_indices=}")
        return r
    
    def unrankShadow(self, r):
        assert 0 <= r < self.num_nonleft[0]
        seq_of_indexes = []
        for i in range(self.n):
            if len(seq_of_indexes) == 0 or self.S[seq_of_indexes[-1]] < self.S[i]:
                if self.num_starting_in[i] > r:
                    seq_of_indexes.append(i)
                else:
                    r -= self.num_starting_in[i]
        assert r == 0
        return seq_of_indexes
                        


if __name__ == "__main__":
    for S in [ [1, 2, 3], [2, 3, 4, 1], [5,4,3,2,1] ]:
        n = len(S)
        poldo = IncrSubseqs(S)
        for i in range(n):
            print(f"{i=}, {poldo.num_starting_in[i]=}")
            print(f"{i=}, {poldo.num_nonleft[i]=}")
        for r in range(poldo.num_nonleft[0]):
            print(f"{r=}, {poldo.unrankShadow(r)=}")
            assert poldo.rankShadow(poldo.unrankShadow(r)) == r


