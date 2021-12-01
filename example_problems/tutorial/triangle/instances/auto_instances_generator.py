import random
import sys

def random_triangle(n:int, MIN_VAL:int, MAX_VAL:int, seed:int):
    
    random.seed(seed,version=2)
    triangle = []
    values = [i for i in range (MIN_VAL,MAX_VAL+1)]
    for row in range(0,n):
        triangle.append(random.choices(values, k=row+1))
    return triangle

how_many = 100
seeds = []
for i in range(how_many):
    n = random.randrange(5,101)
    seed = random.randrange(100000,1000000)
    triangle = random_triangle(n, 0, 99,seed)
    seeds.append(seed)
    txt_file = "big_instance_" + str(i) + ".txt"
    output = open(txt_file,"w")
    sys.stdout = output
    print(n)
    for row in triangle:
        print(' '.join([str(ele).ljust(2) for ele in row]))

for i in range(how_many):      
    n = random.randrange(1,6)
    r = random.randint(0,3)
    if r == 0:
        seed = random.randrange(100000,1000000)
    else:
        seed = seeds[i]
    triangle = random_triangle(n, 0, 99,seed)
    txt_file = "small_instance_" + str(i) + ".txt"
    output = open(txt_file,"w")
    sys.stdout = output
    print(n)
    for row in triangle:
        print(' '.join([str(ele).ljust(2) for ele in row]))
