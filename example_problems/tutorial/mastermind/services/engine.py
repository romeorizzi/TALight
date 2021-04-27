from random import seed
from random import randint

def check(sol : str, mine : str):
    solarray = sol.split(" ")
    minearray = mine.split(" ")

    pos = 0
    col = 0

    for x in range(0, len(solarray)):
        if (solarray[x] == minearray[x]):
            pos = pos + 1
            solarray[x] = '0'
            minearray[x] = '0'

    for x in range(0, len(solarray)):
        f = False

        for y in range(0, len(solarray)):
            if not x == y and not solarray[x] == '0' and not minearray[y] == '0' and not f:
                if (solarray[x] == minearray[y]):
                    col = col + 1
                    solarray[x] = '0'
                    minearray[y] = '0'
                    f = True
                    
    return pos, col

def generatesol(n : int, max : int):
    s = ""
    for i in range(0, n):
        s = s + " " + chr(65 + randint(0, max - 1))

    return s.strip()

def play(lensol : int, numchar : int, step : int):
    sol = generatesol(lensol, numchar)

    t = 0
    while t < step:
        line = input()
        pos, col = check(sol, line)

        print(pos, col, sep=' ')
        if (pos == numchar):
            print('WIN')
            break

        t = t + 1

    print(sol)
    return 1

def main():
    play(4, 4, 10)

if __name__ == "__main__":
    main()
    