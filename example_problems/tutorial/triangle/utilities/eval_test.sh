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
