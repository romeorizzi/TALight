#!/usr/bin/env python3
import os, sys
from time import monotonic

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../services")))
from hanoi_lib import ConfigGenerator, HanoiTowerProblem, generate_n_list


VERSIONS = ['classic', 'toddler', 'clockwise']
INITIAL_TYPE = 'general'
FINAL_TYPE = 'general'
SEED = 130000
N_MAX = 14
SCALING_FACTOR = 1.2



def gen_remote(initial_type, final_type, seed):
    for v in VERSIONS:
        for be_efficient in ['no', 'yes']:
            os.system(f"rtal connect -e hanoi eval_opt_num_moves \
                        -av={v} \
                        -astart={initial_type} \
                        -afinal={final_type} \
                        -aok_if_congruent_modulus={0} \
                        -agoal={'correct'} \
                        -aseed={seed} \
                        -acode_lang={'python'} \
                        -alang={'hardcoded'} \
                        -- ../utils/test_bot.py {v} {be_efficient}")


def gen_local(initial_type, final_type, seed, n_max, scaling_factor):
    for v in VERSIONS:
        # Generate list of n
        n_list = generate_n_list(n_max, scaling_factor)

        # Init Hanoi Tower and configGenerator
        hanoi = HanoiTowerProblem(v)
        gen = ConfigGenerator(seed)

        # Execute all test
        times_correct = list()
        times_efficient = list()
        for n in n_list:
            # get type of configurations
            start, final, error = gen.getConfigs(initial_type, final_type, n)
            assert error == None

            # Get correct answer
            t_start = monotonic()
            hanoi.getMinMoves(start, final, False)
            t_end = monotonic()
            time = t_end - t_start # seconds in float
            times_correct.append(time)

            # Get efficient correct answer
            t_start = monotonic()
            hanoi.getMinMoves(start, final, True)
            t_end = monotonic()
            time = t_end - t_start # seconds in float
            times_efficient.append(time)

            # Print info
            print(f'Finish test with n={n}')
        print('Finish all test of')

        # Save data
        with open(f'data/{v}_n.txt', 'w') as file:
            file.write(f'{n_list}\n')
        with open(f'data/{v}_correct.txt', 'w') as file:
            file.write(f'{times_correct}')
        with open(f'data/{v}_efficient.txt', 'w') as file:
            file.write(f'{times_efficient}')



if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'clean':
            os.system("rm -rf data/*.txt")
            exit(0)
        
        if not os.path.exists('data'):
            os.makedirs('data')
        
        if sys.argv[1] == 'local':
            gen_local(INITIAL_TYPE, FINAL_TYPE, SEED, N_MAX, SCALING_FACTOR)
            exit(0)
        if sys.argv[1] == 'remote':
            gen_remote(INITIAL_TYPE, FINAL_TYPE, SEED)
            exit(0)

    print('param availables:')
    print('  clean')
    print('  local')
    print('  remote')
