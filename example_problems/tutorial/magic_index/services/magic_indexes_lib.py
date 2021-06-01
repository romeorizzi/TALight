import random

def check_input_vector(vec, TAc, LANG):
    for i in range(1,len(vec)):
        if vec[i] == vec[i-1]:
            TAc.print(LANG.render_feedback("equal-values", f'No. Your vector contains entries with the same value vec[{i-1}] = {vec[i-1]} =vec[{i}].'), "red", ["bold"])
            exit(0)
        if vec[i] < vec[i-1]:
            TAc.print(LANG.render_feedback("decrease", f'No. Your vector is not incrisingly sorted: vec[{i-1}] = {vec[i-1]} > {vec[i]} = vec[{i}].'), "red", ["bold"])
            exit(0)

def random_vector(n, seed="random_seed"):
    if seed=="random_seed":
        random.seed()
        seed = random.randrange(0,1000000)
    else:
        seed = int(seed)
    random.seed(seed)
    first_magic = random.randint(0,n-1)
    last_magic = random.randint(0,n-1)
    vec = list(range(n))
    for i in range(last_magic+1,n):
        vec[i] = vec[i-1] + random.randint(2, 5)
    if first_magic > last_magic:
        first_magic = last_magic +1
    for i in range(first_magic-1,-1,-1):
        vec[i] = vec[i+1] - random.randint(2, 5)    
    return vec,seed

def spot_magic_index(vec):
    magic_indexes = []
    for i in range(len(vec)):
        if vec[i]==i:
            magic_indexes.append(i)
    return magic_indexes