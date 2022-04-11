## clean everything
make clean

## generate instances
make

## solve

rtal connect triangle
rtal connect triangle -am=5 -an=15 -aseed=101010 -abig_seed=443322 -ainstance_format=pyramid 
rtal connect triangle -am=5 -an=15 -aseed=101010 -abig_seed=443322 -ainstance_format=in_lines
rtal connect triangle -am=20 -an=3 -aseed=101010 -abig_seed=443322 -aMAX_VAL=1 -aMAX_VAL_BIG=1 -ainstance_format=pyramid 
rtal connect triangle -am=20 -an=3 -aseed=101010 -abig_seed=443322 -aMAX_VAL=1 -aMAX_VAL_BIG=1 -ainstance_format=in_lines

## gimme_instance

rtal connect triangle gimme_instance -asource=randgen_1 -am=5 -an=5 -ainstance_format=pyramid 
rtal connect triangle gimme_instance -asource=randgen_1 -am=5 -an=5 -ainstance_format=in_lines 
rtal connect triangle gimme_instance -asource=randgen_1 -am=10 -an=2 -aMAX_VAL=1 -aMAX_VAL_BIG=1 -ainstance_format=pyramid 
rtal connect triangle gimme_instance -asource=randgen_1 -am=20 -an=2 -aMAX_VAL=1 -aMAX_VAL_BIG=1 -ainstance_format=in_lines 
rtal connect triangle gimme_instance -asource=randgen_1 -am=5 -an=25 -aseed=123456 -abig_seed=654321 -ainstance_format=pyramid 
rtal connect triangle gimme_instance -asource=randgen_1 -am=5 -an=25 -aseed=123456 -abig_seed=654321 -ainstance_format=in_lines 
rtal connect triangle gimme_instance -asource=catalogue -ainstance_id=1 -ainstance_format=pyramid 
rtal connect triangle gimme_instance -asource=catalogue -ainstance_id=1 -ainstance_format=in_lines 
rtal connect triangle gimme_instance -asource=catalogue -ainstance_id=2 -ainstance_format=pyramid 
rtal connect triangle gimme_instance -asource=catalogue -ainstance_id=2 -ainstance_format=in_lines 

### check_feasible_sol

rtal connect triangle check_feasible_sol -asource=catalogue -ainstance_id=1 -ainstance_format=pyramid
rtal connect triangle check_feasible_sol -asource=catalogue -ainstance_id=1 -ainstance_format=in_lines
rtal connect triangle check_feasible_sol -asource=randgen_1 -an=5 -ainstance_format=pyramid
rtal connect triangle check_feasible_sol -asource=randgen_1 -an=5 -ainstance_format=in_lines

### check_and_reward_one_sol

rtal connect triangle check_and_reward_one_sol -asource=terminal -apath=LLRR -ainstance_format=pyramid
rtal connect triangle check_and_reward_one_sol -asource=terminal -apath=LLRR -ainstance_format=in_lines
rtal connect triangle check_and_reward_one_sol -asource=terminal -ainstance_format=pyramid
rtal connect triangle check_and_reward_one_sol -asource=terminal -ainstance_format=in_lines
rtal connect triangle check_and_reward_one_sol -asource=catalogue -ainstance_id=1 -ainstance_format=pyramid
rtal connect triangle check_and_reward_one_sol -asource=catalogue -ainstance_id=1 -ainstance_format=in_lines
rtal connect triangle check_and_reward_one_sol -asource=randgen_1 -am=5 -an=5 -aseed=101010 -apath=RLRL -ainstance_format=pyramid
rtal connect triangle check_and_reward_one_sol -asource=randgen_1 -am=5 -an=5 -aseed=101010 -apath=RLRL -ainstance_format=in_lines
rtal connect triangle check_and_reward_one_sol -asource=randgen_1 -am=5 -an=5 -aseed=101010 -ainstance_format=pyramid
rtal connect triangle check_and_reward_one_sol -asource=randgen_1 -am=5 -an=5 -aseed=101010 -ainstance_format=in_lines

