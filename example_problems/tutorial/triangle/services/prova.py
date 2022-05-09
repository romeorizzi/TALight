import random
import math
import ast

### CONSTANTS #########################################
AVAILABLE_FORMATS = {'instance':{'pyramid':'pyramid.txt', 'in_lines':'in_lines.txt','triangle_dat':'triangle.dat'},'solution':{'all_solutions': 'all_solutions.txt'}}
DEFAULT_INSTANCE_FORMAT='in_lines'
DEFAULT_SOLUTION_FORMAT='all_solutions'
#######################################################

def random_triangle(n:int, MIN_VAL:int, MAX_VAL:int, seed:int):
    random.seed(seed)
    triangle = []
    values = [i for i in range (MIN_VAL,MAX_VAL+1)]
    for row in range(0,n):
        triangle.append(random.choices(values, k=row+1))
    return triangle

def instance_to_txt_str(instance, format_name="pyramid"):
    """Of the given <instance>, this function returns the .txt string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    triangle = instance['triangle']
    big_triangle = instance['big_triangle']
    n = instance['n']
    m = instance['m']    
    output= f''
    if format_name == 'pyramid':
        for num_linea in range(n):
            output+=f" "*2*(n-1-num_linea)
            array = triangle[num_linea]
            for i in range(num_linea+1):
                el = str(array[i])
                if len(el) == 1:
                    output += el + "   "
                else:
                    output += el + "  "
            output += " "*2*(n-num_linea) + "\n"
        if m!= 0:
            output += "\n#\n\n"
        for num_linea in range(m):
            output+=f" "*2*(m-1-num_linea)
            array = big_triangle[num_linea]
            for i in range(num_linea+1):
                el = str(array[i])
                if len(el) == 1:
                    output += el + "   "
                else:
                    output += el + "  "
            output += " "*2*(m-num_linea) + "\n"
    else:   
        output += f'{n}\n'
        for num_linea in range(n):
            array = triangle[num_linea]
            for el in array:
                output += str(el) + " "
            output += "\n"
        if m!= 0:
            output += "\n#\n\n"
            output += f'{m}\n'
            for num_linea in range(m):
                array = big_triangle[num_linea]
                for el in array:
                    output += str(el) + " "
                output += "\n"
    return output

def get_instance_from_txt(instance_as_str, format_name):
    """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
    instance = {}
    str_to_arr = instance_as_str.split()
    delim = "#"
    if delim in str_to_arr:
        del_index = str_to_arr.index(delim)        
        instance['triangle'] = triangle_from_array([int(x) for x in str_to_arr[:del_index]])
        instance['big_triangle'] = triangle_from_array([int(x) for x in str_to_arr[del_index+1:]])
        instance['n'] = len(instance['triangle'])        
        instance['m'] = len(instance['big_triangle'])        
    else:
        instance['triangle'] = triangle_from_array([int(x) for x in str_to_arr])
        instance['n'] = len(instance['triangle'])        
    return instance

def get_instance_from_dat(instance_as_str, format_name):
    """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
    split_instance = instance_as_str.split(";")
    instance = {}
    if len(split_instance) != 4:
        instance['n'] = int(get_param(split_instance[0])) # assign n
        instance['m'] = int(get_param(split_instance[1])) # assign m
        instance['triangle'] = list(ast.literal_eval(get_param(split_instance[2]).replace("] [","],[").replace(" ",""))) # assign triangle
        instance['big_triangle'] = list(ast.literal_eval(get_param(split_instance[3]).replace("] [","],[").replace(" ",""))) # assign big triangle
    else:
        instance['n'] = int(get_param(split_instance[0])) # assign n
        instance['triangle'] = list(ast.literal_eval(get_param(split_instance[1]).replace("] [","],[").replace(" ","")))
    return instance
    
def instance_to_dat_str(instance,format_name='triangle_dat'):
    """Of the given <instance>, this function returns the .dat string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    triangle = instance['triangle']
    big_triangle = instance['big_triangle']
    n = instance['n']        
    m = instance['m']    
    output = f"param n := {n};                  # Number of lines of the triangle\n"
    if m!= 0:
        output += f"param m := {m};                  # Number of lines of the triangle\n"
    output += "param: SMALL_TRIANGLE "    
    output += f":= {triangle[0]} "
    for i in range(1,n):
        output += f"{triangle[i]} "
    if m!= 0:
        output += ";\nparam: BIG_TRIANGLE "
        output += f":= {big_triangle[0]} "
        for i in range(1,m):
            output += f"{big_triangle[i]} "
    output += ";\nend;"
    return output


def instances_generator(num_instances, scaling_factor: float, MIN_VAL: int, MAX_VAL: int, MIN_N: int, MAX_N: int, MIN_M = 0, MAX_M = 0, seed = "random_seed", big_seed = "random_seed"):
    instances = [] 
    n = MIN_N
    m = MIN_M
    for _ in range(num_instances):
        instance = {}
        # first triangle
        if seed == "random_seed":
            seed = random.randint(100000,999999)
        instance['n'] = n
        instance['triangle'] = random_triangle(n,MIN_VAL,MAX_VAL,seed)
        instance['MIN_VAL'] = MIN_VAL
        instance['MAX_VAL'] = MAX_VAL
        instance['seed'] = seed
        n = math.ceil(scaling_factor*n)
        if n > MAX_N:
            n = MAX_N
        #second triangle
        if big_seed == "random_seed":
            big_seed = random.randint(100000,999999)
        instance['m'] = m
        instance['big_triangle'] = random_triangle(m,MIN_VAL,MAX_VAL,big_seed)
        instance['big_seed'] = big_seed
        m = math.ceil(scaling_factor*m)
        if m > MAX_M:
            m = MAX_M
        instance['measured_time'] = None
        instance['answer_correct'] = None
        instances.append(instance)
    return instances

def triangle_from_array(elements):
    t = []
    i = 0
    j = 1
    while j < len(elements) + 1: 
        t.append(elements[i:j])
        k = i
        i = j
        j += int(math.sqrt(k+j)) + 1
    return t 

def get_param(string):
    answer = ""
    for i in range(1,len(string)):
        if string[-i] == "=":
            return answer[::-1]
        else:
            answer += string[-i]
    return answer[::-1]
       
i = instances_generator(1,1,0,99,3,3,0,0)[0]
t = instance_to_dat_str(i,"triangle_dat")
print(t.split(";"))
print(get_instance_from_dat(t,'triangle_dat'))
