def num_piastrellature(n):
    assert n >= 0
    if n <= 1:
        return 1
    return num_piastrellature(n-1) + num_piastrellature(n-2)

N = int(input())
print(num_piastrellature(N))















