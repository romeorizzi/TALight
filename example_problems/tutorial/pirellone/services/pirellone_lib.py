#!/usr/bin/env python3
import random, re, copy
from sys import exit


### CONSTANTS #########################################
NO_SOL = 'NO SOLUTION'
FORMAT_AVAILABLES = ['dat', 'txt']
DAT_STYLES_AVAILABLES = ['']
TXT_STYLES_AVAILABLES = ['only_matrix', 'with_m_and_n']
DEFAULT_FORMAT='only_matrix.txt'
#######################################################


# CONVERTERS FUNCTIONS:
def subset_to_seq(subset_sol):
    """Convert subset solution (e.g.: [[0,1],[0,0,1]]) into sequence solution (e.g.: ['r0','c3'])"""
    if subset_sol == NO_SOL:
        return NO_SOL
    m = len(subset_sol[0])
    n = len(subset_sol[1])
    seq_sol = list()
    for i in range(m):
        if subset_sol[0][i]:
            seq_sol.append(f"r{i}")
    for j in range(n):
        if subset_sol[1][j]:
            seq_sol.append(f"c{j}")
    return seq_sol


def seq_to_subset(seq_sol, m, n):
    """Convert sequence solution (e.g.: ['r0','c3']) into subset solution (e.g.: [[0,1],[0,0,1]])"""
    if seq_sol == NO_SOL:
        return NO_SOL
    assert isinstance(seq_sol, list)
    subset_sol = [[0]*m,[0]*n]
    if not seq_sol == ['']:
        for e in seq_sol:
            if e[0] == 'r':
                subset_sol[0][int(e[1:])] = (1-subset_sol[0][int(e[1:])])
            elif e[0] == 'c':
                subset_sol[1][int(e[1:])] = (1-subset_sol[1][int(e[1:])])
            else:
                raise RuntimeError(f'This seq_sol is bad written: {seq_sol}')
    return subset_sol


def check_one_move_seq(move:str, m:int, n:int, TAc, LANG):
    if move.strip()=="":
        return True
    if move[0].upper()=="R":
        return check_row_index(int(move[1:]), m, TAc, LANG)
    else:
        return check_col_index(int(move[1:]), n, TAc, LANG)


def check_row_index(index:int, m:int, TAc, LANG):
    if index < 0 or index >= m:
        TAc.print(LANG.render_feedback("row-index-out-of-range", f"Row index {index} falls outside the valid range [0,{m-1}].", {"m":m}), "red", ["bold"])
        return False
    return True


def check_col_index(index:int, n:int, TAc, LANG):
    if index < 0 or index >= n:
        TAc.print(LANG.render_feedback("col-index-out-of-range", f"Column index {index} falls outside the valid range [0,{n-1}].", {"n":n}), "red", ["bold"])
        return False
    return True


def parse_sol(raw_sol, sol_style, m, n):
    """Parse this raw_sol with sol_style and return the solution in correct format."""
    # Case0: general
    if len(raw_sol) > 2:
        raise RuntimeError('sol-bad-format')
    if (len(raw_sol) == 1) and (raw_sol == [NO_SOL]):
        return NO_SOL
    
    # Case1: sequence style
    sol = list()
    if sol_style == 'seq':
        if len(raw_sol) != 1:
            raise RuntimeError('sol-bad-format')
        # Checks no moves
        if raw_sol == ['']:
            return sol
        sol = raw_sol[0].split()
        for e in sol: 
            if any(not re.match("^((r|R|c|C)[1-9][0-9]*)$", e) for e in sol):
                raise RuntimeError('seq-regex', e)
            # Checks rows
            if (e[0] in ['r', 'R']) and (int(e[1:]) > m):
                raise RuntimeError('seq-row-m', e)
            # Checks cols
            if (e[0] in ['c', 'C']) and (int(e[1:]) > n):
                raise RuntimeError('seq-col-n', e)
        return sol
    
    # Case2: subset style
    elif sol_style == 'subset':
        # Check rows
        rows_switch = raw_sol[0].split()
        if len(rows_switch) != m:
            raise RuntimeError('subset-row-m', len(rows_switch))
        if any([not re.match(f"^(0|1)$", e) for e in rows_switch]):
            raise RuntimeError('subset-regex', raw_sol[0])
        sol.append([int(e) for e in rows_switch])
        # Check cols
        cols_switch = raw_sol[1].split()
        if len(cols_switch) != n:
            raise RuntimeError('subset-col-n', len(cols_switch))
        if any([not re.match(f"^(0|1)$", e) for e in cols_switch]):
            raise RuntimeError('subset-regex', raw_sol[1])
        sol.append([int(e) for e in cols_switch])
        return sol
    
    # Case3: invalid style
    else:
        raise RuntimeError('invalid-sol-style')


