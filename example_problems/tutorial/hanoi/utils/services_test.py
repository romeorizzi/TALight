#!/usr/bin/env python3
import os, sys



# ====================================================================== #
# FUNCTIONS
def help():
        print("for execute test call:")
        print("./services_test name_service test_type")
        print("for get tests availables call:")
        print("./services_test name_service help")


def check_opt_num_moves(v, start, final, n, answ, modulus, silent, feedback, certificate, lang):
    print(f"rtal connect hanoi check_opt_num_moves")
    print(f"> v={v}")
    print(f"> start={start}")
    print(f"> final={final}")
    print(f"> n={n}")
    print(f"> answ={answ}")
    print(f"> ok_if_congruent_modulus={modulus}")
    print(f"> silent={silent}")
    print(f"> feedback={feedback}")
    print(f"> with_certificate={certificate}")
    print(f"> lang={lang}")
    os.system(f"rtal connect hanoi check_opt_num_moves \
                -astart={start} \
                -afinal={final} \
                -an={n} \
                -aansw={answ} \
                -aok_if_congruent_modulus={modulus} \
                -av={v} \
                -asilent={silent} \
                -afeedback={feedback} \
                -awith_certificate={certificate} \
                -alang={lang}")


def check_lower_bounds(v, start, final, n, answ, disk, silent, feedback, lang):
    print(f"rtal connect hanoi check_lower_bounds")
    print(f"> v={v}")
    print(f"> start={start}")
    print(f"> final={final}")
    print(f"> n={n}")
    print(f"> answ={answ}")
    print(f"> disk={disk}")
    print(f"> silent={silent}")
    print(f"> feedback={feedback}")
    print(f"> lang={lang}")
    os.system(f"rtal connect hanoi check_lower_bounds \
                -av={v} \
                -astart={start} \
                -afinal={final} \
                -an={n} \
                -aansw={answ} \
                -adisk={disk} \
                -asilent={silent} \
                -afeedback={feedback} \
                -alang={lang}")


def gen_random_puzzle(seed, start, final, n, n_instances, verbose, lang):
    print(f"rtal connect hanoi gen_random_puzzle")
    print(f"> seed={seed}")
    print(f"> start={start}")
    print(f"> final={final}")
    print(f"> n={n}")
    print(f"> n_instances={n_instances}")
    print(f"> verbose={verbose}")
    print(f"> lang={lang}")
    os.system(f"rtal connect hanoi gen_random_puzzle \
                -aseed={seed} \
                -astart={start} \
                -afinal={final} \
                -an={n} \
                -an_instances={n_instances} \
                -averbose={verbose} \
                -alang={lang}")


def play_like(role, start, final, n, format, gimme_moves_available, lang):
    print(f"rtal connect hanoi play_like")
    print(f"> role={role}")
    print(f"> start={start}")
    print(f"> final={final}")
    print(f"> n={n}")
    print(f"> format={format}")
    print(f"> gimme_moves_available={gimme_moves_available}")
    print(f"> lang={lang}")
    os.system(f"rtal connect hanoi play_like \
                -arole={role} \
                -astart={start} \
                -afinal={final} \
                -an={n} \
                -aformat={format} \
                -agimme_moves_available={gimme_moves_available} \
                -alang={lang}")


def check_one_sol(v, start, final, n, format, goal, ignore_peg_from, ignore_peg_to, feedback, lang, test):
    print(f"rtal connect -e hanoi check_one_sol")
    print(f"> v={v}")
    print(f"> start={start}")
    print(f"> final={final}")
    print(f"> n={n}")
    print(f"> format={format}")
    print(f"> goal={goal}")
    print(f"> ignore_peg_from={ignore_peg_from}")
    print(f"> ignore_peg_to={ignore_peg_to}")
    print(f"> feedback={feedback}")
    print(f"> lang={lang}")
    if test == 'use_real_bot':
        os.system(f"rtal connect -e hanoi check_one_sol \
                    -astart={start} \
                    -afinal={final} \
                    -an={n} \
                    -av={v} \
                    -aformat={format} \
                    -agoal={goal} \
                    -aignore_peg_from={ignore_peg_from} \
                    -aignore_peg_to={ignore_peg_to} \
                    -afeedback={feedback} \
                    -alang={lang} \
                    -- ../bots/classic_hanoi_bot_check.py")
    else:
        os.system(f"rtal connect -e hanoi check_one_sol \
                    -astart={start} \
                    -afinal={final} \
                    -an={n} \
                    -av={v} \
                    -aformat={format} \
                    -agoal={goal} \
                    -aignore_peg_from={ignore_peg_from} \
                    -aignore_peg_to={ignore_peg_to} \
                    -afeedback={feedback} \
                    -alang={lang} \
                    -- ../utils/fake_bot.py {service} {test}")


