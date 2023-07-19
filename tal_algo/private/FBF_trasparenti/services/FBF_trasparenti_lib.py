#!/usr/bin/env python3
from sys import stderr

def recognize(formula_of_parentheses):
    """If the formula is not an FBF print out the reason and return False, None.
       If the FBF is not transparent  print out the reason and return True, False.
       Otherwise, return True, True."""
    assert type(formula_of_parentheses)==str
    num_dangling_open = 0
    for char, i in zip(formula_of_parentheses,range(1,len(formula_of_parentheses)+1)):
        if char == '(':
            num_dangling_open += 1
        else:
            if num_dangling_open == 0:
                print("Houston, we have a problem. The following formula is not well formed:")
                print(formula_of_parentheses)
                print(f"Indeed on position {i} there is no open parenthesis left to be closed:")
                print(formula_of_parentheses)
                print(" "*(i-1),end="")
                print('^ unmatched ")"')
                return False, None
            num_dangling_open -= 1

    if num_dangling_open > 0:
        print("Houston, we have a problem. The following formula is not well formed:")
        print(formula_of_parentheses)
        print(f"Indeed {num_dangling_open} open parenthesis are left unclosed. The formula contains more '(' than ')' characters.")
        return False, None

    # the given formula_of_parentheses is an FBF.
    # let us check whether it is transparent:

    n = len(formula_of_parentheses) // 2
    level = 0
    starts_pos_at_level = [ [] for _ in range(n) ]
    stops_pos_at_level = [ [] for _ in range(n) ]
    for char, i in zip(formula_of_parentheses,range(1,len(formula_of_parentheses)+1)):
        if char == '(':
            starts_pos_at_level[level].append(i)
            level += 1
        else:
            starts_pos_at_level[level] = []
            stops_pos_at_level[level] = []
            level -= 1
            stops_pos_at_level[level].append(i)
            if len(stops_pos_at_level[level]) == 3:
                print("We have a problem. The following FBF formula is not transparent:")
                print(formula_of_parentheses)
                print(f"Indeed, it contains the forbidden pattern (A)(B)(C) where A, B and C are FBFs:")
                print(" ".join(c for c in formula_of_parentheses))
                print("  "*(starts_pos_at_level[level][0]-1),end="(A")
                print("AA"*(stops_pos_at_level[level][0]-starts_pos_at_level[level][0]-1),end=") (B")
                print("BB"*(stops_pos_at_level[level][1]-starts_pos_at_level[level][1]-1),end=") (C")
                print("CC"*(stops_pos_at_level[level][2]-starts_pos_at_level[level][2]-1),end=")\n")
                return True, False
    
    return True, True