# TO STRING
def seq_to_str(seq_sol):
    """From a sequence solution (e.g.: ['r2']) returns its string form (e.g.: 'r2')"""
    if seq_sol == NO_SOL:
        return NO_SOL
    return ' '.join(seq_sol)


def sol_to_str(pirellone, subset_sol):
    """Print the pirellone instance with the rows and cols to be switches"""
    m = len(pirellone)
    n = len(pirellone[0])
    if subset_sol == NO_SOL:
        sol_str =  f'    {"? " * n}'
        sol_str = sol_str[:-1] + '\n'
        sol_str += f'    {"-" * ((m*2)-1)}\n'
        for i in range(m):
            sol_str += f'? | '
            sol_str += ' '.join(str(e) for e in pirellone[i]) + '\n'
    else:
        sol_str = '    ' + ' '.join(str(e) for e in subset_sol[1]) + '\n'
        sol_str += f'    {"-" * (len(subset_sol[1]*2)-1)}\n'
        for i in range(m):
            sol_str += f'{subset_sol[0][i]} | '
            sol_str += ' '.join(str(e) for e in pirellone[i]) + '\n'
    return sol_str[:-1]


def subset_to_str(subset_sol):
    sol = subset_to_str_list(subset_sol)
    if sol == NO_SOL:
        return NO_SOL
    return sol[0] + '\n' + sol[1]


def subset_to_str_list(subset_sol):
    """From a subset solution (e.g.: [[0,1],[0,0]]) returns a list with the rows string and the columns string (e.g.: ['0 1', '0 0']) or NO_SOL"""
    if subset_sol == NO_SOL:
        return NO_SOL
    return [' '.join([str(e) for e in subset_sol[0]]), \
            ' '.join([str(e) for e in subset_sol[1]])]


def instance_to_str(pirellone, format='default'):
    """This function returns the string representation of the given pirellone instance according to the indicated format"""
    # Get default
    format = DEFAULT_FORMAT if format=='default' else format
    # Parsing format
    format_list = format.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = ''
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]
    # Get pirellone in str format
    assert format_primary in FORMAT_AVAILABLES, f'Value [{format_primary}] unsupported for the argument format_primary.'
    if format_primary == 'dat':
        return instance_to_dat(pirellone, format_secondary)
    if format_primary == 'txt':
        return instance_to_txt(pirellone, format_secondary)
    

def instance_to_txt(pirellone, style='only_matrix'):
    """This function returns the string representation of the given pirellone instance according to the indicated style"""
    assert style in TXT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    output = ""
    if style == "with_m_and_n":
        output = f"{len(pirellone)} {len(pirellone[0])}\n"
    return output + '\n'.join((' '.join(str(col) for col in row) for row in pirellone))


def instance_to_dat(pirellone, style=''):
    """This function returns the dat representation of the given pirellone instance according to the indicated style"""
    assert style in DAT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    M = len(pirellone)
    N = len(pirellone[0])
    output = f"param M := {M};  # Number of rows\n"
    output += f"param N := {N};  # Number of columns\n"
    output += "param PIRELLONE :  " + " ".join([str(i) for i in range(1,N+1)]) + " :=\n"
    for i in range(M):
        output += f"               {i+1}   "
        output += ' '.join(str(col) for col in pirellone[i])
        output += ";\n" if i == (M - 1) else "\n"
    output += "end;"
    return output


# FROM STRING
def get_instance_from_str(pirellone, format):
    """This function returns the string representation of the given pirellone instance according to the indicated format."""
    # Parsing format
    format_list = format.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = ''
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]
    # Get pirellone in str format
    assert format_primary in FORMAT_AVAILABLES, f'Value [{format_primary}] unsupported for the argument format_primary.'
    if format_primary == 'dat':
        return get_instance_from_dat(pirellone, format_secondary)
    if format_primary == 'txt':
        return get_instance_from_txt(pirellone, format_secondary)


def get_instance_from_txt(pirellone, style='only_matrix'):
    """This function returns the string representation of the given pirellone instance according to the indicated format."""
    assert style in TXT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    instance = list()
    lines = pirellone.split('\n')
    if format == "with_m_and_n":
        lines = lines[2:]
    for line in lines:
        if len(line) != 0:
            instance.append([int(e) for e in line.split()])
    return instance


def get_instance_from_dat(pirellone, style=''):
    """This function returns the string representation of the given pirellone instance according to the indicated format."""
    assert style in DAT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    instance = list()
    # Get lines
    lines = pirellone.split('\n')
    # Parse lines
    for line in lines:
        line = line.strip() # remove whitespace before and after
        # Filter the matrix lines
        if line != '' and line[:5] != 'param' and line[:3] != 'end':
            line = line.replace(';', '') #ignore ;
            row = list()
            for e in line.split()[1:]:
                row.append(int(e))
            instance.append(row)
    return instance



