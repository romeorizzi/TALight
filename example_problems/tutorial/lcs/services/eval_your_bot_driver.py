#!/usr/bin/env python3
from sys import stderr, exit
import random
from time import monotonic

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper, prog_lang_ext
import TAL_DAGs
from run_with_deadline import run_with_deadline

import lcs_lib as ll

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('goal',str),
    ('commitment',str),
    ('summary',str),
    ('lang',str),
    ('code_lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# DEFINE THE DAG OF GOALS:

V = ['m_and_n_up_to_10','m_and_n_up_to_100','m_up_to_10_n_up_to_5000','m_up_to_n_n_5000_opt_val_at_least_4980']
A = [('m_and_n_up_to_10','m_and_n_up_to_100'), ('m_and_n_up_to_10','m_up_to_10_n_up_to_5000'), ('m_and_n_up_to_10','m_up_to_n_n_5000_opt_val_at_least_4980')]

TAL_goals = TAL_DAGs.DAG_of_goals(V,A,with_sink_node_all=True)
TAL_goals.reduce_to_down_closure(ENV['goal']) # is_alive is set to False for every goal that can not reach ENV['goal'] in the DAG of goals. 

def instances(goal):
    if goal.name == 'm_and_n_up_to_10':
        for i in range(2):
            for alphabet in ["DNA", "uppercase"]:
                yield {'generator':ll.instance_randgen_1, 'descriptor': {'m':10,'n':10,'alphabet':alphabet,'seed':random.randrange(100000,1000000)}, 'time_allowance':1}
    if goal.name == 'm_and_n_up_to_100':
        for i in range(2):
            for alphabet in ["DNA", "uppercase"]:
                yield {'generator':ll.instance_randgen_1, 'descriptor': {'m':100,'n':100,'alphabet':alphabet,'seed':random.randrange(100000,1000000)}, 'time_allowance':1}
    if goal.name == 'm_up_to_10_n_up_to_5000':
        for i in range(2):
            for alphabet in ["DNA", "uppercase"]:
                yield {'generator':ll.instance_randgen_1, 'descriptor': {'m':10,'n':5000,'alphabet':alphabet,'seed':random.randrange(100000,1000000)}, 'time_allowance':1}
    if goal.name == 'm_up_to_n_n_5000_opt_val_at_least_4980':
        for i in range(2):
            for alphabet in ["DNA", "uppercase"]:
                yield {'generator':ll.instance_randgen_2, 'descriptor': {'m':10,'n':5000,'opt_val':4980,'alphabet':alphabet,'seed':random.randrange(100000,1000000)}, 'time_allowance':1}
                

# FUNCTION TESTING ONE SINGLE TESTCASE: 
def one_test(instance):
    s = "".join(instance['input'][0])
    t = "".join(instance['input'][1])
    TAc.print(LANG.render_feedback("string-s",'# Given the two strings s and t,'), "white", ["bold"])
    TAc.print(LANG.render_feedback("string-s",'# with s='), "white", ["bold"])
    TAc.print(s, "yellow", ["bold"])
    TAc.print(LANG.render_feedback("string-t",'# and t='), "white", ["bold"])
    TAc.print(t, "yellow", ["bold"])
    if ENV['check_also_sol']:
        TAc.print(LANG.render_feedback("prompt-opt-sol", f'# Provide a longest possible common subsequence of s and t:'), "white", ["bold"])
        start = monotonic()
        user_sol = TALinput(token_type=str, num_tokens=1, TAc=TAc, LANG=LANG)[0]
        end = monotonic()
        instance['user_sol'] = user_sol
        #print(f"{user_sol=}")
        if ll.check_sol_feas_and_opt(TAc, LANG, user_sol, 'subseq', s, t):
            instance['correct'] = True
            TAc.print(LANG.render_feedback("ok-sol", f'# Ok! Your solution is indeed both feasible and optimal!'), "green", ["bold"])
        else:
            instance['correct'] = False
    else:
        TAc.print(LANG.render_feedback("prompt-opt-sol", f'# Tell the maximum length of a common subsequence of s and t:'), "white", ["bold"])
        start = monotonic()
        user_val = TALinput(token_type=int, num_tokens=1, TAc=TAc, LANG=LANG)[0]
        end = monotonic()
        instance['user_val'] = user_val
        opt_val, opt_sol = ll.opt_val_and_sol(s, t)
        instance['opt_val'] = opt_val
        if user_val == opt_val:
            instance['correct'] = True
            TAc.print(LANG.render_feedback("ok-val", f'# Ok! We agree that {opt_val} is the optimal value!\n'), "green", ["bold"])
        else:
            instance['correct'] = False
            if user_val > opt_val:
                instance['superopt'] = True
                TAc.print(LANG.render_feedback("superoptimal", f'# No! No common subsequence of s and t has length {user_val}!'), "red", ["bold"])
            else:
                instance['subopt'] = True
                TAc.print(LANG.render_feedback("suboptimal", f'# No! The following common subsequence of s and t has length {opt_val} > {user_val}:'), "red", ["bold"])
                TAc.print(opt_sol, "red", ["bold"])
        instance['time'] = end-start
        
# MAIN LOOP OF THE EVAL SERVICE:

for goal in TAL_goals.topologically_sorted_goals:
    #print(f"{goal.name=}")
    if goal.is_alive:
        TAc.print(LANG.render_feedback("goal", f'# We now check the goal "{goal.name}"'), "green", ["bold"])
        goal.faced = True
        goal.passed = True
        for instance in instances(goal):
            goal.testcases_faced.append(instance)
            TAc.print(LANG.render_feedback("instance-descriptor", f'## evaluating on instance <{instance["generator"].__name__}: {instance["descriptor"]}>'), "green", ["bold"])
            instance['input'] = instance['generator'](**instance['descriptor'])
            finished, answ = run_with_deadline(f=one_test, args={'instance':instance}, deadline=60)
            #print(f"{instance=}")
            if finished:
                if instance['time'] > instance['time_allowance']:
                    goal.num_testcases_over_time += 1
                else:
                    goal.num_testcases_within_time += 1
                if instance['correct']:
                    goal.num_testcases_correct_ans += 1
                    if instance['time'] <= instance['time_allowance']:
                        goal.num_testcases_passed += 1
                else:
                    goal.num_testcases_wrong_ans += 1
                    TAc.print(LANG.render_feedback("goal-failed-wrong-answer", f'Your bot has failed goal {goal.name} by providing a wrong answer'), "red", ["bold"])
                    goal.passed = False
            else:
                goal.out_of_time = True
                goal.num_testcases_over_time += 1
            if not finished:
                TAc.print(LANG.render_feedback("goal-failed-time-limit", f'Your bot has failed goal {goal.name}: we had to stop it by violation of the hard time limits.'), "red", ["bold"])
                goal.passed = False
            elif instance['time'] > instance['time_allowance']:
                TAc.print(LANG.render_feedback("goal-failed-time-limit", f'Your bot has failed goal {goal.name} by violating the time limit ({instance["time"]} > {instance["time_allowance"]})'), "red", ["bold"])
                goal.passed = False
            if not goal.passed:
                TAL_goals.kill_goals_above(goal) # is_alive is set to False for every goal that has goal as one of its direct or inderect prerequisites.
                break
        if goal.passed == True:
            TAc.print(LANG.render_feedback("goal-passed", f'# Your bot has conquered goal {goal.name}\n'), "green", ["bold"])

            

TAL_goals.print_summaries(ENV['summary'],TAc,LANG)

if ENV.LOG_FILES == None:
    TAc.print(LANG.render_feedback("how-to-store", f'\n# NOTE: This service can also be used to act a submission, if the teacher/instructor deploying it has decided to activate this feature for a class or a group of participants to a contect. In this case, the teacher has assigned you a personal token. If you want to turn this service call from a sole evaluation to a submission of your work, then at the service call you should supply also your personal token and the source code implementing your solving algorithm (the source code of your bot). In order to associate this file to the `sourcecode` filehandler, and to provide your personal token, call the service as follows:\n#     rtal connect -e -x <MY_TOKEN> lcs eval_your_bot -fsourcecode=my_bots/my_lcs_solver.py -acode_lang=python -- my_bots/my_lcs_solver.py'), "red", ["bold"])
else:
    if not ENV.seed_generated:
        TAc.print(LANG.render_feedback("generated-seed", f'\n# NOTE: You asked to run this service with a specific seed value ({ENV["seed"]}). We assume you meant to replicate the very same behaviour of the server as on a previous call to this service.'), "orange", ["bold"])
        TAc.print(LANG.render_feedback("generated-seed", '# Such a run can not be stored as a submission (as you now may know the instances in advance).'), "red", ["bold"])
        TAc.stop_bot_and_exit()
    if TALf.exists_input_file('sourcecode'):
        if ENV["code_lang"] == 'compiled' or prog_lang_ext[ENV["code_lang"]] == TALf.lang_extension(TALf.input_filename('sourcecode')):
            sourcecode_as_string = TALf.input_file_as_str('sourcecode')
            TALf.str2log_file(content=sourcecode_as_string, filename=f"source_code.{TALf.lang_extension(TALf.input_filename('sourcecode'))}", timestamped = False)
            for goal in TAL_goals.topologically_sorted_goals:
                if goal.faced:
                    if goal.passed:
                        TALf.str2log_file(content=f'OK goal={goal.name}.{ENV["commitment"]}. File generated by the service eval_your_bot of the problem lcs.', filename=f'OK_{goal.name}_{ENV["commitment"]}', timestamped = False)
                        TALf.str2output_file(content='OK goal={goal.name}.{ENV["commitment"]}. File generated by the service eval_your_bot of the problem lcs.\n\n   In the future we might consider to RSA-sign this message (the codebase is ready for this, but the general setup of the server will have to be done on the server, nor we have the infrastructure for the managing clear in mind). Moreover, as for now we do not need to give value to these certificates.', filename=f'OK_cert_{goal.name}_{ENV["commitment"]}', timestamped = False)
                    else:
                        TALf.str2log_file(content=f'NO goal={goal.name}.{ENV["commitment"]}. File generated by the service eval_your_bot of the problem lcs.', filename=f'NO_{goal.name}_{ENV["commitment"]}', timestamped = False)
            TAc.print(LANG.render_feedback("stored-submission", f'Your submission has been stored on the server'), "green", ["bold"])
        else:
            TAc.print(LANG.render_feedback("declaring-code-lang", f'\n# NOTE: calling this service you declared `code_lang`=`ENV["code_lang"]` but the source you loaded assigning it to the filehandler `sourcecode` has not been recognized as such. If you have troubles in getting your code properly recognized, go for `code_lang`=`compiled`, so that your bot will be put under the highest stress before deciding it has passes any goal.'), "red", ["bold"])
            TAc.stop_bot_and_exit()
    else:
        TAc.print(LANG.render_feedback("missing-sourcecode", f'\n# NOTE: When this service is used to act a submission (i.e., when you provide a valid token) then it is required that at the service call you supply also the source code implementing your solving algorithm. To associate this file to the `sourcecode` filehandler, call the service as follows:\n#     rtal connect -x <MY_TOKEN> lcs eval_your_bot -fsourcecode=my_bots/my_lcs_solver.py'), "red", ["bold"])
        TAc.stop_bot_and_exit()

        
if ENV.seed_generated:
    TAc.print(LANG.render_feedback("generated-seed", f'The seed ({ENV["seed"]}) has been generated by the service. The very same behaviour of the server can be replicated by introducing this seed value (and leaving all the other arguments the same as for this one call).'), "green", ["bold"])
    
TAc.stop_bot_and_exit()
