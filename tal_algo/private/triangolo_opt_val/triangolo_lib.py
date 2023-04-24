#!/usr/bin/env python3

WARNING = """this library is common to a few problems:
../triangolo_opt_val
../triangolo_opt_sol
../triangolo_count_opt_sol
../triangolo_rank_opt_sol
../triangolo_unrank_opt_sol
../triangolo_game_val
../triangolo_game_play
Please, keep this in mind in case you want to modify it."""

from sys import stdin, stdout, stderr
from random import randrange, randint

from functools import lru_cache


class Triangolo:
    
    def __init__(self, T = None, chooser = None, game = False):
        self.is_game = game
        if T is None:
            self.n = int(input())
            self.T = []
            for i in range(self.n):
                self.T.append(list(map(int, input().strip().split())))
            if game:
                self.chooser = list(map(int, input().strip().split()))
        else:
            self.T = T
            self.n = len(T)
            self.chooser = chooser

    def as_str(self, with_n = True):
        ret = f"{str(self.n)}\n" if with_n else ""
        ret += str(self.T[0][0])
        for i in range(1,self.n):
            ret += "\n" + " ".join(map(str, self.T[i]))
        if self.is_game:
            ret += "\n" + " ".join(map(str, self.chooser))
        return ret

    def display(self, out=stderr, with_n = True):
        print(self.as_str(with_n), file=out, flush=True)
        
    @lru_cache(maxsize=None)
    def max_val_ric_memo(self, r = 0, c = 0):
        assert 0 <= c <= r <= self.n
        if r == self.n:
            return 0
        return self.T[r][c] + max(self.max_val_ric_memo(r+1, c), self.max_val_ric_memo(r+1, c+1))

    @lru_cache(maxsize=None)
    def num_opt_sols_ric_memo(self, r = 0, c = 0):
        assert 0 <= c <= r < self.n
        if r == self.n -1:
            return 1
        risp = 0
        if self.max_val_ric_memo(r, c) == self.T[r][c] + self.max_val_ric_memo(r+1, c):
            risp += self.num_opt_sols_ric_memo(r+1, c)
        if self.max_val_ric_memo(r, c) == self.T[r][c] + self.max_val_ric_memo(r+1, c+1):
            risp += self.num_opt_sols_ric_memo(r+1, c+1)
        return risp


    @lru_cache(maxsize=None)
    def game_val_ric_memo(self, r = 0, c = 0):
        assert 0 <= c <= r < self.n
        if r == self.n-1:
            #print(f"called with {r=},{c=} returns {self.T[r][c]=}", file=stderr)
            return self.T[r][c]
        if self.chooser[r] == 1:
            risp = self.T[r][c] + max(self.game_val_ric_memo(r+1, c), self.game_val_ric_memo(r+1, c+1))
        else:
            risp = self.T[r][c] + min(self.game_val_ric_memo(r+1, c), self.game_val_ric_memo(r+1, c+1))
        #print(f"called with {r=},{c=} returns {risp=}", file=stderr)
        return risp


    def play(self, player = 0, opt_play = True):
        r = 0; c = 0; path = ""; path_val = self.T[r][c]
        while r < self.n-1:
            if self.chooser[r] != player:
                next_move = input().strip()
            else:
                if self.T[r][c] == self.game_val_ric_memo(r, c) - self.game_val_ric_memo(r+1, c):
                    next_move = 'L'
                else:
                    next_move = 'R'
                print(next_move, flush=True);
            r += 1; c += 1 if next_move == 'R' else 0;
            path += next_move; path_val += self.T[r][c]
        return path, path_val

        
    def opt_sol(self):
        sol = ""; r = 0; c = 0
        while r+1 < self.n:
            if self.max_val_ric_memo(r+1, c) >= self.max_val_ric_memo(r+1, c+1):
                sol += "L"; r += 1
            else:
                sol += "R"; r += 1; c += 1
        return sol

    
    def unrank_safe(self, rnk):
        path = ""; c = 0
        for r in range(self.n-1):
            #print(f"{r=}, {c=}, {rnk=}, num_opt_sols_ric_memo(r,c)", file=stderr)
            assert 0 <= rnk < self.num_opt_sols_ric_memo(r, c)
            if self.max_val_ric_memo(r, c) > self.T[r][c] + self.max_val_ric_memo(r+1, c):
                path += "R"; c += 1
            else:
                assert self.max_val_ric_memo(r, c) == self.T[r][c] + self.max_val_ric_memo(r+1, c)
                if rnk < self.num_opt_sols_ric_memo(r+1, c):
                    path += "L"
                else:
                    rnk -= self.num_opt_sols_ric_memo(r+1, c); path += "R"; c += 1
        assert rnk == 0
        return path

    
    def rank_safe(self, opt_path):
        rnk = 0; c = 0
        for r in range(self.n -1):
            if opt_path[r] == "R":
                if self.max_val_ric_memo(r, c) == self.T[r][c] + self.max_val_ric_memo(r+1, c):
                    rnk += self.num_opt_sols_ric_memo(r+1, c)
                c += 1
        return rnk

    
    def rank_unsafe(self, path, stated_opt_val):
        ok, val_of_path = self.eval_sol_unsafe(path)
        if not ok:
            return False, val_of_sol
        if stated_opt_val != val_of_path:
            return False, f"On input:\n{self.n}\n{self.as_str()}\nyou claimed that {stated_opt_val} is the optimum value of a solution. However, you then provided a solution whose value is {val_of_path} rather then {stated_opt_val}.\nThe solution you have provided is:\n{path}"
        opt_val = self.max_val_ric_memo()
        assert val_of_path <= opt_val
        if val_of_path < opt_val:
            return False, f"On input:\n{self.n}\n{self.as_str()}\nyou claimed that {val_of_path} is the optimal value. However, the optimal value is {opt_val}.\nIndeed, consider the following descending path:\n{self.opt_sol()}"
        rnk = 0; c = 0
        for r in range(self.n-1):
            if path[r] == "R":
                if self.max_val_ric_memo(r, c) == self.T[r][c] + self.max_val_ric_memo(r+1, c):
                    rnk += self.num_opt_sols_ric_memo(r+1, c)
                c += 1
        return True, rnk

    
    def eval_sol_unsafe(self, sol):
        if len(sol) != self.n -1:
            return False, f"Your solution:\n{sol}\n has length {len(sol)}. We were expecting a string of length {self.n-1=} over the alphabet {{'L','R'}} as the input triangle had {self.n=} rows."
        r = 0; c = 0
        val_sol = self.T[r][c]
        while r+1 < self.n:
            if sol[r] not in {'L','R'}:
                return False, f"Your solution:\n{sol}\n contains the character '{sol[r]}' in position {r} while we were expecting a string over the alphabet {{'L','R'}}."
            if sol[r] == 'R':
                c += 1
            r += 1
            val_sol += self.T[r][c]
        return True, val_sol


if __name__ == "__main__":
    print(WARNING)    
    
