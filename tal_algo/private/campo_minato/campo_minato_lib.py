#!/usr/bin/env python3

WARNING = """this library is common to a few problems:
../campo_minato_opt_val
../campo_minato_via
../triangolo_count_opt_sol
../triangolo_rank_opt_sol
../triangolo_unrank_opt_sol
../triangolo_game_val
../triangolo_game_play
Please, keep this in mind in case you want to modify it."""

from sys import stdin, stdout, stderr
from random import randrange, randint

from functools import lru_cache


class CampoMinato:
    
    def __init__(self, M = None, falling_columns = None, game = False):
        self.is_game = game
        if M is None:
            self.m, self.n = map(int,input().strip().split())
            self.M = []
            for i in range(self.m):
                self.M.append(list(map(int,input().strip().split())))
            if game:
                self.falling_columns = list(map(int,input().strip().split()))
        else:
            self.M = M
            self.m = len(M)
            self.n = len(M[0])
            self.falling_columns = falling_columns

    def as_str(self, with_m_n = True):
        ret = f"{str(self.m)} {str(self.n)}\n" if with_m_n else ""
        ret += "".join(map(lambda x: "." if x else "#", self.M[0]))
        for i in range(1, self.m):
            ret += "\n" + "".join(map(lambda x: "." if x else "#", self.M[i]))
        return ret

    def from_string(self, string):
        self.M = []
        for line in string.split("\n")[1:]:
            self.M.append(list(map(lambda x: True if x == "." else False, line)))
        self.m = len(self.M)
        self.n = len(self.M[0])

    def display(self, out=stderr, with_m_n = True):
        print(self.as_str(with_m_n), file=out, flush=True)

        
    @lru_cache(maxsize=None)
    def num_paths_from_ric_memo(self, r = 0, c = 0):
        assert 0 <= r <= self.m
        assert 0 <= c <= self.n
        if r == self.m:
            return 0
        if c == self.n:
            return 0
        if not self.M[r][c]:
            return 0
        if r == self.m-1 and c == self.n-1:
            return 1
        return self.num_paths_from_ric_memo(r+1, c) + self.num_paths_from_ric_memo(r, c+1)

    @lru_cache(maxsize=None)
    def num_paths_to_ric_memo(self, r, c):
        assert -1 <= r <= self.m
        assert -1 <= c <= self.n
        if r == -1:
            return 0
        if c == -1:
            return 0
        if not self.M[r][c]:
            return 0
        if r == 0 and c == 0:
            return 1
        return self.num_paths_to_ric_memo(r-1, c) + self.num_paths_to_ric_memo(r, c-1)


    def one_path_from(self, r = 0, c = 0):
        assert 0 <= r < self.m
        assert 0 <= c < self.n
        if r == self.m-1 and c == self.n-1:
            return ""
        if r < self.m-1 and self.num_paths_from_ric_memo(r+1, c) > 0:
            return "S" + self.one_path_from(r+1, c)
        return "E" + self.one_path_from(r, c+1)


    def eval_path_unsafe(self, path):
        if len(path) != self.m + self.n - 2:
            return False, f"Your solution:\n{path}\n has length {len(path)}. We were expecting a string of length {self.m + self.n - 2 =} over the alphabet {{'S','E'}} as the input grid had {self.m=} rows and {self.n=} columns."
        r = 0; c = 0
        val_sol = int(self.M[r][c])
        while c+r < self.m + self.n -2:
            if path[c+r] not in {'S','E'}:
                return False, f"Your solution:\n{path}\n contains the character '{path[r]}' in position {r} while we were expecting a string over the alphabet {{'S','E'}}."
            if path[c+r] == 'E':
                c += 1
                if c == self.n:
                    return False, f"Your solution:\n{path}\n leads to exit the grid towards the East after {r+c} steps."
            else:
                r += 1
                if r == self.m:
                    return False, f"Your solution:\n{path}\n leads to exit the grid towards the South after {r+c} steps."
            if not self.M[r][c]:
                return False, f"Your solution:\n{path}\n leads to a forbidden cell after {r+c} steps."
            val_sol += int(self.M[r][c])
        return True, val_sol


    def unrank_safe(self, rnk):
        path = "";  r = 0; c = 0
        while r+c < self.m + self.n -2:
            #print(f"{r=}, {c=}, {rnk=}, num_paths_from_ric_memo((M,r,c)",file=stderr)
            assert 0 <= rnk < self.num_paths_from_ric_memo(r, c)
            if r == self.m -1:
                path += "E"; c += 1
            else:
                if rnk < self.num_paths_from_ric_memo(r+1, c):
                    path += "S"; r += 1
                else:
                    rnk -= self.num_paths_from_ric_memo(r+1,c); path += "E"; c += 1
        assert rnk == 0
        return path

    def rank_safe(self, path):
        ok, val_of_path = self.eval_path_unsafe( path)
        if not ok:
            return False,val_of_path
        rnk = 0; c = 0
        for r in range(self.n-1):
            if path[r] == "R":
                if self.max_val(self.M, r, c) == self.M[r][c] + self.max_val(r+1, c):
                    rnk += self.num_paths_from_ric_memo(r+1, c)
                c += 1
        return True, rnk


if __name__ == "__main__":
    print(WARNING)    
    