class Par:
    def __init__(self, MAX_N_PAIRS):
        self.MAX_N_PAIRS = MAX_N_PAIRS

        # num_wffs[num_pairs] = number of well-formed formula with <num_pairs> pairs of parentheses.

        self.num_wffs = [1] * (MAX_N_PAIRS+1) # while allocating we also set up the correct value for the two base cases
        
        for num_pairs in range(2,MAX_N_PAIRS+1):
            self.num_wffs[num_pairs] = 0
            for n_pairs_included in range(num_pairs):
                self.num_wffs[num_pairs] += self.num_wffs[n_pairs_included] * self.num_wffs[num_pairs - n_pairs_included -1]

        # num_twffs[num_pairs] = number of transparent well-formed formula with <num_pairs> pairs of parentheses.
        # num_twffs1root[num_pairs] = number of transparent well-formed formula with <num_pairs> pairs of parentheses and where the very first open parenthesis is matched with the very last closed parenthesis.
        self.num_twffs = [1] * (MAX_N_PAIRS+1) # while allocating we also set up the correct value for the two base cases
        self.num_twffs1root = [1] * (MAX_N_PAIRS+1) # while allocating we also set up the correct value for the two base cases
        
        for num_pairs in range(2,MAX_N_PAIRS+1):
            self.num_twffs1root[num_pairs] = self.num_twffs[num_pairs-1]
            self.num_twffs[num_pairs] = self.num_twffs1root[num_pairs]
            for n_pairs_included in range(num_pairs-1):
                self.num_twffs[num_pairs] += self.num_twffs[n_pairs_included] * self.num_twffs1root[num_pairs - n_pairs_included -1]

                
    def unrankFBF_t(self, n_pairs, rank):
        if n_pairs == 0:
            return ""
        """(  ... )  ...
               A      B
        """    
        count = 0
        for n_pairs_in_A in reversed(range(n_pairs)):
            num_A = self.num_twffs[n_pairs_in_A]
            num_B = self.num_twffs1root[n_pairs - n_pairs_in_A -1]
            if count + num_A*num_B > rank:
                break
            count += num_A*num_B
        if n_pairs_in_A == n_pairs -1:
            ret = "(" + self.unrankFBF_t(n_pairs_in_A, (rank-count) // num_B) + ")"
        elif n_pairs_in_A == n_pairs -2:
            ret = "(" + self.unrankFBF_t(n_pairs_in_A, (rank-count) // num_B) + ")()"
        else:            
            ret = "(" + self.unrankFBF_t(n_pairs_in_A, (rank-count) // num_B) + ")(" + self.unrankFBF_t(n_pairs - n_pairs_in_A -2, (rank-count) % num_B) + ")"
        #print(f"call to unrankFBF_t({n_pairs=}, {rank=}) ==> {ret=}, {num_A=}, {num_B=}, {n_pairs_in_A=}, {count=}", file=stderr)
        return ret

    def rankFBF_t(self, wff):
        if wff == "":
            return 0
        num_dangling_open = 0
        for char, i in zip(wff,range(len(wff))):
            if char == '(':
                num_dangling_open += 1
            else:
                num_dangling_open -= 1
                if num_dangling_open == 0:
                    break
        assert  i%2 == 1
        """
           (  ... )  ...    with len(A) even
           0   A  i    B
        """
        n_pairs = len(wff)//2
        count = 0
        for ii in range(i+2, len(wff)+1, 2):
            n_pairs_A = ii//2
            n_pairs_B = n_pairs - n_pairs_A -1
            num_A = self.num_twffs[n_pairs_A]
            num_B = self.num_twffs1root[n_pairs_B]
            count += num_A*num_B
        n_pairs_A = i//2
        n_pairs_B = n_pairs - n_pairs_A -1
        num_B = self.num_twffs1root[n_pairs_B]
        return count + self.rankFBF_t(wff[1:i])*num_B + self.rankFBF_t(wff[i+1:len(wff)+1])

    def unrankFBF(self, n_pairs, rank):
        if n_pairs == 0:
            return ""
        """(  ... )  ...
               A      B
        """    
        count = 0
        for n_pairs_in_A in reversed(range(n_pairs)):
            num_A = self.num_wffs[n_pairs_in_A]
            num_B = self.num_wffs[n_pairs - n_pairs_in_A -1]
            if count + num_A*num_B > rank:
                break
            count += num_A*num_B
        return "(" + self.unrankFBF(n_pairs_in_A, (rank-count) // num_B) + ")" + self.unrankFBF(n_pairs - n_pairs_in_A -1, (rank-count) % num_B)

    def rankFBF(self, wff):
        if wff == "":
            return 0
        num_dangling_open = 0
        for char, i in zip(wff,range(len(wff))):
            if char == '(':
                num_dangling_open += 1
            else:
                num_dangling_open -= 1
                if num_dangling_open == 0:
                    break
        assert  i%2 == 1
        """
           (  ... )  ...    with len(A) even
           0   A  i    B
        """
        n_pairs = len(wff)//2
        count = 0
        for ii in range(i+2, len(wff)+1, 2):
            n_pairs_A = ii//2
            n_pairs_B = n_pairs - n_pairs_A -1
            num_A = self.num_wffs[n_pairs_A]
            num_B = self.num_wffs[n_pairs_B]
            count += num_A*num_B
        n_pairs_A = i//2
        n_pairs_B = n_pairs - n_pairs_A -1
        num_B = self.num_wffs[n_pairs_B]
        return count + self.rankFBF(wff[1:i])*num_B + self.rankFBF(wff[i+1:len(wff)+1])


if __name__ == "__main__":
    p = Par(1000)
    assert p.rankFBF("(())") == 0
    assert p.rankFBF("()()") == 1

    assert p.rankFBF("((()))") == 0
    assert p.rankFBF("(()())") == 1
    assert p.rankFBF("(())()") == 2
    assert p.rankFBF("()(())") == 3
    assert p.rankFBF("()()()") == 4

    for n_pairs in range(5):
        print(f"{n_pairs=}, {p.num_wffs[n_pairs]=}")
        for r in range(p.num_wffs[n_pairs]):
            print(f"{p.unrankFBF(n_pairs, r)=}")
            assert p.rankFBF(p.unrankFBF(n_pairs, r)) == r

    for n_pairs in range(5):
        print(f"{n_pairs=}, {p.num_twffs[n_pairs]=}")
        for r in range(p.num_twffs[n_pairs]):
            print(f"{p.unrankFBF_t(n_pairs, r)=}")
            assert p.rankFBF_t(p.unrankFBF_t(n_pairs, r)) == r
