#!/usr/bin/env python3
import random

# PER MODALITA' LAZY, GENERIAMO UN TRIANGOLO CASUALE DI n RIGHE

def random_triangle(n,m,M,s):
	random.seed(s,version=2)
	values = []
	for _ in range(0, sum(range(n+1))):
		values.append(random.randrange(m,M))
	return values

# STAMPIAMO IL TRIANGOLO SUL TERMINALE

def print_triangle(n,triangle_array):
	for i in range(len(triangle_array)):
		if len(str(triangle_array[i])) == 1:
			triangle_array[i] = str(triangle_array[i]) + " "
	z = 0
	m = (2 * n) - 2
	for i in range(0, n):
		for j in range(0, m):
		    print(end="  ")
		m = m - 1
		for j in range(0, i + 1):
		    print(triangle_array[z], end='  ')
		    z += 1
		print("  ")
		
def calculate_path(n,triangle,path_directions):
	path = [triangle[0]]
	s = triangle[0]
	i = 0
	last_pos = 0
	for move in path_directions:
		if(move == "L"):
		    path.append(triangle[i+1 + last_pos])
		    s += triangle[i+1 + last_pos]
		    last_pos += i + 1 
		else:
		    path.append(triangle[i+2 + last_pos])
		    s += triangle[i+2 + last_pos]
		    last_pos += i + 2 
		i += 1
	return path,s

def best_path(n, t):
	triangle = t[::-1]
	dist = n
	i  = 0
	count = 1
	while dist > 1:
		triangle[i + dist] = max(triangle[i] + triangle[i + dist], triangle[i + 1] + triangle[i + dist])
		count += 1
		i += 1
		if count == dist:
			count = 1
			dist -= 1
			i += 1
	best_value = triangle[i]
	path_directions = []
	triangle = triangle[::-1]
	last_pos = 0
	for i in range(n-1):
		if triangle[i+1+last_pos] >= triangle[i + 2 + last_pos]:
			path_directions.append("L")
			last_pos += i + 1
		else:
			path_directions.append("R")
			last_pos += i + 2
	path_values, _ = calculate_path(n,t,path_directions)		
	
	return best_value,path_directions,path_values
	
#rtal connect -a how_to_input_the_triangle=100000 triangle check_one_sol


'''		
def recognize(treatement, TAc, LANG, yield_feedback=True):
    assert type(treatement)==str
    #print(f"treatement={treatement}")
    num_dangling_broken_pills = 0
    for char, i in zip(treatement,range(1,len(treatement)+1)):
        if char == 'I':
            num_dangling_broken_pills += 1
        else:
            if num_dangling_broken_pills == 0:
                if yield_feedback:
                    TAc.print(treatement, "yellow", ["underline"])
                    TAc.print(LANG.render_feedback("unfeasible", f"No. On position {i} there is no broken pill left to be eaten. This prescription is not consistent.", {'i': i}), "red", ["bold"])
                    TAc.print(treatement, "yellow", ["underline"])
                    print(" "*(i-1),end="")
                    TAc.print(LANG.render_feedback("pointer", '^ no "H" is available at this point'), "yellow", ["underline"])
                return False
            num_dangling_broken_pills -= 1

    if num_dangling_broken_pills > 0:
        if yield_feedback:
            TAc.print(treatement, "yellow", ["underline"])
            TAc.print(LANG.render_feedback("unfinished", f"No. There are {num_dangling_broken_pills} broken pills left over in the flask. This prescription is not consistent. It contains more 'I' than 'H' characters."), "red", ["bold"])
        return False
    return True


class Triangle:
    def __init__(self):
        pass

    def num_sol(self, n):
        assert 1 <= n
        return 2 ** (n-1)

    def unrank(self, n_pills, pos, sorting_criterion="lovesI"):
        if n_pills == 0:
            return ""
        """I  ... H  ...
               A      B
        """    
        count = 0
        for n_pills_in_A in range(n_pills) if sorting_criterion=="lovesH" else reversed(range(n_pills)):
            num_A = self.num_sol(n_pills_in_A)
            num_B = self.num_sol(n_pills - n_pills_in_A -1)
            if count + num_A*num_B > pos:
                break
            count += num_A*num_B
        return "I" + self.unrank(n_pills_in_A, (pos-count) // num_B, sorting_criterion) + "H" + self.unrank(n_pills - n_pills_in_A -1, (pos-count) % num_B, sorting_criterion)

    def rank(self, treatment, sorting_criterion="lovesI"):
        if treatment == "":
            return 0
        num_dangling_broken_pills = 0
        for char, i in zip(treatment,range(len(treatment))):
            if char == 'I':
                num_dangling_broken_pills += 1
            else:
                num_dangling_broken_pills -= 1
                if num_dangling_broken_pills == 0:
                    break
        assert  i%2 == 1
        """
           I  ... H  ...    with len(A) even
           0   A  i    B
        """
        n_pills = len(treatment)//2
        count = 0
        if sorting_criterion=="lovesI":
            for ii in range(i+2, len(treatment)+1, 2):
                n_pills_A = ii//2
                n_pills_B = n_pills - n_pills_A -1
                num_A = self.num_sol(n_pills_A)
                num_B = self.num_sol(n_pills_B)
                count += num_A*num_B
        if sorting_criterion=="lovesH":
            for ii in range(1, i-1, 2):
                n_pills_A = ii//2
                n_pills_B = n_pills - n_pills_A -1
                num_A = self.num_sol(n_pills_A)
                num_B = self.num_sol(n_pills_B)
                count += num_A*num_B
        n_pills_A = i//2
        n_pills_B = n_pills - n_pills_A -1
        num_B = self.num_sol(n_pills_B)
        return count + self.rank(treatment[1:i], sorting_criterion)*num_B + self.rank(treatment[i+1:len(treatment)+1], sorting_criterion)

    def rand_gen(self, n_pills, seed=None):
        """returns a pseudo-random treatment with <n> I's and H's. The seed univokely determines the treatment."""
        random.seed(seed)
        r = random.randrange(self.num_sol(n_pills))
        return self.unrank(n_pills, r)
    
    def next(self, treatment, sorting_criterion="lovesI"):
        n_pills = len(treatment) // 2
        r = self.rank(treatment, sorting_criterion)
        assert r < self.num_sol(n_pills) -1
        return self.unrank(n_pills, r+1, sorting_criterion)

if __name__ == "__main__":
    p = Triangle(1000)
    assert p.rank("IIHH", 'lovesI') == 0
    assert p.rank("IHIH", 'lovesI') == 1
    assert p.rank("IIHH", 'lovesH') == 1
    assert p.rank("IHIH", 'lovesH') == 0

    assert p.rank("IIIHHH", 'lovesI') == 0
    assert p.rank("IIHIHH", 'lovesI') == 1
    assert p.rank("IIHHIH", 'lovesI') == 2
    assert p.rank("IHIIHH", 'lovesI') == 3
    assert p.rank("IHIHIH", 'lovesI') == 4

    assert p.rank("IIIHHH", 'lovesH') == 4
    assert p.rank("IIHIHH", 'lovesH') == 3
    assert p.rank("IIHHIH", 'lovesH') == 2
    assert p.rank("IHIIHH", 'lovesH') == 1
    assert p.rank("IHIHIH", 'lovesH') == 0

    for n in range(5):
        for r in range(p.num_sol(n)):
            assert p.rank(p.unrank(n, r)) == r
        for _ in range(5):
            #print(p.rand_gen(n))
            assert p.rand_gen(n, _ + 5*n) == p.rand_gen(n, _ + 5*n)
'''