def eval_sol(v, start, final, format, seed, num_tests, n_max, lang, test):
    print(f"rtal connect -e hanoi eval_sol")
    print(f"> v={v}")
    print(f"> start={start}")
    print(f"> final={final}")
    print(f"> format={format}")
    print(f"> seed={seed}")
    print(f"> num_tests={num_tests}")
    print(f"> n_max={n_max}")
    print(f"> lang={lang}")
    if test == 'use_real_bot':
        os.system(f"rtal connect -e hanoi eval_sol \
                    -av={v} \
                    -astart={start} \
                    -afinal={final} \
                    -aformat={format} \
                    -aseed={seed} \
                    -anum_tests={num_tests} \
                    -an_max={n_max} \
                    -alang={lang} \
                    -- ../bots/classic_hanoi_bot_eval_sol.py")
    else:
        os.system(f"rtal connect -e hanoi eval_sol \
                    -av={v} \
                    -astart={start} \
                    -afinal={final} \
                    -aformat={format} \
                    -aseed={seed} \
                    -anum_tests={num_tests} \
                    -an_max={n_max} \
                    -alang={lang} \
                    -- ../utils/fake_bot.py {service} {test}")


def eval_opt_num_moves(v, start, final, modulus, goal, seed, num_tests, n_max, code_lang, lang):
    print(f"rtal connect -e hanoi eval_opt_num_moves")
    print(f"> v={v}")
    print(f"> start={start}")
    print(f"> final={final}")
    print(f"> ok_if_congruent_modulus={modulus}")
    print(f"> goal={goal}")
    print(f"> seed={seed}")
    print(f"> num_tests={num_tests}")
    print(f"> n_max={n_max}")
    print(f"> code_lang={code_lang}")
    print(f"> lang={lang}")
    os.system(f"rtal connect -e hanoi eval_opt_num_moves \
                -av={v} \
                -astart={start} \
                -afinal={final} \
                -aok_if_congruent_modulus={modulus} \
                -agoal={goal} \
                -aseed={seed} \
                -anum_tests={num_tests} \
                -an_max={n_max} \
                -acode_lang={code_lang} \
                -alang={lang} \
                -- ../bots/classic_hanoi_bot_eval_min_moves.py")



