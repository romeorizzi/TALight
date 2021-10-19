#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from bot_interface import service_server_requires_and_gets_the_only_file

# METADATA OF THIS TAL_SERVICE:
problem="board2tok"
service="verify_tiling_server"
args_list = [
    ('m',str),
    ('n',str),
    ('loading', str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
LANG.print_opening_msg()
    
# START CODING YOUR SERVICE:

if ENV['loading'] == 'from_terminal':
    if ENV['m']!='lazy':
        m=int(ENV['m'])
    else:
        TAc.print(LANG.render_feedback("gimme-m", "Insert the number of rows. Parameter m = "), "yellow", ["bold"])
        m=TALinput(
            int,
            num_tokens=1,
            TAc=TAc
        )[0]
    if ENV['n']!='lazy':
        n=int(ENV['n'])
    else:
        TAc.print(LANG.render_feedback("gimme-n", "Insert the number of columns. Parameter n = "), "yellow", ["bold"])
        n=TALinput(
            int,
            num_tokens=1,
            TAc=TAc
        )[0]

    line = ['0'] * n
    TAc.print(LANG.render_feedback("waiting", f"#? Insert your tiling line by line ({m} lines of length {n} over the alphabet {{N,E,S,W,0,1,2,3,4}} as explained by the synopsis service and other documentation of the exercise)."), "yellow")
    for r in range(m):
        prev_line = line
        line = TALinput(
            str,
            num_tokens=1,
            regex=f"^(0|1|2|3|4|N|E|S|W){{{n},{n}}}$",
            TAc=TAc
        )[0]
        if line[0] in {'3','4','E'}: 
            TAc.print(LANG.render_feedback("left-margin", f"The first character of a line can not be a '{line[0]}' for otherwise its tromino exits the left border of your grid."), "red", ["bold"])
            exit(0)
        if line[n-1] in {'1','2','W'}: 
            TAc.print(LANG.render_feedback("right-margin", f"The last character of a line can not be a '{n-1}' for otherwise its tromino exits the right border of your grid."), "red", ["bold"])
            exit(0)
        for j in range(n):
            if (line[j] in {'1','2'} and line[j+1] != 'E') or \
            (j<n-1 and line[j+1] == 'E' and line[j] not in {'1','2'}) or \
            (line[j] == 'W' and line[j+1] not in {'3','4'}) or \
            (j<n-1 and line[j+1] in {'3','4'} and line[j] != 'W'):
                TAc.print(LANG.render_feedback("inconsistent-tromino-row", f"You can not have a `{line[j+1]}` character at the immidiate right of a `{line[j]}` character (see the characters in position {j} and {j+1} of your line)."), "red", ["bold"])
                exit(0)
        if r==0:
            for char in line:
                if char in {'1','4','S'}: 
                    TAc.print(LANG.render_feedback("top-margin", f"No character of the first (topmost) line can be a '{char}' for otherwise its tromino exits the top border of your grid."), "red", ["bold"])
                    exit(0)
        if r==m-1:
            for char in line:
                if char in {'2','3','N'}: 
                    TAc.print(LANG.render_feedback("bottom-margin", f"No character of the last (bottom) line can be a '{char}' for otherwise its tromino exits the bottom border of your grid."), "red", ["bold"])
                    exit(0)
        for j in range(n):
            if (line[j] in {'1','4'} and prev_line[j] != 'N') or \
            (prev_line[j] == 'N' and line[j] not in {'1','4'}) or \
            (line[j] == 'S' and prev_line[j] not in {'2','3'}) or \
            (prev_line[j] in {'2','3'} and line[j] != 'S'):
                TAc.print(LANG.render_feedback("inconsistent-tromino-col", f"You can not have a `{prev_line[j]}` character just above a `{line[j]}` character (check the characters in column {j}, indexes starting from 0)."), "red", ["bold"])
                exit(0)
        
    TAc.print(LANG.render_feedback("correct-tiling", "Well done! You have inserted a correct tiling."), "green", ["bold"])

    exit(0)

else:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input file."), "yellow")
    tiling=service_server_requires_and_gets_the_only_file().decode()
    lines=tiling.splitlines()
    r = 0
    while lines[r][0] == '#':
        r += 1
    m, n = map(int,lines[r].split())
    line = ['#'] * n
    for row_num in range(1,m+1):
        prev_line = line
        r += 1
        while lines[r][0] == '#':
            r += 1
        line = lines[r]
        if line[0] in {'3','4','E'}: 
            TAc.print(LANG.render_feedback("left-margin", f"The first character of a line can not be a '{line[0]}' for otherwise its tromino exits the left border of your grid."), "red", ["bold"])
            exit(0)
        if line[n-1] in {'1','2','W'}: 
            TAc.print(LANG.render_feedback("right-margin", f"The last character of a line can not be a '{n-1}' for otherwise its tromino exits the right border of your grid."), "red", ["bold"])
            exit(0)
        for j in range(n):
            if (line[j] in {'1','2'} and line[j+1] != 'E') or \
            (j<n-1 and line[j+1] == 'E' and line[j] not in {'1','2'}) or \
            (line[j] == 'W' and line[j+1] not in {'3','4'}) or \
            (j<n-1 and line[j+1] in {'3','4'} and line[j] != 'W'):
                TAc.print(LANG.render_feedback("inconsistent-tromino-row", f"You can not have a `{line[j+1]}` character at the immidiate right of a `{line[j]}` character (see the characters in position {j} and {j+1} of your line)."), "red", ["bold"])
                exit(0)
        if row_num==1:
            for char in line:
                if char in {'1','4','S'}: 
                    TAc.print(LANG.render_feedback("top-margin", f"No character of the first (topmost) line can be a '{char}' for otherwise its tromino exits the top border of your grid."), "red", ["bold"])
                    exit(0)
        if row_num==m:
            for char in line:
                if char in {'2','3','N'}: 
                    TAc.print(LANG.render_feedback("bottom-margin", f"No character of the last (bottom) line can be a '{char}' for otherwise its tromino exits the bottom border of your grid."), "red", ["bold"])
                    exit(0)
        for j in range(n):
            if (line[j] in {'1','4'} and prev_line[j] != 'N') or \
            (prev_line[j] == 'N' and line[j] not in {'1','4'}) or \
            (line[j] == 'S' and prev_line[j] not in {'2','3'}) or \
            (prev_line[j] in {'2','3'} and line[j] != 'S'):
                TAc.print(LANG.render_feedback("inconsistent-tromino-col", f"You can not have a `{prev_line[j]}` character just above a `{line[j]}` character (check the characters in row {r} and column {j} of your tiling, indexes starting from 0)."), "red", ["bold"])
                exit(0)

    if ENV['loading'] == 'from_file':
        TAc.print(LANG.render_feedback("correct-tiling", "Well done! You have inserted a correct tiling."), "green", ["bold"])

    exit(0)
