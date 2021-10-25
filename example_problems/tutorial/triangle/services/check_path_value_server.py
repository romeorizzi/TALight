#!/usr/bin/env python3
from sys import stderr, exit
from triangle_lib import *
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors


# METADATA OF THIS TAL_SERVICE:
problem="triangle"
service="check_path_value"
args_list = [
    ('n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('how_to_input_the_triangle',str),
    ('path_value',int),
    ('path',str),
    ('silent',bool),
    ('lang',str),
]


ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 

# TRIANGLE GENERATION

if ENV['how_to_input_the_triangle'] == "lazy":
	triangle = []
	for i in range(1,ENV['n']+1):
		line = input(f"Insert the values of your triangle's line {i}.\n")
		line = line.split()
		line = [int(x) for x in line]
		if len(line) == i:
			triangle.append(line)
		else:
			TAc.print(LANG.render_feedback("wrong_elements_number", f"You inserted {len(line)} elements for line {i} instead of the {i} required."), "red", ["bold"])
			exit(0)
	if not ENV['silent']:
		TAc.print(LANG.render_feedback("right_triangle_insertion", f"Insertion completed."), "yellow", ["bold"])
else:
	triangle = random_triangle(ENV['n'],ENV['MIN_VAL'],ENV['MAX_VAL'],ENV['how_to_input_the_triangle'])

# PRINT TRIANGLE
if not ENV['silent']:
	TAc.print(LANG.render_feedback("triangle_print", f"The triangle you chose is displayed here.\n\n"), "yellow", ["bold"])
	print_triangle(triangle)

# GET PATH

if ENV['path'] == 'lazy':
	print(f"Insert the path as a sequence of L and R with no space in between.")
	path = input()
else:
	path = ENV['path']	
	
# CHECK WHETHER THE PATH CONTAINS ENOUGH DIRECTIONS

if len(path) != ENV['n']-1:
	TAc.print(LANG.render_feedback("wrong_directions_number", f"You inserted {len(path)} directions instead of the {ENV['n']-1} required. Remember not to insert spaces between the letters."), "red", ["bold"])
	exit(0)
elif any(x != "L" and x !="R" for x in path):
	TAc.print(LANG.render_feedback("wrong_direction",f"The path you inserted contains other directions than L or R."),"red", ["bold"])
	exit(0)
	
# CALCOLO PATH
p,s = calculate_path(triangle,path)

if not ENV['silent']:
	TAc.print(LANG.render_feedback("show_path_and_cost",f"The path you chose moves through the following nodes: {p}."),"yellow", ["bold"])
	if int(ENV['path_value']) == s:	
		TAc.print(LANG.render_feedback("right_path_value",f"We agree. The path you chose has cost {s}."),"green", ["bold"])	
if int(ENV['path_value']) != s:	
	TAc.print(LANG.render_feedback("wrong_path_value",f"We don't agree, the path you chose has not cost {ENV['path_value']}."),"red", ["bold"])
	if not ENV['silent']:
		TAc.print(LANG.render_feedback("correct_path_value",f"The path you chose has cost {s} instead."),"yellow", ["bold"])

exit(0)