# PIRELLONE GENERATOR FUNCTIONS:
def is_solvable_seed(seed):
    """Returns True if the given seed would generate a solvable pirellone instance, False otherwise."""
    # We reserve those seed divisible by 3 to the NOT solvable instances
    return (seed % 3) != 0


def gen_instance_seed(solvable=None):
    """This function returns a random seed to generate a pirellone instance with the specificated solvability."""
    random.seed(None)
    seed = random.randint(100002,999999)
    # Check solvability requirement:
    if solvable == None:
        return seed
    # ajust seed if not suitable:
    if solvable != is_solvable_seed(seed):
        # We reserve those seed divisible by 3 to the NOT solvable instances
        if solvable:
            seed -= random.randrange(1, 3)   
        else:
            seed -= (seed % 3)  
    return seed


def gen_instance(m, n, seed:int, with_yes_certificate=False):
    """From (m,n,seed), this functions returns a pirellone instance, with eventually the certificate."""
    assert m >= 0
    assert n >= 0
    must_be_solvable = is_solvable_seed(seed)
    # Generate solution
    random.seed(seed)
    switches_row = [random.randint(0, 1) for _ in range(m)]         
    switches_col = [random.randint(0, 1) for _ in range(n)]
    # Generate instance
    pirellone = [[(switches_col[j] + switches_row[i]) % 2 for j in range(n)] for i in range(m)]
    if not must_be_solvable:
        if m < 2 or n < 2:
            # In this case, the pirellone is always solvable
            raise RuntimeError('invalid-unsolvable-dimensions')
        num_altered_rows = random.randrange(1, m)
        altered_rows = random.sample(range(m), num_altered_rows)
        for row in altered_rows:
            col = random.randrange(0, n)
            pirellone[row][col] = 1-pirellone[row][col]
    if with_yes_certificate:
        return pirellone, [switches_row, switches_col] if must_be_solvable else NO_SOL
    else:
        return pirellone


