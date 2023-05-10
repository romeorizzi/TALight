#!/usr/bin/env python3

def num_paths(M):
    m = len(M)
    n = len(M[0])
    num_paths_from = [[0] * (n + 1) for i in range(m + 1)]
    num_paths_from[m - 1][n - 1] = int(M[m - 1][n - 1])
    for i in reversed(range(m)):
        for j in reversed(range(n)):
            if i == m - 1 and j == n - 1:
                continue
            if M[i][j]:
                num_paths_from[i][j] = num_paths_from[i + 1][j] + num_paths_from[i][j + 1]
    return num_paths_from[0][0]

if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        n, m = map(int, input().strip().split())
        M = list(map(lambda x: [y == "." for y in x], [input() for i in range(n)]))
        print(num_paths(M))
