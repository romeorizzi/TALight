#!/usr/bin/env python3
import os
from sys import stderr

class Goal():
    def __init__(self, goal_name, immidiate_prec_goals, immidiate_succ_goals):
        self.name = goal_name
        self.is_alive = True
        self.faced = False
        self.out_of_time = False
        self.prec = immidiate_prec_goals
        self.succ = immidiate_succ_goals
        self.testcases_faced = []
        self.num_testcases_passed = 0
        self.num_testcases_correct_ans = 0
        self.num_testcases_wrong_ans = 0
        self.num_testcases_within_time = 0
        self.num_testcases_over_time = 0

    def print_goal_summary(self, summary_type, TAc,LANG):
        assert summary_type in ['short','long']
        TAc.print(LANG.render_feedback("summary", f'\n# {summary_type.upper()} SUMMARY OF THE RESULTS FOR GOAL "{self.name}":\n'), "white")
        if summary_type=='short':
            TAc.print(LANG.render_feedback("testcases-faced", f'# Testcases faced: {len(self.testcases_faced)}'), "green")
            TAc.print(LANG.render_feedback("testcases-passed", f'# Testcases passed with correct answer within the time limit: {self.num_testcases_passed}/{len(self.testcases_faced)}'), "green")
        else:
            for t,i in zip(self.testcases_faced,range(1,1+len(self.testcases_faced))):
                if t["correct"] == True:
                    TAc.print(LANG.render_feedback("right-ans", f'# TestCase {i}: Correct answer! Took time {t["time"]} on your machine.\n'), "green")
                elif t["correct"] == False:
                    if 'user_sol' in t.keys():
                        TAc.print(LANG.render_feedback("wrong-opt-sol", f'# NO! You gave a wrong solution to the instance generated from <{t["generator"].__name__}: {t["descriptor"]}>.\n'), "yellow")
                    elif 'subopt' in t.keys():
                        TAc.print(LANG.render_feedback("subopt-val", f'# NO! You missed the optimal value for the instance generated from <{t["generator"].__name__}: {t["descriptor"]}>.\n'), "yellow")
                    else:
                        TAc.print(LANG.render_feedback("superopt-val", f'# NO! Your bot has returned a super-optimal value for the instance generated from <{t["generator"].__name__}: {t["descriptor"]}>.\n'), "yellow")
                else:
                    TAc.print(LANG.render_feedback("out-of-time-ans-with-user-sol", f'# Your bot took too much time on this instances generated from <{t["generator"].__name__}: {t["descriptor"]}>.\n'), "white")

            if self.passed:
                TAc.print(LANG.render_feedback("right-in-time", f'# OK! Your solution achieved goal "{self.name}".\n'), "green")
            if self.num_testcases_over_time > 0 and self.num_testcases_wrong_ans == 0:
                TAc.print(LANG.render_feedback("right-not-in-time", f'# OK! Though all answers produced by your solution are correct, still it exceeded the time limit on some instances. As such, you did not achieve goal "{self.name}".\n'), "yellow")
            elif self.num_testcases_wrong_ans != 0:
                TAc.print(LANG.render_feedback("wrong-answ", f'# NO! Your solution gave wrong answers on at least one instance. Your solution does NOT achieve goal "{self.name}".\n'), "red")

            
