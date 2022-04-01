#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import string

### CONSTANTS #########################################
AVAILABLE_FORMATS = {'instance':{'only_strings':'only_strings.txt', 'with_m_and_n':'with_m_and_n.txt', 'gmpl_dat':'dat'},'solution':{'subseq':'subseq.txt', 'annotated_subseq':'annotated_subseq.txt'}}
DEFAULT_INSTANCE_FORMAT='only_strings'
DEFAULT_SOLUTION_FORMAT='subseq'
#######################################################

def format_name_to_file_extension(format_name, format_gender):
    assert format_gender in AVAILABLE_FORMATS, f'No format has been adopted for objects of the gender `{format_gender}`.'
    assert format_name in AVAILABLE_FORMATS[format_gender], f'Format_name `{format_name}` unsupported for objects of gender {format_gender}.'
    return AVAILABLE_FORMATS[format_gender][format_name]

def file_extension_to_format_name(file_extension):
    for format_gender in AVAILABLE_FORMATS:
        for format_name in AVAILABLE_FORMATS[format_gender]:
            if AVAILABLE_FORMATS[format_gender][format_name] == file_extension:
                return format_name
    assert False, f'No adopted format is associated to the file_extension `{file_extension}`.'

def format_name_expand(format_name, format_gender):
    long_format_name = format_name_to_file_extension(format_name, format_gender)
    format_list = long_format_name.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = None
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]
    return format_primary, format_secondary
    
# MANAGING REPRESENTATIONS OF SOLUTIONS:

def str_to_sequence(string: str) -> list:
    #print(f"str_to_sequence  called with {string=}")
    return [char for char in string]

def sequence_to_str(sequence):
    #print(f"sequence_to_str  called with {sequence=}")
    return "".join(e for e in sequence)

def annotated_subseq_to_sequence(annotated_solution):
    #print(f"annotated_subseq_to_sequence  called with {annotated_solution=}")
    return [annotated_solution[key] for key in sorted(annotated_solution)]

def annotated_subseq_to_str(annotated_solution) -> str:
    #print(f"annotated_subseq_to_str  called with {annotated_solution=}")
    return sequence_to_str(annotated_subseq_to_sequence(annotated_solution))

def render_annotated_subseq_as_str(solution) -> str:
    #print(f"render_annotated_subseq_as_str  called with {solution=}")
    return '\n'.join([f'{solution[key]} {key[0]} {key[1]}' for key in sorted(solution)])

def read_annotated_subseq(raw_annotated_subseq: str):
    #print(f"read_annotated_subseq  called with {raw_annotated_subseq=}")
    sol = {}
    for line in raw_annotated_subseq[:-1].split('\n'):
        values = line.split()
        sol[(int(values[1]), int(values[2]))] = values[0]
    return sol

def check_triple(TAc, LANG, triple, triple_num, s,t):
    spec_error_msg = None
    if triple[0] not in string.ascii_letters:
        spec_error_msg = LANG.render_feedback('error-first-not-character', '#ERROR: The first element of the triple ({}) must be a single character common to s and t.')
    elif not triple[1].isdecimal():
        spec_error_msg = LANG.render_feedback('error-second-not-digit', '#ERROR: The second element of the triple must be a number, corresponding to the index of the common character in the first string.')
    elif not triple[2].isdecimal():
        spec_error_msg = LANG.render_feedback('error-third-not-digit', '#ERROR: The third element of the triple must be a number, corresponding to the index of the common character in the second string.')
    elif int(triple[1]) not in range(len(s)):
        spec_error_msg = LANG.render_feedback('error-second-not-index', f'#ERROR: The second element of the triple must be the index of the common character in the first string (string s, where {len(s)=}). As such, it must be an integer in the semi-closed interval [0, {len(s)}).')
    elif int(triple[2]) not in range(len(t)):
        spec_error_msg = LANG.render_feedback('error-second-not-index', f'#ERROR: The third element of the triple must be the index of the common character in the second string (string t, where {len(t)=}). As such, it must be an integer in the semi-closed interval [0, {len(t)}).')
    elif s[int(triple[1])] != triple[0]:
        spec_error_msg = LANG.render_feedback('wrong-char-in-string-s', f'#ERROR: s[{int(triple[1])}]={s[int(triple[1])]} != \'{triple[0]}\'.')
    elif t[int(triple[2])] != triple[0]:
        spec_error_msg = LANG.render_feedback('wrong-char-in-string-t', f'#ERROR: t[{int(triple[2])}]={t[int(triple[2])]} != \'{triple[0]}\'.')
    if spec_error_msg != None:
        TAc.print(LANG.render_feedback('error-in-triple', f'#ERROR: There is a problem in your annotated solution. The problem is in line {triple_num}, that comprises the three tokens {triple}.'), 'red', ['bold'])
        TAc.print(spec_error_msg, 'red', ['bold'])
        exit(0)


