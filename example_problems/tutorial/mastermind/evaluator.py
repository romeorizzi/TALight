import random

from turingarena import *

algorithm = submitted_algorithm()

hanged_up = False
got_4_blacks = False
last_black_guess = [-1,-1,-1,-1]

def main():
    # simply random
    for _ in range(10):
        code = [random.randint(0, 6) for _ in range(0,4) ]
        is_correct_answer, number_of_guess = compute_fixed(code)
        if is_correct_answer:
            print('correct, number of guess', number_of_guess)
        else:
            print('WRONG!')

    # move the secret code in the most difficult position
    for _ in range(10):
        code = [random.randint(0, 6) for _ in range(0,4) ]
        is_correct_answer, number_of_guess = compute_moving(code)
        if is_correct_answer:
            print('correct, number of guess', number_of_guess)
        else:
            print('WRONG!')


def compute_fixed(code):
    with algorithm.run() as process:

        number_of_guess = 0

        def impossible():
            global hanged_up
            hanged_up = True
            process.exit()

        def blackScore(submitted_code):
            nonlocal number_of_guess, last_black_guess, got_4_blacks, code
            number_of_guess += 1
            last_black_guess = submitted_code
            risp = 0
            for i in range(0,4):
                if submitted_code[i] == code[i]:
                    risp += 1
            if risp==4:
                got_4_blacks = True
                process.exit()
            return risp

        def whiteScore(submitted_code):
            nonlocal number_of_guess, last_black_guess, code
            if last_black_guess != submitted_code
                number_of_guess += 1
            
            risp = 0
            code_occur = [0, 0, 0, 0, 0, 0]
            submitted_code_occur = [0, 0, 0, 0, 0, 0]
            for i in range(0,4):
                if submitted_code[i] == code[i]:
                    risp -= 1
                code_occur[code[i]] += 1
                submitted_code_occur[submitted_code[i]] += 1
            for i in range(0,6):
                risp += min(code_occur[i], submitted_code_occur[i])
            return risp

        process.call.play(blackScore=blackScore,whiteScore=whiteScore,impossible=impossible)
        return got_4_blacks, number_of_guess


def compute_moving(code):
    compute_fixed(code)

main()
