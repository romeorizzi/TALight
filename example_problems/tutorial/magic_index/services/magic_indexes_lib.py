#!/usr/bin/env python3
import random, math
import numpy as np

 
def check_input_vector(vec, TAc, LANG):
    for i in range(1,len(vec)):
        if vec[i] == vec[i-1]:
            TAc.print(LANG.render_feedback("equal-values", f'No. Your vector contains entries with the same value vec[{i-1}] = {vec[i-1]} =vec[{i}].'), "red", ["bold"])
            exit(0)
        if vec[i] < vec[i-1]:
            TAc.print(LANG.render_feedback("decrease", f'No. Your vector is not incrisingly sorted: vec[{i-1}] = {vec[i-1]} > {vec[i]} = vec[{i}].'), "red", ["bold"])
            exit(0)

def random_vector():
    n = random.randint(5, 20)
    vec, seed = random_vector_fixed(n)
    return vec, seed, n


def random_vector_fixed(n, seed="random_seed"):
    if seed=="random_seed":
        seed = random.randrange(100000,1000000)
    else:
        seed = int(seed)
    random.seed(seed)
    if seed >= 100000:
        magics_run_length = min(random.randint(0,n),random.randint(0,n))
        first_magic = random.randint(0,n-magics_run_length)
        last_magic = first_magic + magics_run_length
        vec = list(range(n))
        for i in range(last_magic+1,n):
            vec[i] = vec[i-1] + random.randint(2, 5)
        if first_magic > last_magic:
            first_magic = last_magic +1
        for i in range(first_magic-1,-1,-1):
            vec[i] = vec[i+1] - random.randint(2, 5)
    else:
        prefix = (seed%2 == 1) # gli indici magici sono un prefisso o un suffisso?
        seed_rem=seed//2
        magics_run_length = seed_rem % (n+1)
        seed_rem=seed_rem//(n+1)
        vec = list(range(magics_run_length))
        base = magics_run_length + 1
        while len(vec) < n:
            delta = seed_rem % n
            seed_rem=seed_rem//n            
            vec.append(base+delta)
            base = base+delta+1
        
    return vec,seed

def spot_magic_index(vec):
    magic_indexes = []
    for i in range(len(vec)):
        if vec[i]==i:
            magic_indexes.append(i)
    return magic_indexes

# The optimal strategy shoots always in the middle. The worst case is as follows: at the first shoot nature answers "yes, it is a magic index" (otherwise half of the positions are lost from the very beginning). The problem splits into two, left and right, which howevere have a different nature (since I now know that the magic positions will form a prefix or a suffix).
# On this residual problem nature decides each time I can not split in precisely half, leaving me the biggest half.

