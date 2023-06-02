#!/usr/bin/env python3
from sys import stderr

from game_eat_left_or_right_lib import sol

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        #print(f"testcase {t}", file=stderr)
        n = int(input())
        V = list(map(int, input().strip().split()))
        f = sol(V)
        fullscore = sum(V)
        i, j = 0, n
        if f(i, j)[0] > fullscore / 2:
            my_turn = 1 # preferisco giocare per primo
        else:
            my_turn = 2 # preferisco giocare per secondo
        print(my_turn, flush=True)
        while i < j:
            if my_turn == 1:
                if f(i, j)[1] == "L":
                    print("L", flush=True)
                    i += 1
                else:
                    print("R", flush=True)
                    j -= 1
            else:
                if input().strip() == "L":
                    i += 1
                else:
                    j -= 1
            my_turn = 3 - my_turn