# ====================================================================== #
# TESTS
if __name__ == "__main__":
    # get service and test
    if len(sys.argv) != 3:
        print("Wrong call.")
        help()
        exit(0)
    service = sys.argv[1]
    test = sys.argv[2]

    ######################################################################
    # check_opt_num_moves
    if service == 'check_opt_num_moves':
        print(f"TEST: {service} service")
        # run selected test:
        if test == 'help':
            print(f"tests availables for {service} are:")
            print('  correct_no_silent')
            print('  correct_silent')
            print('  wrong_true_val')
            print('  wrong_bigger')
            print('  wrong_smaller')
            print('  wrong_bigger_certificate')
            print('  wrong_smaller_certificate')

        elif test == 'correct_no_silent':
            print(f"TEST: {test}")
            check_opt_num_moves('classic', 'all_A', 'all_C', 2, 3, 0, '0', 'yes_no', 0, 'hardcoded')
        
        elif test == 'correct_silent':
            print(f"TEST: {test}")
            check_opt_num_moves('classic', 'all_A', 'all_C', 2, 3, 0, '1', 'yes_no', 0, 'hardcoded')

        elif test == 'wrong_true_val':
            print(f"TEST: {test}")
            check_opt_num_moves('classic', 'all_A', 'all_C', 2, 2, 0, '0', 'true_val', 0, 'hardcoded')

        elif test == 'wrong_bigger':
            print(f"TEST: {test}")
            check_opt_num_moves('classic', 'all_A', 'all_C', 2, 2, 0, '0', 'smaller_or_bigger', 0, 'hardcoded')

        elif test == 'wrong_smaller':
            print(f"TEST: {test}")
            check_opt_num_moves('classic', 'all_A', 'all_C', 2, 4, 0, '0', 'smaller_or_bigger', 0, 'hardcoded')

        elif test == 'wrong_bigger_certificate':
            print(f"TEST: {test}")
            check_opt_num_moves('classic', 'all_A', 'all_C', 2, 2, 0, '0', 'yes_no', 1, 'hardcoded')

        elif test == 'wrong_smaller_certificate':
            print(f"TEST: {test}")
            check_opt_num_moves('classic', 'all_A', 'all_C', 2, 4, 0, '0', 'yes_no', 1, 'hardcoded')
        
        else:
            print("invalid test")
        exit(0)


    ######################################################################
    # check_lower_bounds
    if service == 'check_lower_bounds':
        print(f"TEST: {service} service")
        # run selected test:
        if test == 'help':
            print(f"tests availables for {service} are:")
            print('  correct_no_silent')
            print('  correct_silent')
            print('  wrong_true_val')
            print('  wrong_bigger')
            print('  wrong_smaller')

        elif test == 'correct_no_silent':
            print(f"TEST: {test}")
            check_lower_bounds('classic', 'all_A', 'all_C', 2, 1, 2, '0', 'yes_no', 'hardcoded')
        
        elif test == 'correct_silent':
            print(f"TEST: {test}")
            check_lower_bounds('classic', 'all_A', 'all_C', 2, 1, 2, '1', 'yes_no', 'hardcoded')

        elif test == 'wrong_true_val':
            print(f"TEST: {test}")
            check_lower_bounds('classic', 'all_A', 'all_C', 2, 2, 2, '0', 'true_val', 'hardcoded')

        elif test == 'wrong_bigger':
            print(f"TEST: {test}")
            check_lower_bounds('classic', 'all_A', 'all_C', 2, 0, 2, '0', 'smaller_or_bigger', 'hardcoded')

        elif test == 'wrong_smaller':
            print(f"TEST: {test}")
            check_lower_bounds('classic', 'all_A', 'all_C', 2, 3, 2, '0', 'smaller_or_bigger', 'hardcoded')
        
        else:
            print("invalid test")
        exit(0)


    ######################################################################
    # gen_random_puzzle
    if service == 'gen_random_puzzle':
        print(f"TEST: {service} service")
        # run selected test:
        if test == 'help':
            print(f"tests availables for {service} are:")
            print('  random')
            print('  verbose0')
            print('  verbose1_rnd')
            print('  verbose1_fixed')
            print('  verbose2')

        elif test == 'random':
            print(f"TEST: {test}")
            gen_random_puzzle(-1, 'all_A', 'all_C', 3, 3, '0', 'hardcoded')

        elif test == 'verbose0':
            print(f"TEST: {test}")
            gen_random_puzzle(130000, 'all_A', 'all_C', 3, 3, '0', 'hardcoded')

        elif test == 'verbose1_rnd':
            print(f"TEST: {test}")
            gen_random_puzzle(-1, 'all_A', 'all_C', 3, 3, '1', 'hardcoded')

        elif test == 'verbose1_fixed':
            print(f"TEST: {test}")
            gen_random_puzzle(130000, 'all_A', 'all_C', 3, 3, '1', 'hardcoded')

        elif test == 'verbose2':
            print(f"TEST: {test}")
            gen_random_puzzle(130000, 'all_A', 'all_C', 3, 3, '2', 'hardcoded')
        
        else:
            print("invalid test")
        exit(0)


    ######################################################################
    # play_like
    if service == 'play_like':
        print(f"TEST: {service} service")
        # run selected test:
        if test == 'help':
            print(f"tests availables for {service} are:")
            print('  toddler')
            print('  daddy')
            print('  toddler_help')
            print('  daddy_help')
            print('  format_extended')

        elif test == 'toddler':
            print(f"TEST: {test}")
            play_like('toddler', 'all_A', 'all_C', 2, 'minimal', '0', 'hardcoded')

        elif test == 'daddy':
            print(f"TEST: {test}")
            play_like('daddy', 'all_A', 'all_C', 2, 'minimal', '0', 'hardcoded')

        elif test == 'toddler_help':
            print(f"TEST: {test}")
            play_like('toddler', 'all_A', 'all_C', 2, 'minimal', '1', 'hardcoded')

        elif test == 'daddy_help':
            print(f"TEST: {test}")
            play_like('daddy', 'all_A', 'all_C', 2, 'minimal', '1', 'hardcoded')

        elif test == 'format_extended':
            print(f"TEST: {test}")
            play_like('daddy', 'all_A', 'all_C', 2, 'extended', '1', 'hardcoded')
        
        else:
            print("invalid test")
        exit(0)


    ######################################################################
    # check_opt_num_moves
    if service == 'check_one_sol':
        print(f"TEST: {service} service")
        # run selected test:
        if test == 'help':
            print(f"tests availables for {service} are:")
            print('  optimal')
            print('  optimal_bot')
            print('  optimal_custom_config')
            print('  optimal_wrong_short')
            print('  optimal_wrong')
            print('  simple_walk_not_optimal1')
            print('  simple_walk_not_optimal2')
            print('  admissible')
            print('  admissible_optimal')
            print('  no_simple_walk')
            print('  spot_first_non_optimal_move')
            print('  gimme_shorter_solution')
            print('  gimme_optimal_solution')
            print('  ignore_correct')
            print('  ignore_peg_from')
            print('  ignore_peg_to')
            print('  ignore_both')

        elif test == 'optimal':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '0', '0', 'yes_no', 'hardcoded', 'optimal')

        elif test == 'optimal_bot':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '0', '0', 'yes_no', 'hardcoded', 'use_real_bot')

        elif test == 'optimal_custom_config':
            print(f"TEST: {test}")
            check_one_sol('classic', 'ABC', 'CBA', 2, 'minimal', 'optimal', '0', '0', 'yes_no', 'hardcoded', 'optimal_custom_config')

        elif test == 'optimal_wrong_short':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '0', '0', 'yes_no', 'hardcoded', 'wrong_short')

        elif test == 'optimal_wrong':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '0', '0', 'yes_no', 'hardcoded', 'wrong')

        elif test == 'simple_walk_not_optimal1':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '0', '0', 'yes_no', 'hardcoded', 'simple_walk_not_optimal')

        elif test == 'simple_walk_not_optimal2':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'simple_walk', '0', '0', 'yes_no', 'hardcoded', 'simple_walk_not_optimal')

        elif test == 'admissible':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'admissible', '0', '0', 'yes_no', 'hardcoded', 'admissible_loop')

        elif test == 'admissible_optimal':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'admissible', '0', '0', 'yes_no', 'hardcoded', 'optimal')

        elif test == 'no_simple_walk':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'simple_walk', '0', '0', 'yes_no', 'hardcoded', 'admissible_loop')

        elif test == 'spot_first_non_optimal_move':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '0', '0', 'spot_first_non_optimal_move', 'hardcoded', 'admissible_loop')

        elif test == 'gimme_shorter_solution1':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'admissible', '0', '0', 'gimme_shorter_solution', 'hardcoded', 'admissible_loop')

        elif test == 'gimme_shorter_solution2':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '0', '0', 'gimme_shorter_solution', 'hardcoded', 'admissible_loop')

        elif test == 'gimme_optimal_solution':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '0', '0', 'gimme_optimal_solution', 'hardcoded', 'admissible_loop')

        elif test == 'ignore_correct':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '1', '1', 'yes_no', 'hardcoded', 'optimal')

        elif test == 'ignore_peg_from':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '1', '0', 'yes_no', 'hardcoded', 'ignore_peg_from')

        elif test == 'ignore_peg_to':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '0', '1', 'yes_no', 'hardcoded', 'ignore_peg_to')

        elif test == 'ignore_both':
            print(f"TEST: {test}")
            check_one_sol('classic', 'all_A', 'all_C', 2, 'minimal', 'optimal', '1', '1', 'yes_no', 'hardcoded', 'ignore_both')
        
        else:
            print("Invalid test")
        exit(0)


    ######################################################################
    # eval_sol
    if service == 'eval_sol':
        print(f"TEST: {service} service")
        # run selected test:
        if test == 'help':
            print(f"tests availables for {service} are:")
            print('  A_to_C')
            print('  general')
            print('  fail')
            print('  random')

        elif test == 'A_to_C':
            print(f"TEST: {test}")
            eval_sol('classic', 'all_A', 'all_C', 'minimal', 130000, 1, 10, 'hardcoded', 'use_real_bot')

        elif test == 'general':
            print(f"TEST: {test}")
            eval_sol('classic', 'general', 'general', 'minimal', 130000, 2, 5, 'hardcoded', 'use_real_bot')

        elif test == 'fake_correct':
            print(f"TEST: {test}")
            eval_sol('classic', 'all_A', 'all_C', 'minimal', 130000, 1, 2, 'hardcoded', 'fake_correct')

        elif test == 'fake_fail':
            print(f"TEST: {test}")
            eval_sol('classic', 'all_A', 'all_C', 'minimal', 130000, 1, 2, 'hardcoded', 'fake_fail')
        
        elif test == 'random':
            print(f"TEST: {test}")
            eval_sol('classic', 'general', 'general', 'minimal', -1, 2, 2, 'hardcoded', 'use_real_bot')

        else:
            print("Invalid test")
        exit(0)


    ######################################################################
    # eval_opt_num_moves
    if service == 'eval_opt_num_moves':
        print(f"TEST: {service} service")
        # run selected test:
        if test == 'help':
            print(f"tests availables for {service} are:")
            print('  A_to_C')
            print('  general')
            print('  random')

        elif test == 'A_to_C':
            print(f"TEST: {test}")
            eval_opt_num_moves('classic', 'all_A', 'all_C', 0, 'correct', 130000, 1, 10, 'python', 'hardcoded')

        elif test == 'general':
            print(f"TEST: {test}")
            eval_opt_num_moves('classic', 'general', 'general', 0, 'correct', 130000, 1, 10, 'python', 'hardcoded')

        elif test == 'random':
            print(f"TEST: {test}")
            eval_opt_num_moves('classic', 'general', 'general', 0, 'correct', -1, 1, 5, 'python', 'hardcoded')

        else:
            print("Invalid test")
        exit(0)



    ######################################################################
    # invalid service
    print("Invalid service.")
    help()
    exit(0)