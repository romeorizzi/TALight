import random

import turingarena as ta

def eratostene(givenNumber):  
    
    # Initialize a list
    primes = []
    for possiblePrime in range(2, givenNumber + 1):

        # Assume number is prime until shown it is not. 
        isPrime = True
        for num in range(2, int(possiblePrime ** 0.5) + 1):
            if possiblePrime % num == 0:
                isPrime = False
                break

        if isPrime:
            primes.append(possiblePrime)

for _ in range(10):
    value_range = range(10 ** ta.parameters.digits, 5 * 10 ** ta.parameters.digits)
    a, b = random.choices(value_range, k=2)

    try:
        print(f"Testing {a} + {b} ...", end="")
        with ta.run_algorithm(ta.submission.source) as process:
            c = process.functions.sum(a, b)
        print(f" answer: {c}", end="")
        if c == a + b:
            print(" (correct)", end="")
        else:
            print("  (WRONG!)", end="")
            ta.goals["correct"] = False
        print(f"(time: {int(process.time_usage * 1000000)} us)")
    except ta.AlgorithmError as e:
        print(f" error: {e}")
        ta.goals["correct"] = False

ta.goals.setdefault("correct", True)


def test_correct_solution():
    with ta.run_algorithm("solutions/correct.cpp") as p:
        assert p.functions.sum(3, 5) == 8