def num_questions_worst_case(n):
    if n==0:
        return 0
    else:
	    return 1 + num_questions_worst_case_support((n-1)//2) + num_questions_worst_case_support((n-1)//2 + ((n-1)%2))

def num_questions_worst_case_support(n):
    if n==0:
        return 0
    else:
        return 1 + num_questions_worst_case_support((n-1)//2 + ((n-1)%2))

'''
questions = 0
def generate_optimal_question_vector(vec, lower, upper, vector_optmal_questions):
    global questions

    if lower > upper:
        return []

    mid = (lower + upper) // 2
    vector_optmal_questions[mid] = questions
    questions += 1

    if vec[mid] > mid:      
        return generate_optimal_question_vector(vec, lower, mid - 1,vector_optmal_questions)

    if vec[mid] < mid:
        return generate_optimal_question_vector(vec, mid + 1, upper, vector_optmal_questions)

    if vec[mid] == mid: 
        return generate_optimal_question_vector(vec, lower, mid - 1, vector_optmal_questions) + [mid] + generate_optimal_question_vector(vec, mid + 1, upper, vector_optmal_questions)
'''


def print_vector(vec, TAc, LANG):
    w = len(vec)*2
    h = 3
    print()
    for i in range(h):
        if not i or i == h-1:
            #print(' -'*w, end ='')
            TAc.print(LANG.render_feedback("draw box", f' -'*w), "white", ["bold"], end="")
            print()
        else:
            #print('|', end="")
            TAc.print(LANG.render_feedback("draw box", '|'), "white", ["bold"], end="")
            for i in vec:
                #print(f' {i} |', end="")
                TAc.print(LANG.render_feedback("draw box", f' {i} |'), "white", ["bold"], end="")
            print()
    print()


table_g = [None] * 1000
table_f = [None] * 1000
worst_f, worst_g = {}, {}
table_f[0],table_g[0] = 0, 0
table_f[1], table_g[1] = 1, 1


def g(u, case):
    global table_g, worst_g
    # arrotondiamo per eccesso per non avere il problema della numerazione degli indici da 0 o 1
    pos = math.ceil(u/2)
    if u == 0:
        return table_g[u]
    if u == 1:
        return table_g[u]
    else:
        if case == 'left':
            if table_g[u-pos] == None:
                table_g[u-pos] = g(u-pos, case) #-1 
            case1 = table_g[u-pos]
        else:
            if table_g[pos-1] == None:
                table_g[pos-1] = g(pos-1, case) #1
            case1 = table_g[pos-1]

        if table_g[u-pos] == None:
            table_g[u-pos] = g(u-pos, case)
        case0 = table_g[u-pos] #0

        print(f'u={u}, pos={pos}, case1 = {case1}, case0 = {case0}, case={case}')
        #if the worst case is the same, choose a random value between 0 and 1 (-1)
        if case0 == case1:
            if case == 'left':
                w = random.randint(-1,0)
            else:
                w = random.randint(0,1)
        else:
            w = np.argmax([case1, case0])

        #if w==0 means that the worst case is obtained placing a 1 or -1 in the index 
        if w == 0:
            if case == 'left':
                worst_g[pos-1] = '-1'
            else:
                worst_g[pos-1] = '1'
        else:
            worst_g[pos-1] = '0'
        
        return 1 + max(case1, case0)
  
# la funzione f dato l'indice ottimale (quello spezzando al centro) torna quante domande bisogna fare nel caso pessimo per ogni possibile valore -1 (valore più piccolo dell'indice), 
# 0 valore identico all'indice (MI), e infine 1 (valore più grande dell'indice) 
def f(u):
    global table_f, table_g, worst_f
    # arrotondiamo per eccesso per non avere il problema della numerazione degli indici da 0 o 1
    pos = math.ceil(u/2)
    if u == 0:
        return table_f[u]
    if u == 1:
        return table_f[u]
    else:
        if table_f[u-pos] == None:
            table_f[u-pos] = f(u-pos) #-1
        case1 = table_f[u-pos]

        if table_f[pos - 1] == None:
            table_f[pos - 1] = f(pos-1)
        case2 = table_f[pos - 1] #1

        if table_g[pos-1] == None:
            table_g[pos-1] = g(pos-1, 'left')
        if table_g[u-pos] == None:
            table_g[u-pos] = g(u-pos, 'right') 

        case0 =  table_g[pos-1] + table_g[u-pos] #0

        w = np.argmax([case1,case2,case0])
        if w == 0:
            worst_f[pos-1] = '-1'
        elif w == 1:
            worst_f[pos-1] = '1'
        else:
            worst_f[pos-1] = '0'
     
        return 1 + max(case1, case2, case0)


def get_positions_f(vec):
    # get last occurence of a '-1', index() returns the first occurence so we inverted the vector and took the first occurence (so the last in the original vec) and subtract the result from the original last position of the vector. For the computation of the optimal move, we use the rounded down division in order to avoid mistakes with indexes. Note for the optimal move with enumeration that starts from 1 we use the following formula: (unknow / 2) rounded up, which corresponds to the formula: (lower+upper)// 2 (rounded down) with enumeration from 0.
    if '-1' in vec and '1' in vec:
        posLess = (len(vec)-1) - vec[::-1].index('-1')
        posGreater = vec.index('1')

        if posGreater == posLess + 1:
            return len(vec[posLess+1:posGreater]), None
        return len(vec[posLess+1:posGreater]), ((posLess+1) + (posGreater-1))//2
    elif '-1' in vec: 
        posLess = (len(vec)-1) - vec[::-1].index('-1')
        if posLess == len(vec)-1:
            return 0,None
        else:
            return len(vec[posLess+1:]), (((posLess+1)+ (len(vec)-1))//2)
    elif '1' in vec:
        posGreater = vec.index('1')
        if posGreater == 0:
            return 0,None
        else:
            return len(vec[:posGreater]), ((posGreater-1)//2)
    else:
        return len(vec), ((len(vec)-1)//2)
    
def get_positions_g(vec):
    first_occ_0 = vec.index('0')
    last_occ_0 = (len(vec)-1) - vec[::-1].index('0')

    last_occ_less = 0
    first_occ_greater = len(vec) # we initialize this like if the first occurence was out of the vector
    sum_factor = 0 # use if there is not a '-1' in the vector 
    sub_factor = 0 # use if there is not a '1' in the vector 
    s = 0
   
    # if it exists at least one element equal to '-1' in vec update the position of '-1' with the last occurence.
    if '-1' in vec:
        last_occ_less = (len(vec)-1) - vec[::-1].index('-1')
        sum_factor += 1
    
    # if it exists at least one element equal to '1' in vec update the position of '-1' with the first occurence.
    if '1' in vec:
        first_occ_greater = vec.index('1')
        sub_factor += 1

    # use this variable in the case where we don't have a 1 in vec. Since we initialize the first occurance to len(vec), then in the division if we don't subtract a -1 we obtain a wrong position where to point
    if first_occ_greater == len(vec):
        s += 1

    #print(vec)
    #print(f'first_occ_0 = {first_occ_0}, last_occ_0 = {last_occ_0}, last_occ_less = {last_occ_less}, first_occ_greater = {first_occ_greater}')


    # the optimal moves are computed as the middle value between the last occurence of a '-1' and the first MI excluded and the last occurence of MI excluded and the first occurence of a '1' 
    optimal_pos = [((last_occ_less + sum_factor) + (first_occ_0 - 1))//2 , ((last_occ_0 + 1) + (first_occ_greater - s - sub_factor))//2]    
    unknowns = [len(vec[last_occ_less + sum_factor: first_occ_0]), len(vec[last_occ_0 + 1: first_occ_greater])]

    # check that if unknow is 0 in some part of the vector (i.e., we know already everything), the optimal move is None.
    if unknowns[0] == 0:
        optimal_pos[0] = None
    if unknowns[1] == 0:
        optimal_pos[1] = None    

    return unknowns, optimal_pos


def getWorst_f():
    return worst_f

def getWorst_g():
    return worst_g

def cleanWorst_f():
    worst_f = {}
    return

def cleanWorst_g():
    worst_g = {}
    return


def get_first_previous(discovered_vec, chosen_index):
    free_space_left = 0
    for i in discovered_vec[chosen_index-1::-1]:
        if i != None:
            return i, free_space_left
        free_space_left += 1

def get_first_following(discovered_vec, chosen_index):
    free_space_right = 0
    for i in discovered_vec[chosen_index+1:]:
        if i != None:
            return i, free_space_right
        free_space_right += 1


def generate_value_for_vector(server_vector, discovered_vec, chosen_index):
    #print('chosen index= ', chosen_index)

    if server_vector[chosen_index] == '0':
        return chosen_index

    elif server_vector[chosen_index] == '-1':
        if '-1' in server_vector[:chosen_index] and '-1' in server_vector[chosen_index+1:]:
            first_previous_smaller, free_space_left = get_first_previous(discovered_vec, chosen_index)
            first_following_smaller, free_space_rigth  = get_first_following(discovered_vec, chosen_index)
            upper_bound = (first_following_smaller - 1) - free_space_rigth
            lower_bound = (first_previous_smaller + 1) + free_space_left
            
            return random.randint(lower_bound, upper_bound)

        elif '-1' in server_vector[:chosen_index]:
            first_previous_smaller, free_space_left = get_first_previous(discovered_vec, chosen_index)
            upper_bound = chosen_index - 1
            lower_bound = (first_previous_smaller + 1) + free_space_left
            
            return random.randint(lower_bound, upper_bound)

        elif '-1' in server_vector[chosen_index+1:]:
            first_following_smaller, free_space_rigth  = get_first_following(discovered_vec, chosen_index)
            upper_bound = (first_following_smaller - 1) - free_space_rigth
            lower_bound = chosen_index - random.randint(10,100)

            return random.randint(lower_bound, upper_bound)

        else:
            upper_bound = chosen_index - 1
            lower_bound = chosen_index - random.randint(10,100)
            
            return random.randint(lower_bound, upper_bound)



    elif server_vector[chosen_index] == '1':
        if '1' in server_vector[:chosen_index] and '1' in server_vector[chosen_index+1:]:
            first_previous_greater, free_space_left = get_first_previous(discovered_vec, chosen_index)
            first_following_greater, free_space_rigth  = get_first_following(discovered_vec, chosen_index)
            upper_bound = (first_previous_greater + 1) + free_space_left
            lower_bound = (first_following_greater - 1) - free_space_rigth
            
            return random.randint(lower_bound, upper_bound)

        elif '1' in server_vector[:chosen_index]:
            first_previous_greater, free_space_left = get_first_previous(discovered_vec, chosen_index)
            upper_bound = chosen_index + random.randint(10,100)
            lower_bound = (first_previous_greater + 1) + free_space_left
            
            return random.randint(lower_bound, upper_bound)

        elif '1' in server_vector[chosen_index+1:]:
            first_following_greater, free_space_rigth  = get_first_following(discovered_vec, chosen_index)
            upper_bound = (first_following_greater - 1) - free_space_rigth
            lower_bound = chosen_index + 1

            return random.randint(lower_bound, upper_bound)

        else:
            lower_bound = chosen_index + 1
            upper_bound = chosen_index + random.randint(10,100)
            
            return random.randint(lower_bound, upper_bound)


def check_goal(opponent, goal, feedback, magic_indexes, user_solution, wasted_dollars, min_questions_worst_case, TAc, LANG):
    # we give feedback based on the chosen optimality level
    if user_solution == ['e'] and magic_indexes==[]:
        isCorrect = True
    else:
        isCorrect = magic_indexes == user_solution

    if isCorrect:

        if wasted_dollars < min_questions_worst_case and opponent=='optimal':
            TAc.print(LANG.render_feedback("correct solution!", f'Correct! But it is impossible to solve the problem asking {wasted_dollars} questions (in the worst case)! You are cheating...'), "yellow", ["bold"])
            exit(0)
    
        #correct
        if goal == 'correct':
            TAc.print(LANG.render_feedback(" correct solution!", f'Correct! You reached your goal'), "green", ["bold"])
            exit(0)

        #at_most_twice_the_opt - al massimo 2 volte la sol ottima
        elif goal == 'at_most_twice_the_opt':
            isAtMostTwice = wasted_dollars <= 2*min_questions_worst_case #compreso il doppio, true if is it at most twice the opt

            if isAtMostTwice:
                TAc.print(LANG.render_feedback(" correct solution!", f'Correct! You reached your goal'), "green", ["bold"])
                exit(0)
            else:
                if feedback == 'yes_no_goal':
                    TAc.print(LANG.render_feedback(" correct solution!", f'Correct! You inserted the right magic indexes, but you wasted too many dollars: you didn\'t reach your goal'), "yellow", ["bold"])
                    exit(0)
                elif feedback == 'how_far':    
                    TAc.print(LANG.render_feedback(" correct solution!", f'Correct! You inserted the right magic indexes, but you wasted {wasted_dollars-2*min_questions_worst_case} more dollars than the optimal solution: you didn\'t reach your goal'), "yellow", ["bold"])             
                    exit(0)

        #opt_plus_one - esattamente la sol ottima + 1
        elif goal == 'opt_plus_one':
            isOptPlusOne = wasted_dollars == min_questions_worst_case + 1 #true if it is exactly opt_plus_one

            if isOptPlusOne:
                TAc.print(LANG.render_feedback(" correct solution!", f'Correct! You reached your goal'), "green", ["bold"])
                exit(0)
            else:
                if feedback == 'yes_no_goal':
                    TAc.print(LANG.render_feedback(" correct solution!", f'Correct! You inserted the right magic indexes, but you wasted too many dollars: you didn\'t reach your goal'), "yellow", ["bold"])
                    exit(0)
                elif feedback == 'how_far':    
                    TAc.print(LANG.render_feedback(" correct solution!", f'Correct! You inserted the right magic indexes, but you wasted {wasted_dollars-(min_questions_worst_case + 1)} more dollars than the optimal solution: you didn\'t reach your goal'), "yellow", ["bold"])             
                    exit(0)

        elif goal == 'optimal':
            isOptimal = wasted_dollars == min_questions_worst_case 
            
            if isOptimal:
                TAc.print(LANG.render_feedback(" correct solution!", f'Correct! You reached your goal'), "green", ["bold"])
                exit(0)
            else:
                if feedback == 'yes_no_goal':
                    TAc.print(LANG.render_feedback(" correct solution!", f'Correct! You inserted the right magic indexes, but you wasted too many dollars: you didn\'t reach your goal'), "yellow", ["bold"])
                    exit(0)
                elif feedback == 'how_far':    
                    TAc.print(LANG.render_feedback(" correct solution!", f'Correct! You inserted the right magic indexes, but you wasted {wasted_dollars-(min_questions_worst_case)} more dollars than the optimal solution: you didn\'t reach your goal'), "yellow", ["bold"])             
                    exit(0)
        
        
                    
    else:
        TAc.print(LANG.render_feedback("wrong solution!", f'Wrong answer! You didn\'t reach your goal'), "red", ["bold"])
        exit(0)
