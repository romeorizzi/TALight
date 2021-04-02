#!/usr/bin/env python3
import random

def recognize(treatement, TAc, LANG, yield_feedback=True):
    assert type(treatement)==str
    #print(f"treatement={treatement}")
    num_dangling_broken_pills = 0
    for char, i in zip(treatement,range(1,len(treatement)+1)):
        if char == 'I':
            num_dangling_broken_pills += 1
        else:
            if num_dangling_broken_pills == 0:
                if yield_feedback:
                    TAc.print(treatement, "yellow", ["underline"])
                    TAc.print(LANG.render_feedback("unfeasible", f"No. On position {i} there is no broken pill left to be eaten. This prescription is not consistent."), "red", ["bold"])
                    TAc.print(treatement, "yellow", ["underline"])
                    print(" "*(i-1),end="")
                    TAc.print("^ no 'H' is available at this point", "yellow", ["underline"])
                return False
            num_dangling_broken_pills -= 1

    if num_dangling_broken_pills > 0:
        if yield_feedback:
            TAc.print(treatement, "yellow", ["underline"])
            TAc.print(LANG.render_feedback("unfinished", f"No. There are {num_dangling_broken_pills} broken pills left over in the flask. This prescription is not consistent. It contains more 'I' than 'H' characters."), "red", ["bold"])
        return False
    return True


class Flask:
    def __init__(self, MAX_N, nums_mod=0):
        self.MAX_N = MAX_N

        # num_sols[n_pills] = number of feasible treatment with <n_pills> pills.
        # A treatment with n pills is a string of n 'I' characters and n 'H' characters such that no prefix contains more 'H's than 'I's and every 'I' matches with the first 'H' after it that brings back the balance.
        self.num_sols = [1] * (MAX_N+1) # while allocating it we also set up the correct value for the two base cases
        
        for n in range(2,MAX_N+1):
            self.num_sols[n] = 0
            for n_pills_included in range(n):
                self.num_sols[n] += self.num_sols[n_pills_included] * self.num_sols[n - n_pills_included -1]
                if nums_mod > 0:
                    self.num_sols[n] %= nums_mod

    def num_sol(self, n):
        assert n <= self.MAX_N
        return self.num_sols[n]

    def unrank(self, n_pills, pos, sorting_criterion="lovesI"):
        if n_pills == 0:
            return ""
        """I  ... H  ...
               A      B
        """    
        count = 0
        for n_pills_in_A in range(n_pills) if sorting_criterion=="lovesH" else reversed(range(n_pills)):
            num_A = self.num_sol(n_pills_in_A)
            num_B = self.num_sol(n_pills - n_pills_in_A -1)
            if count + num_A*num_B > pos:
                break
            count += num_A*num_B
        return "I" + self.unrank(n_pills_in_A, (pos-count) // num_B, sorting_criterion) + "H" + self.unrank(n_pills - n_pills_in_A -1, (pos-count) % num_B, sorting_criterion)

    def rank(self, treatment, sorting_criterion="lovesI"):
        if treatment == "":
            return 0
        num_dangling_broken_pills = 0
        for char, i in zip(treatment,range(len(treatment))):
            if char == 'I':
                num_dangling_broken_pills += 1
            else:
                num_dangling_broken_pills -= 1
                if num_dangling_broken_pills == 0:
                    break
        assert  i%2 == 1
        """
           I  ... H  ...    with len(A) even
           0   A  i    B
        """
        n_pills = len(treatment)//2
        count = 0
        if sorting_criterion=="lovesI":
            for ii in range(i+2, len(treatment)+1, 2):
                n_pills_A = ii//2
                n_pills_B = n_pills - n_pills_A -1
                num_A = self.num_sol(n_pills_A)
                num_B = self.num_sol(n_pills_B)
                count += num_A*num_B
        if sorting_criterion=="lovesH":
            for ii in range(1, i-1, 2):
                n_pills_A = ii//2
                n_pills_B = n_pills - n_pills_A -1
                num_A = self.num_sol(n_pills_A)
                num_B = self.num_sol(n_pills_B)
                count += num_A*num_B
        n_pills_A = i//2
        n_pills_B = n_pills - n_pills_A -1
        num_B = self.num_sol(n_pills_B)
        return count + self.rank(treatment[1:i], sorting_criterion)*num_B + self.rank(treatment[i+1:len(treatment)+1], sorting_criterion)

    def rand_gen(self, n_pills, seed=None):
        """returns a pseudo-random treatment with <n> I's and H's. The seed univokely determines the treatment."""
        random.seed(seed)
        r = random.randrange(self.num_sol(n_pills))
        return self.unrank(n_pills, r)
    
    def next(self, treatment, sorting_criterion="lovesI"):
        n_pills = len(treatment) // 2
        r = self.rank(treatment, sorting_criterion)
        assert r < self.num_sol(n_pills) -1
        return self.unrank(n_pills, r+1, sorting_criterion)

if __name__ == "__main__":
    p = Flask(1000)
    assert p.rank("IIHH", 'lovesI') == 0
    assert p.rank("IHIH", 'lovesI') == 1
    assert p.rank("IIHH", 'lovesH') == 1
    assert p.rank("IHIH", 'lovesH') == 0

    assert p.rank("IIIHHH", 'lovesI') == 0
    assert p.rank("IIHIHH", 'lovesI') == 1
    assert p.rank("IIHHIH", 'lovesI') == 2
    assert p.rank("IHIIHH", 'lovesI') == 3
    assert p.rank("IHIHIH", 'lovesI') == 4

    assert p.rank("IIIHHH", 'lovesH') == 4
    assert p.rank("IIHIHH", 'lovesH') == 3
    assert p.rank("IIHHIH", 'lovesH') == 2
    assert p.rank("IHIIHH", 'lovesH') == 1
    assert p.rank("IHIHIH", 'lovesH') == 0

    for n in range(5):
        for r in range(p.num_sol(n)):
            assert p.rank(p.unrank(n, r)) == r
        for _ in range(5):
            #print(p.rand_gen(n))
            assert p.rand_gen(n, _ + 5*n) == p.rand_gen(n, _ + 5*n)