### check_best_sol

rtal connect triangle check_best_sol -asource=terminal -ainstance_format=pyramid
rtal connect triangle check_best_sol -asource=terminal -ainstance_format=in_lines 
rtal connect triangle check_best_sol -asource=catalogue -ainstance_id=1 -ainstance_format=pyramid
rtal connect triangle check_best_sol -asource=catalogue -ainstance_id=1 -ainstance_format=in_lines
rtal connect triangle check_best_sol -asource=randgen_1 -am=5 -an=5 -aseed=112233 -ainstance_format=pyramid
rtal connect triangle check_best_sol -asource=randgen_1 -am=5 -an=5 -aseed=112233 -ainstance_format=in_lines
rtal connect triangle check_best_sol -asource=randgen_1 -am=5 -an=5 -acheck_also_path=1 -aseed=654321 -aopt_sol_val=341 -ainstance_format=pyramid
rtal connect triangle check_best_sol -asource=randgen_1 -am=5 -an=5 -acheck_also_path=1 -aseed=654321 -aopt_sol_val=341 -ainstance_format=in_lines

### check_number_of_triangles_in_triangle

rtal connect triangle check_number_of_triangles_in_triangle -asource=terminal -ainstance_format=pyramid
rtal connect triangle check_number_of_triangles_in_triangle -asource=terminal -ainstance_format=in_lines 
rtal connect triangle check_number_of_triangles_in_triangle -asource=catalogue -ainstance_id=2 -ainstance_format=pyramid
rtal connect triangle check_number_of_triangles_in_triangle -asource=catalogue -ainstance_id=2 -ainstance_format=in_lines
rtal connect triangle check_number_of_triangles_in_triangle -asource=randgen_1 -am=10 -an=2 -aseed=112233 -abig_seed=101010 -aMAX_VAL=1 -aMAX_VAL_BIG=1 -ainstance_format=pyramid
rtal connect triangle check_number_of_triangles_in_triangle -asource=randgen_1 -am=10 -an=2 -aseed=112233 -abig_seed=101010 -aMAX_VAL=1 -aMAX_VAL_BIG=1 -ainstance_format=in_lines

### test eval services through bots

 # always right answers
 
rtal connect -agoal=time_at_most_n_exp_2 -e triangle eval_feasible_sol -- ~/TALight/example_problems/tutorial/triangle/bots/always_right_bot.py 1
rtal connect -agoal=time_at_most_n_exp_2 -e triangle eval_and_reward_one_sol -- ~/TALight/example_problems/tutorial/triangle/bots/always_right_bot.py 2
rtal connect -agoal=time_at_most_n_exp_2 -e triangle eval_best_sol -- ~/TALight/example_problems/tutorial/triangle/bots/always_right_bot.py 3
rtal connect -agoal=time_at_most_n_exp_2 -e triangle eval_number_of_triangles_in_triangle -- ~/TALight/example_problems/tutorial/triangle/bots/always_right_bot.py 4

 # always wrong answers
 
rtal connect -agoal=time_at_most_n_exp_2 -e triangle eval_feasible_sol -- ~/TALight/example_problems/tutorial/triangle/bots/always_wrong_bot.py 1
rtal connect -agoal=time_at_most_n_exp_2 -e triangle eval_and_reward_one_sol -- ~/TALight/example_problems/tutorial/triangle/bots/always_wrong_bot.py 2
rtal connect -agoal=time_at_most_n_exp_2 -e triangle eval_best_sol -- ~/TALight/example_problems/tutorial/triangle/bots/always_wrong_bot.py 3
rtal connect -agoal=time_at_most_n_exp_2 -e triangle eval_number_of_triangles_in_triangle -- ~/TALight/example_problems/tutorial/triangle/bots/always_wrong_bot.py 4
 