class DAG_of_goals():
    def __init__(self, V,A,with_sink_node_all=True):
        if with_sink_node_all:
            for v in V:
                A.append((v,'all'))
            V.append('all')
        self.n = len(V)
        self.m = len(A)
        self.topologically_sorted_goals = []
        self.order = {}
        opened = set({})
        closed = set({})
        def dfs(v):
            opened.add(v)
            for a,b in A:
                if b == v:
                    if a in opened and a not in closed:
                        print("Error: your DAG contains a cycle!")
                    if a not in opened:
                        dfs(a)
            closed.add(v)
            self.order[v] = len(self.topologically_sorted_goals)
            self.topologically_sorted_goals.append(v)
        for v in V:
            if v not in closed:
                dfs(v)
        #print(f"{self.order=}")
        for i in range(self.n):
            goal_i_name = self.topologically_sorted_goals[i]
            #print(f"{i=}, {goal_i_name=}")
            #print(goal_i_name, [self.order[u] for (u,v) in A if v == goal_i_name], [self.order[v] for (u,v) in A if u == goal_i_name])
            self.topologically_sorted_goals[i] = Goal(goal_i_name, [self.order[u] for (u,v) in A if v == goal_i_name], [self.order[v] for (u,v) in A if u == goal_i_name])
        for goal in self.topologically_sorted_goals:
            for j in range(len(goal.succ)):
                goal.succ[j] = self.topologically_sorted_goals[goal.succ[j]]
            for j in range(len(goal.prec)):
                goal.prec[j] = self.topologically_sorted_goals[goal.prec[j]]
            
    def reduce_to_down_closure(self, goal_name):
        goal_order = self.order[goal_name]
        goal = self.topologically_sorted_goals[goal_order]
        #print(f"{goal_name=}, {goal_order=}, {goal=}")
        for g in self.topologically_sorted_goals:
            g.is_alive = False
            g.reason_of_exclusion = f'is not the goal you have set ("{goal_name}") nor a prerequisite of it'
        def back_dfs(v):
            #print(f"{v.name=}, {v.is_alive=}\n{v=}\n{v.prec=}\n{[u.name for u in v.prec]=}")
            v.is_alive = True
            for u in v.prec:
                if not u.is_alive:
                    back_dfs(u)
        back_dfs(goal)
        
    def kill_goals_above(self, goal):
        def dfs(u):
            #print(f"{u.name=}, {u.is_alive=}\n{u=}\n{u.prec=}\n{[v.name for v in u.succ]=}")
            u.is_alive = False
            u.reason_of_exclusion = f'has a goal where your bot has failed ("{goal.name}") as a prerequisite'
            for v in u.succ:
                if v.is_alive:
                    dfs(v)
        for v in goal.succ:
            dfs(v)
        

    def print_summaries(self, summary_type, TAc,LANG):
        assert summary_type in ['only-recap','short','long']
        if summary_type in ['short','long']:
            TAc.print(LANG.render_feedback('summary-of-results', f'# SUMMARY OF RESULTS ({summary_type}):'), "white", ["bold"])
            for goal in self.topologically_sorted_goals:
                if len(goal.testcases_faced) > 0:
                    goal.print_goal_summary(summary_type, TAc,LANG)
        TAc.print(LANG.render_feedback('summary-of-results-recap', '\n# SUMMARY OF RESULTS, THE RECAP:'), "white", ["bold"])
        for goal in self.topologically_sorted_goals:
            if not goal.faced:
                TAc.print(LANG.render_feedback('goal-not-faced', f'# Goal "{goal.name}": NO instance of this goal has been faced since this goal {goal.reason_of_exclusion}.'), 'cyan', ['bold'])
            elif goal.passed:
                TAc.print(LANG.render_feedback('goal-passed', f'# Goal "{goal.name}": PASSED (passed instances: {goal.num_testcases_passed}/{len(goal.testcases_faced)} instances)'), 'green', ['bold'])
            else:
                TAc.print(LANG.render_feedback('goal-NOT-passed', f'# Goal "{goal.name}": NOT passed (passed instances: {goal.num_testcases_passed}/{len(goal.testcases_faced)} instances, correct answers: {goal.num_testcases_correct_ans}/{len(goal.testcases_faced)}, wrong answers: {goal.num_testcases_wrong_ans}/{len(goal.testcases_faced)} instances), over time limit: {goal.num_testcases_over_time}/{len(goal.testcases_faced)} instances)'), 'red', ['bold'])

        
        
        
        
        
        
        
        
        
        
        
        
        
        