# MANAGING REPRESENTATIONS OF INSTANCES:

# YIELD STRING REPRESENTATIONS OF GIVEN INSTANCE:

def instance_to_str(instance, format_name=DEFAULT_INSTANCE_FORMAT):
    """This function returns the string representation of the given <instance> provided in format <instance_format_name>"""
    format_primary, format_secondary = format_name_expand(format_name, 'instance')
    if format_primary == 'dat':
        return instance_to_dat_str(instance, format_name)
    if format_primary == 'txt':
        return instance_to_txt_str(instance, format_name)

def instance_to_txt_str(instance, format_name=DEFAULT_INSTANCE_FORMAT):
    """Of the given <instance>, this function returns the .txt string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    output= ""
    if format_name == "with_m_and_n":
        output += f'{len(instance[0])} {len(instance[1])}\n'
    output += '\n'.join(sequence_to_str(string) for string in instance)
    return output

def instance_to_dat_str(instance, format_name=''):
    """Of the given <instance>, this function returns the .dat string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    M = len(instance[0])
    N = len(instance[1])
    output = f"param M := {M};  # Number of characters of the first string s\n"
    output += f"param N := {N};  # Number of characters of the second string t\n"
    output += "param: STRINGS: S_STRING    T_STRING :=\n"
    for j in range(max(M, N)):
        if j < M and j < N:
            output += f'            {j+1} {instance[0][j]}             {instance[1][j]}\n'
        elif j >= M:
            output += f'            {j+1} .               {instance[1][j]}\n'
        elif j >= N:
            output += f'            {j+1} {instance[0][j]}             .\n'
    output = output[:-1] + ";\nend;"
    return output


# GET INSTANCE FROM STRING REPRESENTATION:
def get_instance_from_str(instance_as_str, instance_format_name=DEFAULT_INSTANCE_FORMAT):
    """This function returns the instance it gets from its string representation as provided in format <instance_format_name>."""
    format_primary, format_secondary = format_name_expand(instance_format_name, 'instance')
    if format_primary == 'dat':
        return get_instance_from_dat(instance_as_str, instance_format_name)
    if format_primary == 'txt':
        return get_instance_from_txt(instance_as_str, instance_format_name)


