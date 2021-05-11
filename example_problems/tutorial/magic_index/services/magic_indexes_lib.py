import random

def check_input_vector(vec, TAc, LANG):
    for i in range(1,len(vec)):
        if vec[i] == vec[i-1]:
            TAc.print(LANG.render_feedback("equal-values", f'No. Your vector contains entries with the same value vec[{i-1}] = {vec[i-1]} =vec[{i}].'), "red", ["bold"])
            exit(0)
        if vec[i] < vec[i-1]:
            TAc.print(LANG.render_feedback("decrease", f'No. Your vector is not incrisingly sorted: vec[{i-1}] = {vec[i-1]} > {vec[i]} = vec[{i}].'), "red", ["bold"])
            exit(0)

def random_vector(n, seed="any"):
    if seed=="any":
        random.seed()
        seed = random.randrange(0,1000000)
    else:
        seed = int(seed)

    random.seed(seed)
    vec = [random.randint(-10, 1000) for _ in range(n)]
    vec = set(vec) # we remove any duplicates
    vec = list(vec) 
    vec.sort()  # and we sort the list of elements
    
    return vec,seed

def spot_magic_index(vec):
    magic_indexes = []
    for i in range(len(vec)):
        if vec[i]==i:
            magic_indexes.append(i)
    return magic_indexes
