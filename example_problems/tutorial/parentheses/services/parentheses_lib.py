#!/usr/bin/env python3
import random

def recognize(formula_of_parentheses, TAc, LANG, yield_feedback=True):
    assert type(formula_of_parentheses)==str
    #print(f"formula_of_parentheses={formula_of_parentheses}")
    num_dangling_open = 0
    for char, i in zip(formula_of_parentheses,range(1,len(formula_of_parentheses)+1)):
        if char == '(':
            num_dangling_open += 1
        else:
            if num_dangling_open == 0:
                if yield_feedback:
                    TAc.print(formula_of_parentheses, "yellow", ["underline"])
                    TAc.print(LANG.render_feedback("unfeasible", f"No. On position {i} there is no open parenthesis left to be closed. This formula is not well formed."), "red", ["bold"])
                    TAc.print(formula_of_parentheses, "yellow", ["underline"])
                    print(" "*(i-1),end="")
                    TAc.print("^ unmatched ')'", "yellow", ["underline"])
                return False
            num_dangling_open -= 1

    if num_dangling_open > 0:
        if yield_feedback:
            TAc.print(formula_of_parentheses, "yellow", ["underline"])
            TAc.print(LANG.render_feedback("unfinished", f"No. You have left {num_dangling_open} open parenthesis unclosed. This formula is not well formed. It contains more '(' than ')' characters."), "red", ["bold"])
        return False
    return True


class Par:
    def __init__(self, MAX_N_PAIRS):
        self.MAX_N_PAIRS = MAX_N_PAIRS

        # num_wffs[num_pairs] = number of well-formed formula with <num_pairs> open parentheses and <num_pairs> closed parentheses correctly matching with them.

        self.num_wffs = [1] * (MAX_N_PAIRS+1) # while allocating w also set up the correct value for the two base cases
        
        for num_pairs in range(2,MAX_N_PAIRS+1):
            self.num_wffs[num_pairs] = 0
            for n_pairs_included in range(num_pairs):
                self.num_wffs[num_pairs] += self.num_wffs[n_pairs_included] * self.num_wffs[num_pairs - n_pairs_included -1] 

    def num_sol(self, num_pairs):
        assert num_pairs <= self.MAX_N_PAIRS
        return self.num_wffs[num_pairs]

    def unrank(self, n_pairs, pos, sorting_criterion="loves_opening_par"):
        if n_pairs == 0:
            return ""
        """(  ... )  ...
               A      B
        """    
        count = 0
        for n_pairs_in_A in range(n_pairs) if sorting_criterion=="loves_closing_par" else reversed(range(n_pairs)):
            num_A = self.num_sol(n_pairs_in_A)
            num_B = self.num_sol(n_pairs - n_pairs_in_A -1)
            if count + num_A*num_B > pos:
                break
            count += num_A*num_B
        return "(" + self.unrank(n_pairs_in_A, (pos-count) // num_B, sorting_criterion) + ")" + self.unrank(n_pairs - n_pairs_in_A -1, (pos-count) % num_B, sorting_criterion)

    def rank(self, wff, sorting_criterion="loves_opening_par"):
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
        if sorting_criterion=="loves_opening_par":
            for ii in range(i+2, len(wff)+1, 2):
                n_pairs_A = ii//2
                n_pairs_B = n_pairs - n_pairs_A -1
                num_A = self.num_sol(n_pairs_A)
                num_B = self.num_sol(n_pairs_B)
                count += num_A*num_B
        if sorting_criterion=="loves_closing_par":
            for ii in range(1, i-1, 2):
                n_pairs_A = ii//2
                n_pairs_B = n_pairs - n_pairs_A -1
                num_A = self.num_sol(n_pairs_A)
                num_B = self.num_sol(n_pairs_B)
                count += num_A*num_B
        n_pairs_A = i//2
        n_pairs_B = n_pairs - n_pairs_A -1
        num_B = self.num_sol(n_pairs_B)
        return count + self.rank(wff[1:i], sorting_criterion)*num_B + self.rank(wff[i+1:len(wff)+1], sorting_criterion)

    def rand_gen(self, n_pairs, seed=None):
        """ritorna una wff pseudo-rando di n-pairs parentesi. Il seed la determina univocamente."""
        random.seed(seed)
        r = random.randrange(self.num_sol(n_pairs))
        return self.unrank(n_pairs, r)
    

if __name__ == "__main__":
    p = Par(1000)
    assert p.rank("(())", 'loves_opening_par') == 0
    assert p.rank("()()", 'loves_opening_par') == 1
    assert p.rank("(())", 'loves_closing_par') == 1
    assert p.rank("()()", 'loves_closing_par') == 0

    assert p.rank("((()))", 'loves_opening_par') == 0
    assert p.rank("(()())", 'loves_opening_par') == 1
    assert p.rank("(())()", 'loves_opening_par') == 2
    assert p.rank("()(())", 'loves_opening_par') == 3
    assert p.rank("()()()", 'loves_opening_par') == 4

    assert p.rank("((()))", 'loves_closing_par') == 4
    assert p.rank("(()())", 'loves_closing_par') == 3
    assert p.rank("(())()", 'loves_closing_par') == 2
    assert p.rank("()(())", 'loves_closing_par') == 1
    assert p.rank("()()()", 'loves_closing_par') == 0

    for n in range(5):
        for r in range(p.num_sol(n)):
            assert p.rank(p.unrank(n, r)) == r
        for _ in range(5):
            #print(p.rand_gen(n))
            assert p.rand_gen(n, _ + 5*n) == p.rand_gen(n, _ + 5*n)