def get_instance_from_txt(instance_as_str, instance_format_name='only_strings'):
    """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
    assert instance_format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
    instance = list()
    lines = instance_as_str.split('\n')
    if instance_format_name == "with_m_and_n":
        lines = lines[1:]
    for line in lines:
        if len(line) != 0:
            instance.append(line)
    return instance


def get_instance_from_dat(instance_as_str, format_name=''):
    """This function returns the instance it gets from its .dat string representation in format <format_name>."""
    instance = list()
    instance.append(list())
    instance.append(list())
    lines = instance_as_str.split('\n')
    for line in lines:
        line = line.strip() # remove whitespace before and after
        # Filter the instance_as_str lines
        if line != '' and line[:5] != 'param' and line[:3] != 'end':
            line = line.replace(';', '') #ignore ;
            line = line.split()
            if line[1] != '.':
                instance[0].append((line[1]))
            if line[-1] != '.':
                instance[1].append((line[-1]))
    return instance


# INSTANCE GENERATOR FUNCTIONS:
def shuffle(a:list,b:list):
    pattern = ['a']*len(a)+['b']*len(b)
    random.shuffle(pattern)
    outcome = []
    for p in pattern:
        if p=='a':
            outcome.append(a.pop(0))
        else:
            outcome.append(b.pop(0))
    return outcome
    
def instance_randgen_1(m:int,n:int,alphabet:str,seed:int):
    assert m >= 0
    assert n >= 0
    instance_alphabet = get_alphabet(alphabet)
    random.seed(seed)
    instance = []
    instance.append([random.choice(instance_alphabet) for i in range(m)])
    instance.append([random.choice(instance_alphabet) for i in range(n)])
    return instance

def instance_randgen_2(m:int,n:int,opt_val:int,alphabet:str,seed:int):
    assert m >= 0
    assert n >= 0
    instance_alphabet = get_alphabet(alphabet)
    random.seed(seed)
    instance = []
    opt = [random.choice(instance_alphabet[1:-1]) for i in range(opt_val)]
    instance.append(shuffle(opt, [instance_alphabet[0]] * (m-opt_val)))
    instance.append(shuffle(opt, [instance_alphabet[-1]] * (n-opt_val)))
    return instance


# CORE FUNCTIONS:
def get_alphabet(alphabet):
    if alphabet == "lowercase":
        return string.ascii_lowercase
    elif alphabet == "uppercase":
        return string.ascii_uppercase
    elif alphabet == "lowercase_uppercase":
        return string.ascii_letters
    else: # alphabet == "DNA"
        return "ACGT"


def opt_val_and_sol(s, t):
    """returns the maximum length of a common subsequence of strings s and t, and an optimal LCS(s,t)
    """
    #print(f"opt_val_and_sol called with {s=} and {t=}")
    m = len(s); n = len(t)
    risp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m):
        for j in range(n):
            if s[i] == t[j]:
                risp[i+1][j+1] = 1 + risp[i][j]
            else:
                risp[i+1][j+1] = max(risp[i+1][j],risp[i][j+1])
    opt_val = risp[m][n]
    an_opt_solution = {}
    while m > 0 and n > 0:
        if s[m-1] == t[n-1]:
            an_opt_solution[(m-1, n-1)] = s[m-1]
            m-=1
            n-=1
        elif risp[m-1][n] > risp[m][n-1]:
            m-=1
        else:
            n-=1
    return opt_val, an_opt_solution



def check_sol_feasibility(TAc, LANG, user_sol, sol_format, s, t):
    if sol_format == 'subseq':
        i = 0; j = 0
        for char in user_sol:
            not_yet_found_in_s = True
            not_yet_found_in_t = True
            while not_yet_found_in_s and i < len(s):
                if char == s[i]:
                    not_yet_found_in_s = False
                i += 1
            while not_yet_found_in_t and j < len(t):
                if char == t[j]:
                    not_yet_found_in_t = False
                j += 1
            if not_yet_found_in_s:
                TAc.print(LANG.render_feedback('not-subsequence-of-s', f'# The string produced is NOT a subsequence of s. Here, the string produced is:\n    `{user_sol}`\n# whereas string s is:\n    `{s}`'), 'red', ['bold'])
                return False
            if not_yet_found_in_t:
                TAc.print(LANG.render_feedback('not-subsequence-of-t', f'# The string produced is NOT a subsequence of t. Here, the string produced is:\n    `{user_sol}`\n# whereas string t is:\n    `{s}`'), 'red', ['bold'])
                return False
    if sol_format == 'annotated_subseq':
        sorted_keys = sorted(user_sol)
        prev_i_s = -1; prev_j_t = -1
        prev_pair = None
        for pair in sorted_keys:
            if pair[0] == prev_i_s or pair[1] == prev_j_t:
                TAc.print(LANG.render_feedback('error-duplicated-index', f'# This solution is not feasible since it contains both the pair {pair} and the pair {prev_pair} which share a same coordinate. This means that your subsequence intends to use twice a same character of the including string.'), 'red', ['bold'])
                return False
            if pair[1] < prev_j_t:
                TAc.print(LANG.render_feedback('error-crossing-pairs', f'# This solution is not feasible since it contains both the pair {pair} and the pair {prev_pair} which cross since {prev_pair[0]}<{pair[0]} but  {prev_pair[1]}>{pair[1]}.'), 'red', ['bold'])
                return False
            if s[pair[0]] != user_sol[pair]:
                TAc.print(LANG.render_feedback('error-s-no-matching-char', f'#ERROR: The char in position {pair[0]} of the first string is a `{s[pair[0]]}` and not a `{user_sol[pair]}`.'), 'red', ['bold'])
                return False
            if t[pair[1]] != user_sol[pair]:
                TAc.print(LANG.render_feedback('error-t-no-matching-char', f'#ERROR: The char in position {pair[1]} of the second string is a `{t[pair[0]]}` and not a `{user_sol[pair]}`.'), 'red', ['bold'])
                return False 
            prev_i_s = pair[0]
            prev_j_t = pair[1]
            prev_pair = pair
    return True

def check_sol_feas_and_opt(TAc, LANG, user_sol, sol_format, s, t):
    if not check_sol_feasibility(TAc, LANG, user_sol, sol_format, s, t):
        TAc.print(LANG.render_feedback('not-feasible', f'# The solution produced is NOT feasible. The string `{user_sol}` is NOT a common subsequence of s=`{s}` and t=`{t}`.'), 'red', ['bold'])
        return False
    else:
        TAc.print(LANG.render_feedback('feasible', f'# The solution produced is feasible. Indeed, `{user_sol}` encodes a common subsequence of s=`{s}` and t=`{t}`.'), 'green')
    max_val, an_opt_sol = opt_val_and_sol(s, t)
    assert len(user_sol) <= max_val
    if len(user_sol) < max_val:
        TAc.print(LANG.render_feedback('not-optimal', f'# The solution produced is NOT optimal. Its length is only {len(user_sol)} < {max_val}, where {max_val} is the length of the feasible solution `{an_opt_sol}`.'), 'red', ['bold'])
        return False
    TAc.print(LANG.render_feedback('feasible', f'# Great! The solution produced is feasible and optimal.'), 'green')
    
    return True

