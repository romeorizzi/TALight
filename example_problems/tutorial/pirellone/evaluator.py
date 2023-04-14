import turingarena as ta 
import random
import tempfile 


def random_pirellone(n, m, solvable=False):
    line = [random.randint(0, 1) for _ in range(m)]
    inv = [int(not x) for x in line]
    pirellone = []
    for _ in range(n):
        if random.randint(0, 1) == 0:
            pirellone.append(line[:])
        else:
            pirellone.append(inv[:])
    if not solvable:
        row = random.randrange(0, m)
        col = random.randrange(0, n)
        pirellone[row][col] = 1-pirellone[row][col]
    return pirellone


def is_solvable(pirellone, n, m):
    for i in range(n):
        inv = pirellone[0][0] != pirellone[i][0]
        for j in range(m):
            v = not pirellone[i][j] if inv else pirellone[i][j]
            if v != pirellone[0][j]:
                return False
    return True 


def print_pirellone(pirellone):
    for l in pirellone:
        print(*l)


def send_pirellone_file(pirellone):
    res = ""
    n, m = len(pirellone), len(pirellone[0])
    res += f"{n} {m}\n"
    for row in pirellone:
        res += " ".join(map(str, row)) + "\n"
    ta.send_file(res, filename=f"pirellone_{n}_{m}_fail.txt")


def eval_is_solvable(n, m, solvable=False):
    print(f"Checking if solvable {n}x{m}")
    pirellone = random_pirellone(n, m, solvable=solvable)

    read = [[False for j in range(m + 1)] for i in range(n + 1)]
    def is_on(i, j):
        if read[i][j]:
            ta.goals["decision_no_double_read"] = False
        read[i][j] = True
        p.check(1 <= i <= n, "row index out of range")
        p.check(1 <= j <= m, "column index out of range")
        return pirellone[i - 1][j - 1]

    with ta.run_algorithm(ta.submission.source) as p:
        res = bool(p.functions.is_solvable(n, m, callbacks=[is_on]))
         
    solvable = is_solvable(pirellone, n, m)
    if res == solvable:
        print("Correct!")
        return True 
    if res:
        print("You said that the pirellone was solvable, but it is not, take a look")
    else:
        print("You said that the pirellone was not solvable, but it is, take a look")

    if n <= 50:
        print_pirellone(pirellone)
    send_pirellone_file(pirellone)
    return False

def eval_solve(n, m):
    print(f"Getting solution for {n}x{m}")

    pirellone = random_pirellone(n, m, solvable=True)

    count = 0
    read = [[False for j in range(m + 1)] for i in range(n + 1)]
    def is_on(i, j):
        nonlocal count 
        if read[i][j]:
            ta.goals["solve_no_double_read"] = False
        read[i][j] = True

        count += 1
        if count > n + m - 1:
            ta.goals["solve_minimum_reads"] = False
        p.check(1 <= i <= n, "row index out of range")
        p.check(1 <= j <= m, "column index out of range")
        return pirellone[i - 1][j - 1]

    def switch_row(i):
        i -= 1
        for j in range(m):
            pirellone[i][j] = int(not pirellone[i][j])

    def switch_col(j):
        j -= 1
        for i in range(n):
            pirellone[i][j] = int(not pirellone[i][j])
 
    with ta.run_algorithm(ta.submission.source) as p:
        p.procedures.solve(n, m, callbacks=[is_on, switch_row, switch_col])

    solved = not any(any(pirellone[i][j] for j in range(m)) for i in range(n))
    if not solved:
        print("You didn't turn off all the lights. Take a look")
        if n <= 50:
            print_pirellone(pirellone)
        send_pirellone_file(pirellone)
    else:
        print("Correct!")
    return solved


def main():
    ta.goals.check("decision_exponential", lambda: eval_is_solvable(10, 10))
    ta.goals.check("decision_exponential", lambda: eval_is_solvable(10, 10, solvable=True))
    ta.goals.check("solve_exponential", lambda: eval_solve(10, 10))
    ta.goals.check("decision_exponential", lambda: eval_is_solvable(20, 20))
    ta.goals.check("decision_exponential", lambda: eval_is_solvable(20, 20, solvable=True))
    ta.goals.check("solve_exponential", lambda: eval_solve(20, 20))

    ta.goals.check("decision_quadratic", lambda: eval_is_solvable(50, 50))
    ta.goals.check("decision_quadratic", lambda: eval_is_solvable(50, 50, solvable=True))
    ta.goals.check("solve_quadratic", lambda: eval_solve(50, 50))
    ta.goals.check("decision_quadratic", lambda: eval_is_solvable(100, 100))
    ta.goals.check("decision_quadratic", lambda: eval_is_solvable(100, 100, solvable=True))
    ta.goals.check("solve_quadratic", lambda: eval_solve(100, 100))

    ta.goals.setdefault("decision_exponential", True)
    ta.goals.setdefault("solve_exponential", True)
    ta.goals.setdefault("decision_quadratic", True)
    ta.goals.setdefault("solve_quadratic", True)
    ta.goals.setdefault("solve_minimum_reads", True)
    ta.goals.setdefault("decision_no_double_read", True)
    ta.goals.setdefault("solve_no_double_read", True)

    print(ta.goals)


if __name__ == "__main__":
    main()
