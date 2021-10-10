import random, math

#TO DO: - creare funzione con ricorsione per vettore domande ottimali 
#       - uniformare la funzione per sia generare il vettore di domande per il caso random e pessimo (gioco in modalità optimal) 
#       - sia per controllare il numero di domande minimo da fare nel caso scelto check_n_questions_random_case = num_questions_worst_case. 
#       - testare tutto che funzioni nel caso di giocata random --> optmal necessità di sistemare il discorso della generazione del vettore tramite range dei seed prestabiliti.

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


def generate_optimal_question_vector(vec, low, upper, vector_optmal_questions):
    return []


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



# remove ??
def check_n_questions_random_case(questions_vector):
    return len([i for i in questions_vector if i is not None])

def check_goal(opponent, goal, feedback, magic_indexes, user_solution, vector_optmal_questions, vector_questions, wasted_dollars, min_questions_worst_case, TAc, LANG):
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
            isOptimal = vector_questions == vector_optmal_questions  #true if the sequence of questions in the provided vector is the same of the vector_optmal_questions

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
