# !/usr/bin/env python3
from sys import stderr

from campo_minato_lib import CampoMinato

if __name__ == "__main__":
    M, N, K = map(int, input().strip().split())
    campo_input = f"{M} {N}\n"
    for i in range(M):
        row = input()
        assert len(row) == N
        campo_input += row + ("\n" if i < M - 1 else "")
    campo = CampoMinato(M=[[True]])
    campo.from_string(campo_input)
    print(campo.rank_safe(K))


