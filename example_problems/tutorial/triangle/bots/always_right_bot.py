#!/usr/bin/python
from sys import stderr, exit, argv
import random
from bot_lib import Bot

usage=f"""# I am a bot that always provides the right answer. Call me with:
#   > {argv[0]} <required functionality>
# I support the following functionalities:
#   [0] display this help message 
#   [1] eval feasible solution 
#   [2] eval and reward one sol
#   [3] best sol
#   [4] number of triangles in triangle
"""

# BOT = Bot(report_inputs=True,reprint_outputs=True)
BOT = Bot(report_inputs=False,reprint_outputs=False)


def fits(start,livello,big_triangle,small_triangle,small_size):
    last_visited = start
    indexes = [start]
    for i in range(1, small_size):
        last_visited += livello
        for j in range(i + 1):
            indexes.append(last_visited+j)
        last_visited += 1
    for i in range(len(indexes)):
        if small_triangle[i] != big_triangle[indexes[i]]:
            return False,[]
    return True,indexes

def cast_to_array(triangle):
    array = []
    for i in triangle:
        array += i
    return array

def calculate_path(triangle,path_values):
    triangle_array = cast_to_array(triangle)
    n = len(triangle)
    path = [triangle_array[0]]
    s = triangle_array[0]
    i = 0
    last_pos = 0
    for move in path_values:
        if(move == "L"):
            path.append(triangle_array[i+1 + last_pos])
            s += triangle_array[i+1 + last_pos]
            last_pos += i + 1
        else:
            path.append(triangle_array[i+2 + last_pos])
            s += triangle_array[i+2 + last_pos]
            last_pos += i + 2
        i += 1
    return s

def best_reward_and_path(triangle):
    dist = len(triangle)
    triangle_array = cast_to_array(triangle)
    triangle_array = triangle_array[::-1]
    i  = 0
    count = 1
    while dist > 1:
        triangle_array[i + dist] = max(triangle_array[i] + triangle_array[i + dist], triangle_array[i + 1] + triangle_array[i + dist])
        count += 1
        i += 1
        if count == dist:
            count = 1
            dist -= 1
            i += 1
    reward = triangle_array[i]
    triangle_array = triangle_array[::-1]
    path = ""
    last_pos = 0
    dist = len(triangle)
    for j in range(dist-1):
        if triangle_array[j+1 + last_pos] > triangle_array[j+2 + last_pos] :
            path += "L"
            last_pos += j + 1
        else:
            path += "R"
            last_pos += j + 2
    return [reward,path]

if len(argv) != 2:
    print("# Error! Wrong number of arguments.")
if len(argv) != 2 or argv[1]=='0':
    print(usage)
    exit(0)

#  BOT THAT YELDS A FEASIBLE SOLUTION
def yield_feasible_solution_bot():
    while True:
        n = int(BOT.input())
        # get/eat triangle instance:
        for i in range(n):
            BOT.input() # eat the n rows of the triangle
        directions = ['L','R']
        answer = "".join(random.choices(directions,k=n-1))
        BOT.print(answer)
        
#  CHECK AND REWARD ONE SOL
def check_and_reward_one_solution_bot():
    while True:
        n = int(BOT.input())
        # get/eat triangle instance:
        t = []
        for i in range(n):
            t.append(map(int,BOT.input().split()))
        path = BOT.input().strip()
        BOT.print(calculate_path(t,path))

def eval_best_solution_bot():
    while True:
        check_also_sol = False
        # get triangle size:
        n = int(BOT.input())
        # get/eat triangle instance:
        triangle = []
        for i in range(n):
            triangle.append(map(int, BOT.input().split()))
        # get check_also_sol
        if eval(BOT.input()):
            check_also_sol = True
        # give your answer:
        if check_also_sol:
            [best_reward,best_path] = best_reward_and_path(triangle)
            # reward
            # path
            BOT.print(str(best_reward)+best_path)
        else:
            [best_reward, _] = best_reward_and_path(triangle)
            # reward
            BOT.print(best_reward)

def eval_number_of_triangles_in_triangle_bot():
    while True:
        # get small triangle size:
        l = int(BOT.input())
        # get big triangle size:
        L = int(BOT.input())
        # get small triangle array:
        small_triangle = []
        for i in range(l):
            small_triangle.append(map(int, BOT.input().split()))
        # get big triangle array:
        big_triangle = []
        for i in range(L):
            big_triangle.append(map(int, BOT.input().split()))
        # give your answer:
        big_array = cast_to_array(big_triangle)
        small_array = cast_to_array(small_triangle)
        answer = 0
        livello = 1
        indexes = []
        for i in range(int(((L-l+1)*(L-l+2))/2)):
            if i >= livello*(livello+1)/2:
                livello +=1
            if big_array[i] == small_array[0]:
                if fits(i,livello,big_array,small_array,l)[0]:
                    indexes.append(fits(i,livello,big_array,small_array,l)[1])
                    answer += 1
        BOT.print(answer)
        
# MAIN:
if argv[1] == "1":
    yield_feasible_solution_bot()
if argv[1] == "2":
    check_and_reward_one_solution_bot()
if argv[1] == "3":
    eval_best_solution_bot()
if argv[1] == "4":
    eval_number_of_triangles_in_triangle_bot()