# CORE FUNCTIONS:
def is_optimal(sol):
    """It assumes that sol contains a valid solution. Returns True if this solution is the minimum one"""
    assert sol != NO_SOL
    m = len(sol[0])
    n = len(sol[1])
    switches_row, switches_col = sol
    return sum(switches_col) + sum(switches_row) <= ((m + n) // 2)


def make_optimal(sol):
    """Returns the optimal solution of a solvable pirellone given a first solution."""
    switches_row = sol[0]
    switches_col = sol[1]
    m = len(switches_row)
    n = len(switches_col)
    if sum(switches_col) + sum(switches_row) > ((m + n) // 2):
        switches_row = [ 1-val for val in switches_row]
        switches_col = [ 1-val for val in switches_col]
    return [switches_row, switches_col]


def get_opt_sol_if_solvable(pirellone):
    """Returns the optimal solution of a solvable pirellone."""
    m = len(pirellone)
    switches_col = pirellone[0]
    if switches_col[0]:
       switches_row = [ 1-pirellone[_][0] for _ in range(m) ]
    else:
       switches_row = [ pirellone[_][0] for _ in range(m) ]
    return make_optimal([switches_row, switches_col])


def check_sol(pirellone, sol):
    """Returns True if sol turns off entirely the pirellone. Otherwise it returns False and an (i, j) such that pirellone[i, j] is set to one after the solution sol gets applied."""
    assert sol != NO_SOL
    m = len(pirellone)
    n = len(pirellone[0])
    switches_row, switches_col = sol
    for i in range(m):
        for j in range(n):
            if pirellone[i][j] != ((switches_row[i] + switches_col[j]) % 2):
                return False, (i, j)
    return True, None


def is_solvable(pirellone, with_yes_certificate=False):
    """From a pirellone instance, this functions returns True if it is solvable, False otherwise."""
    opt_sol = get_opt_sol_if_solvable(pirellone)
    solvable, _ = check_sol(pirellone, opt_sol)
    if with_yes_certificate:
        return solvable, opt_sol if solvable else None
    return solvable


def get_opt_sol(pirellone):
    """Returns NO_SOL if the instance is unsolvable, otherwise the optimal solution."""
    is_solv, opt_sol = is_solvable(pirellone, with_yes_certificate=True)
    if is_solv:
        return opt_sol
    return NO_SOL


def get_padded_sol(m, n, seq_sol, pad_size):
    """From (m,n) and a sequence solution (e.g.: ['r2']), this functions returns a solution longer than at least pad_size."""
    if seq_sol == NO_SOL:
        return NO_SOL
    assert isinstance(seq_sol, list) and all(isinstance(e, str) for e in seq_sol)
    padded_sol = seq_sol.copy()
    diff = pad_size
    turn = 0
    while diff > 0:
        if turn == 0:
            # add fake random row move
            num = f"r{random.randint(1, m)}"
        else:
            # add fake random col move
            num = f"c{random.randint(1, n)}"
        padded_sol.append(num)
        padded_sol.append(num)
        turn = (turn + 1) % 2
        diff -= 2
    random.shuffle(padded_sol)
    return padded_sol



# TESTS
if __name__ == "__main__":
    # CONVERTERS FUNCTIONS:
    print('Test: subset_to_seq()')
    assert subset_to_seq([[0, 0, 1], [0, 1, 0]]) == ['r2', 'c1']
    assert subset_to_seq(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: seq_to_subset()')
    assert seq_to_subset(['r2', 'c1'], 4, 4) == [[0, 0, 1, 0], [0, 1, 0, 0]]
    assert seq_to_subset(['r0', 'c1', 'c1'], 3, 3) == [[1, 0, 0], [0, 0, 0]]
    assert seq_to_subset(NO_SOL, 4, 4) == NO_SOL
    print('==> OK\n')


    # TO_STRING and FROM_STRING FUNCTIONS:
    print('Test: seq_to_str()')
    assert seq_to_str(['r3', 'c2']) == 'r3 c2'
    assert seq_to_str(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: sol_to_str()')
    assert sol_to_str([[0, 0], [1, 1]], [[0, 1], [0, 0]]) == \
        "    0 0\n" + \
        "    ---\n" + \
        "0 | 0 0\n" + \
        "1 | 1 1"
    assert sol_to_str([[0, 0], [0, 1]], NO_SOL) == \
        "    ? ?\n" + \
        "    ---\n" + \
        "? | 0 0\n" + \
        "? | 0 1"
    print('==> OK\n')


    print('Test: subset_to_str()')
    assert subset_to_str([[0, 0, 1], [0, 1, 0]]) == "0 0 1\n0 1 0"
    assert subset_to_str(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: subset_to_str_list()')
    assert subset_to_str_list([[0, 0, 1], [0, 1, 0]]) == ['0 0 1', '0 1 0']
    assert subset_to_str_list(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: instance_to_str()')
    assert instance_to_str([[0, 0], [1, 1]]) == '0 0\n1 1'
    print('==> OK\n')


    print('Test: instance_to_txt()')
    print('MAYBE TODO?')
    print('==> OK\n')


    print('Test: instance_to_dat()')
    print('MAYBE TODO?')
    print('==> OK\n')


    print('Test: get_instance_from_str()')
    print('==> OK\n')


    print('Test: get_instance_from_txt()')
    assert get_instance_from_txt('0 0\n1 1', 'only_matrix') == [[0, 0], [1, 1]]
    print('==> OK\n')


    print('Test: get_instance_from_dat()')
    dat_instance = \
        "param M := 10;  # Number of rows\n" + \
        "param N := 2;  # Number of columns\n" + \
        "param PIRELLONE :  1 2 3 4 5 6 7 8 9 10:=\n" + \
        "                           \n" + \
        "              1    1 0 1 1 0 1 0 0 0 1   \n" + \
        "                                            \n" + \
        "\n" + \
        "              2    0 1 0 0 1 0 0 1 1 1 ;\n" + \
        "end;\n"
    assert get_instance_from_dat(dat_instance)  == [[1, 0, 1, 1, 0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 1, 0, 0, 1, 1, 1]]
    dat_instance = \
        "param M := 2;  # Number of rows\n" + \
        "param N := 2;  # Number of columns\n" + \
        "param PIRELLONE :  1 2:=\n" + \
        "                           \n" + \
        "              1    1 0   \n" + \
        "                                            \n" + \
        "\n" + \
        "              2    0 1;\n" + \
        "end;\n"
    assert get_instance_from_dat(dat_instance)  == [[1, 0], [0, 1]]
    print('==> OK\n')


    # PIRELLONE GENERATOR FUNCTIONS:
    print('Test: is_solvable_seed()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: gen_instance_seed()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: gen_instance()')
    print('MAYBE TODO?')
    print('==> OK\n')


    # CORE FUNCTIONS:
    print('Test: is_optimal()')
    assert is_optimal([[0, 0],[0, 0]])
    assert is_optimal([[0, 0],[0, 1]])
    assert is_optimal([[0, 0],[1, 0]])
    assert is_optimal([[0, 0],[1, 1]])
    assert is_optimal([[0, 1],[0, 0]])
    assert is_optimal([[0, 1],[0, 1]])
    assert is_optimal([[0, 1],[1, 0]])
    assert not is_optimal([[0, 1],[1, 1]])
    assert is_optimal([[1, 0],[0, 0]])
    assert is_optimal([[1, 0],[0, 1]])
    assert is_optimal([[1, 0],[1, 0]])
    assert not is_optimal([[1, 0],[1, 1]])
    assert is_optimal([[1, 1],[0, 0]])
    assert not is_optimal([[1, 1],[0, 1]])
    assert not is_optimal([[1, 1],[1, 0]])
    assert not is_optimal([[1, 1],[1, 1]])
    print('==> OK\n')


    print('Test: make_optimal()')
    assert make_optimal([[0, 0], [0, 0]]) == [[0, 0], [0, 0]]
    assert make_optimal([[0, 0], [0, 1]]) == [[0, 0], [0, 1]]
    assert make_optimal([[0, 0], [1, 0]]) == [[0, 0], [1, 0]]
    assert make_optimal([[0, 0], [1, 1]]) == [[0, 0], [1, 1]]
    assert make_optimal([[0, 1], [0, 0]]) == [[0, 1], [0, 0]]
    assert make_optimal([[0, 1], [0, 1]]) == [[0, 1], [0, 1]]
    assert make_optimal([[0, 1], [1, 0]]) == [[0, 1], [1, 0]]
    assert make_optimal([[1, 0], [0, 0]]) == [[1, 0], [0, 0]]
    assert make_optimal([[1, 0], [0, 1]]) == [[1, 0], [0, 1]]
    assert make_optimal([[1, 0], [1, 0]]) == [[1, 0], [1, 0]]
    assert make_optimal([[1, 1], [0, 0]]) == [[1, 1], [0, 0]]
    assert make_optimal([[0, 1], [1, 1]]) == [[1, 0], [0, 0]] #not_optimal
    assert make_optimal([[1, 0], [1, 1]]) == [[0, 1], [0, 0]] #not_optimal
    assert make_optimal([[1, 1], [0, 1]]) == [[0, 0], [1, 0]] #not_optimal
    assert make_optimal([[1, 1], [1, 0]]) == [[0, 0], [0, 1]] #not_optimal
    assert make_optimal([[1, 1], [1, 1]]) == [[0, 0], [0, 0]] #not_optimal
    print('==> OK\n')


    print('Test: get_opt_sol_if_solvable() in solvable instances')
    assert get_opt_sol_if_solvable([[0, 0], [0, 0]]) == [[0, 0],[0, 0]]
    assert get_opt_sol_if_solvable([[0, 0], [1, 1]]) == [[0, 1],[0, 0]]
    assert get_opt_sol_if_solvable([[0, 1], [0, 1]]) == [[0, 0],[0, 1]]
    assert get_opt_sol_if_solvable([[0, 1], [1, 0]]) in [[[1, 0],[1, 0]],
                                                        [[0, 1],[0, 1]]]
    assert get_opt_sol_if_solvable([[1, 0], [0, 1]]) in [[[1, 0],[0, 1]],
                                                        [[0, 1],[1, 0]]]
    assert get_opt_sol_if_solvable([[1, 0], [1, 0]]) == [[0, 0],[1, 0]]
    assert get_opt_sol_if_solvable([[1, 1], [0, 0]]) == [[1, 0],[0, 0]]
    assert get_opt_sol_if_solvable([[1, 1], [1, 1]]) in [[[1, 1],[0, 0]],
                                                        [[0, 0],[1, 1]]]
    print('Test: get_opt_sol_if_solvable() in NOT solvable instances')
    print('THIS BEHAVIOR MAKES NO SENSE ')
    # print( get_opt_sol_if_solvable([[0, 0], [0, 1]]) )
    # print( get_opt_sol_if_solvable([[0, 0], [1, 0]]) )
    # print( get_opt_sol_if_solvable([[0, 1], [0, 0]]) )
    # print( get_opt_sol_if_solvable([[0, 1], [1, 1]]) )
    # print( get_opt_sol_if_solvable([[1, 0], [0, 0]]) )
    # print( get_opt_sol_if_solvable([[1, 0], [1, 1]]) )
    # print( get_opt_sol_if_solvable([[1, 1], [0, 1]]) )
    # print( get_opt_sol_if_solvable([[1, 1], [1, 0]]) )
    print('==> OK\n')


    print('Test: check_sol() in solvable instances with CORRECT sol')
    assert check_sol([[0, 0], [0, 0]],  [[0, 0], [0, 0]]) == (True, None)
    assert check_sol([[0, 0], [1, 1]],  [[0, 1], [0, 0]]) == (True, None)
    assert check_sol([[0, 1], [0, 1]],  [[0, 0], [0, 1]]) == (True, None)
    assert check_sol([[0, 1], [1, 0]],  [[0, 1], [0, 1]]) == (True, None)
    assert check_sol([[1, 0], [0, 1]],  [[0, 1], [1, 0]]) == (True, None)
    assert check_sol([[1, 0], [1, 0]],  [[0, 0], [1, 0]]) == (True, None)
    assert check_sol([[1, 1], [0, 0]],  [[1, 0], [0, 0]]) == (True, None)
    assert check_sol([[1, 1], [1, 1]],  [[1, 1], [0, 0]]) == (True, None)
    print('Test: check_sol() in solvable instances with WRONG sol')
    assert check_sol([[0, 0], [0, 0]],  [[0, 1], [0, 0]]) == (False, (1, 0))
    assert check_sol([[0, 0], [1, 1]],  [[0, 1], [1, 0]]) == (False, (0, 0))
    assert check_sol([[0, 1], [0, 1]],  [[0, 1], [0, 0]]) == (False, (0, 1))
    assert check_sol([[0, 1], [1, 0]],  [[0, 1], [0, 0]]) == (False, (0, 1))
    assert check_sol([[1, 0], [0, 1]],  [[0, 0], [0, 1]]) == (False, (0, 0))
    assert check_sol([[1, 0], [1, 0]],  [[0, 0], [1, 1]]) == (False, (0, 1))
    assert check_sol([[1, 1], [0, 0]],  [[1, 1], [0, 0]]) == (False, (1, 0))
    assert check_sol([[1, 1], [1, 1]],  [[0, 1], [0, 0]]) == (False, (0, 0))
    print('Test: check_sol() in NOT solvable instances')
    assert check_sol([[0, 0], [0, 1]],  [[0, 0], [0, 0]]) == (False, (1, 1))
    assert check_sol([[0, 0], [1, 0]],  [[0, 0], [0, 0]]) == (False, (1, 0))
    assert check_sol([[0, 1], [0, 0]],  [[0, 0], [0, 0]]) == (False, (0, 1))
    assert check_sol([[0, 1], [1, 1]],  [[0, 0], [0, 0]]) == (False, (0, 1))
    assert check_sol([[1, 0], [0, 0]],  [[0, 0], [0, 0]]) == (False, (0, 0))
    assert check_sol([[1, 0], [1, 1]],  [[0, 0], [0, 0]]) == (False, (0, 0))
    assert check_sol([[1, 1], [0, 1]],  [[0, 0], [0, 0]]) == (False, (0, 0))
    assert check_sol([[1, 1], [1, 0]],  [[0, 0], [0, 0]]) == (False, (0, 0))
    print('==> OK\n')


    print('Test: is_solvable() in solvable instances WITHOUT certificate')
    assert is_solvable([[0, 0], [0, 0]])
    assert is_solvable([[0, 0], [1, 1]])
    assert is_solvable([[0, 1], [0, 1]])
    assert is_solvable([[0, 1], [1, 0]])
    assert is_solvable([[1, 0], [0, 1]])
    assert is_solvable([[1, 0], [1, 0]])
    assert is_solvable([[1, 1], [0, 0]])
    assert is_solvable([[1, 1], [1, 1]])
    print('Test: is_solvable() in NOT solvable instances WITHOUT certificate')
    assert not is_solvable([[0, 0], [0, 1]])
    assert not is_solvable([[0, 0], [1, 0]])
    assert not is_solvable([[0, 1], [0, 0]])
    assert not is_solvable([[0, 1], [1, 1]])
    assert not is_solvable([[1, 0], [0, 0]])
    assert not is_solvable([[1, 0], [1, 1]])
    assert not is_solvable([[1, 1], [0, 1]])
    assert not is_solvable([[1, 1], [1, 0]])
    print('Test: is_solvable() in solvable instances WITH certificate')
    instance = [[0, 0], [0, 0]]
    assert is_solvable(instance, True) == (True, get_opt_sol_if_solvable(instance))
    instance = [[0, 0], [1, 1]]
    assert is_solvable(instance, True) == (True, get_opt_sol_if_solvable(instance))
    instance = [[0, 1], [0, 1]]
    assert is_solvable(instance, True) == (True, get_opt_sol_if_solvable(instance))
    instance = [[0, 1], [1, 0]]
    assert is_solvable(instance, True) == (True, get_opt_sol_if_solvable(instance))
    instance = [[1, 0], [0, 1]]
    assert is_solvable(instance, True) == (True, get_opt_sol_if_solvable(instance))
    instance = [[1, 0], [1, 0]]
    assert is_solvable(instance, True) == (True, get_opt_sol_if_solvable(instance))
    instance = [[1, 1], [0, 0]]
    assert is_solvable(instance, True) == (True, get_opt_sol_if_solvable(instance))
    instance = [[1, 1], [1, 1]]
    assert is_solvable(instance, True) == (True, get_opt_sol_if_solvable(instance))
    print('Test: is_solvable() in NOT solvable instances WITH certificate')
    assert is_solvable([[0, 0], [0, 1]], True) == (False, None)
    assert is_solvable([[0, 0], [1, 0]], True) == (False, None)
    assert is_solvable([[0, 1], [0, 0]], True) == (False, None)
    assert is_solvable([[0, 1], [1, 1]], True) == (False, None)
    assert is_solvable([[1, 0], [0, 0]], True) == (False, None)
    assert is_solvable([[1, 0], [1, 1]], True) == (False, None)
    assert is_solvable([[1, 1], [0, 1]], True) == (False, None)
    assert is_solvable([[1, 1], [1, 0]], True) == (False, None)
    print('==> OK\n')


    print('Test: get_opt_sol()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: get_padded_sol_seq()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: others')
    instance = [[0, 1], [0, 1]]
    assert get_opt_sol_if_solvable(instance) == [[0, 0], [0, 1]]
    subset_not_minimal = [[1, 1], [1, 0]]
    assert check_sol(instance, subset_not_minimal) == (True, None)
    assert not is_optimal(subset_not_minimal)
    seq_not_minimal = ['r0', 'c1', 'r0']
    assert check_sol(instance, seq_to_subset(seq_not_minimal, 2, 2)) == (True, None)
    assert is_optimal(seq_to_subset(seq_not_minimal, 2, 2)) #Note this

    print('==> OK\n')


    print("FINISH")













####DA SISTEMARE TUTTI I CHECK OFF LIGHTS 


def random_pirellone(m, n, seed="random_seed", solvable=False, s=False):
    if seed=="random_seed":
        random.seed()
        seed = random.randrange(0,1000000)
    else:
        seed = int(seed)
    random.seed(seed)
    switches_row = [random.randint(0, 1) for _ in range(m)]         
    switches_col = [random.randint(0, 1) for _ in range(n)]
    pirellone = [ [ (switches_col[j] + switches_row[i]) % 2 for j in range(n) ] for i in range(m)]
    if not solvable:
        ar=[]
        ac=[]
        k=random.randrange(1, m+n)
        for _ in range(k):
            row = random.randrange(0, m)
            col = random.randrange(0, n)
            if row not in ar and col not in ac:
                pirellone[row][col] = 1-pirellone[row][col] 
    if s:
        return pirellone, seed, switches_row, switches_col
    else:
        return pirellone, seed

def extract_sol(line, m, n, LANG, TAc):
    matched = re.match("^((\n*(r|c)[1-9][0-9]{0,3})*\n*)$", line)
    if not bool(matched):
        TAc.print(LANG.render_feedback("wrong-sol-line",f'# Error! The line with your solution ({line}) is not accordant (it does not match the regular expression "^((\n*(r|c)[1-9][0-9]{0,3})*\n*)$"'), "red", ["bold"])
        exit(0)
    switch_rows = [0]*m
    switch_cols = [0]*n
    moves = line.split()
    for move,i in zip(moves,len(moves)):
        index = int(move[1:])
        if move[0] == "r":
            if index > m:
                TAc.print(LANG.render_feedback("row-index-exceeds-m",f'# Error! In your solution line ({line}) the {i}-th move ({move}) is not applicable. Indeed, {index}>{m}=m.'), "red", ["bold"])
                exit(0)
            switch_rows[index] = 1-switch_rows[index]
        if move[0] == "c":
            if index > n:
                TAc.print(LANG.render_feedback("column-index-exceeds-n",f'# Error! In your solution line ({line}) the {i}-th move ({move}) is not applicable. Indeed, {index}>{n}=n.'), "red", ["bold"])
                exit(0)
            switch_cols[index] = 1-switch_cols[index]
    return switch_rows, switch_cols

    
    
def switch_row(i,pirellone):
    for j in range(len(pirellone[0])):
        pirellone[i][j] = int(not pirellone[i][j])

def switch_col(j,pirellone):
    for i in range(len(pirellone)):
        pirellone[i][j] = int(not pirellone[i][j])

def is_solvable(pirellone):
    for i in range(len(pirellone)):
        inv = pirellone[0][0] != pirellone[i][0]
        for j in range(len(pirellone[0])):
            v = not pirellone[i][j] if inv else pirellone[i][j]
            if v != pirellone[0][j]:
                return False
    return True 

def print_pirellone(pirellone):
    for l in pirellone:
        print(*l) 
        
def check_off_lights(pirellone,solu, LANG, TAc):
    pirellone1=[line[:] for line in pirellone]
    m=len(pirellone)
    n=len(pirellone[0])
    empty=[[0 for j in range(0,len(pirellone[0]))] for i in range(0,len(pirellone))]
    for i in range(0,len(solu)):
        if solu[i][0]=='r':
            if int(solu[i][1:]) > m:
                TAc.print(LANG.render_feedback("row-index-exceeds-m",f'# Error! In your solution the move ({solu[i]}) is not applicable. Indeed, {int(solu[i][1:])}>{m}.'), "red", ["bold"])
                exit(0)
            switch_row(int(solu[i][1:])-1,pirellone)
        elif solu[i][0]=='c':
            if int(solu[i][1:]) > n:
                TAc.print(LANG.render_feedback("col-index-exceeds-n",f'# Error! In your solution the move ({solu[i]}) is not applicable. Indeed, {int(solu[i][1:])}>{n}.'), "red", ["bold"])
                exit(0)
            switch_col(int(solu[i][1:])-1,pirellone)
    if is_solvable(pirellone):             
        if empty==pirellone:
                return True,'s'
        else: 
                return False,'s'
    else:
        lights=0
        for i in range(len(pirellone)):
            lights+=sum(pirellone[i]) 
        if lights==(min_lights_on(pirellone1)):
            return True,'n'
        else:
            return False,'n'

def solution_min(switches_row,switches_col):
    m=len(switches_row)
    n=len(switches_col)
    num_one=sum(switches_col)+sum(switches_row)
    if num_one>m+n-num_one:
        switches_row = [ 1-val for val in switches_row]
        switches_col = [ 1-val for val in switches_col]
    lista=[]
    for i in range(m):
        if switches_row[i]:
            lista.append(f"r{i+1}")
    for j in range(n):
        if switches_col[j]:
            lista.append(f"c{j+1}")
    return lista
        
def solution(pirellone):
    m=len(pirellone)
    n=len(pirellone[0]) 
    sr=[]
    sc=[]
    for j in range(n):
        if pirellone[0][j]:
            sc.append(j)
            switch_col(j,pirellone)
    for i in range(1,m):
        if pirellone[i][0]:
            sr.append(i)
            switch_row(i,pirellone)
    if len(sr)+len(sc)>= (m+n)//2:
        switches_row=[]
        switches_col=[]
        for j in range(n):
            if j not in sc:
                switches_col.append(j)
        for i in range(m):
            if i not in sr:
                switches_row.append(i)
    else:
        switches_row=sr
        switches_col=sc
    lista=[]
    for i in switches_row:
        lista.append(f"r{i+1}")
    for j in switches_col:
        lista.append(f"c{j+1}")
    return lista
        
#forse non corretta la seguente funzione            
def solution_irredundant(pirellone,switches_row,switches_col,smallest=True):
    m=len(switches_row)
    n=len(switches_col)
    assert is_solvable(pirellone)
    switches_row = pirellone[0]
    if pirellone[0][0] == 0:
        switches_col = pirellone[0]
    else:    
        switches_row = [ 1-pirellone[i][0] for i in range(m) ]
    if smallest != (sum(switches_col)+sum(switches_row) <= (m+n)//2):
        switches_row = [ 1-val for val in switches_row]
        switches_col = [ 1-val for val in switches_col]
    
    [random.randint(0, 1) for _ in range(m)]         
    switches_col = [random.randint(0, 1) for _ in range(n)]
    pirellone = [ [ (switches_col[j] + switches_row[i]) % 2 for j in range(n) ] for i in range(m)]

    lista=[]
    for i in range(m):
        if switches_row[i]:
            lista.append(f"r{i+1}")
    for j in range(n):
        if switches_col[j]:
            lista.append(f"c{j+1}")
    return lista

def solution_pad(sol,m,n,lb,seed="random_seed"):
    if type(seed)==str:
        assert seed=="random_seed"
        random.seed()
        seed = random.randrange(0,1000000)
    random.seed(seed)  
    longsol=sol
    while len(longsol)<lb:
        num=f"r{random.randint(1,m)}" 
        longsol.append(num)
        longsol.append(num)
        num=f"c{random.randint(1,n)}"
        longsol.append(num)
        longsol.append(num)      
    random.shuffle(longsol)
    return longsol



def min_lights_on(pirellone):
    s=0
    h=1
    k=1
    while h!=0 or k!=0:
        h=0
        k=0
        for i in range(len(pirellone)):
            if sum(pirellone[i])>(len(pirellone)-sum(pirellone[i])):
                switch_row(i,pirellone)
                h+=1      
        for j in range(len(pirellone[0])):
            for i in range(len(pirellone)):
                s+=pirellone[i][j]
            if s>(len(pirellone[0])-s):
                switch_col(j,pirellone)
                k+=1
            s=0   
    light=0
    for i in range(len(pirellone)):
        light+=sum(pirellone[i]) 
    return light
    
     

