#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import string

### CONSTANTS #########################################
FORMAT_AVAILABLES = ['dat', 'txt']
DAT_STYLES_AVAILABLES = ['']
TXT_STYLES_AVAILABLES = ['only_strings', 'with_m_and_n']
DEFAULT_FORMAT='only_strings.txt'
#######################################################

def annotated_subseq_to_sequence(solution):
    return [solution.get(key) for key in sorted(solution)]

# TO STRING
def annotated_subseq_to_str(solution):
    return ('\n'.join([f'{solution.get(key)} {key[0]} {key[1]}' for key in sorted(solution)]))


def sequence_to_str(sequence):
    return " ".join(e for e in sequence)


def instance_to_str(problem, format='default'):
    """This function returns the string representation of the given two strings instance according to the indicated format"""
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
    # Get problem in str format
    assert format_primary in FORMAT_AVAILABLES, f'Value [{format_primary}] unsupported for the argument format_primary.'
    if format_primary == 'dat':
        return instance_to_dat(problem, format_secondary)
    if format_primary == 'txt':
        return instance_to_txt(problem, format_secondary)


def instance_to_txt(problem, style='only_strings'):
    """This function returns the string representation of the given two strings instance according to the indicated style"""
    assert style in TXT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    output= ""
    if style == "with_m_and_n":
        output += f'{len(problem[0])} {len(problem[1])}\n'
    output += '\n'.join(sequence_to_str(string) for string in problem)
    return output


def instance_to_dat(problem, style=''):
    """This function returns the dat representation of the given two strings instance according to the indicated style"""
    assert style in DAT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    M = len(problem[0])
    N = len(problem[1])
    output = f"param M := {M};  # Number of characters of the first string s\n"
    output += f"param N := {N};  # Number of characters of the second string t\n"
    output += "param: STRINGS: S_STRING    T_STRING :=\n"
    for j in range(max(M, N)):
        if j < M and j < N:
            output += f'            {j+1} {problem[0][j]}             {problem[1][j]}\n'
        elif j >= M:
            output += f'            {j+1} .               {problem[1][j]}\n'
        elif j >= N:
            output += f'            {j+1} {problem[0][j]}             .\n'
    output = output[:-1] + ";\nend;"
    return output


# FROM STRING
def get_instance_from_str(problem, format):
    """This function returns the string representation of the given two string instances according to the indicated format."""
    # Parsing format
    format_list = format.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = ''
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]
    # Get two strings in str format
    assert format_primary in FORMAT_AVAILABLES, f'Value [{format_primary}] unsupported for the argument format_primary.'
    if format_primary == 'dat':
        return get_instance_from_dat(problem, format_secondary)
    if format_primary == 'txt':
        return get_instance_from_txt(problem, format_secondary)


def get_instance_from_txt(problem, style='only_strings'):
    """This function returns the string representation of the given two strings instance according to the indicated format."""
    assert style in TXT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    instance = list()
    lines = problem.split('\n')
    if style == "with_m_and_n":
        lines = lines[1:]
    for line in lines:
        if len(line) != 0:
            instance.append(line.split())
    return instance


def get_instance_from_dat(problem, style=''):
    """This function returns the string representation of the given two strings instance according to the indicated format."""
    assert style in DAT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    instance = list()
    instance.append(list())
    instance.append(list())
    # Get lines
    lines = problem.split('\n')
    # Parse lines
    for line in lines:
        line = line.strip() # remove whitespace before and after
        # Filter the problem lines
        if line != '' and line[:5] != 'param' and line[:3] != 'end':
            line = line.replace(';', '') #ignore ;
            line = line.split()
            if line[1] != '.':
                instance[0].append((line[1]))
            if line[-1] != '.':
                instance[1].append((line[-1]))
    return instance


# INSTANCE GENERATOR FUNCTIONS:
def gen_instance(m:int,n:int,alphabet:str,seed:int):
    assert m >= 0
    assert n >= 0
    instance_alphabet = get_alphabet(alphabet)
    random.seed(seed)
    problem = []
    problem.append([random.choice(instance_alphabet) for i in range(m)])
    problem.append([random.choice(instance_alphabet) for i in range(n)])
    return problem


# CORE FUNCTIONS:
def get_alphabet(alphabet):
    if alphabet == "lowercase":
        return string.ascii_lowercase
    elif alphabet == "lowercase_uppercase":
        return string.ascii_letters
    else: # alphabet == "dna"
        return "ACGT"


def get_sol(s, t, m, n, sol_style="default"):
    risp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m):
        for j in range(n):
            if s[i] == t[j]:
                risp[i+1][j+1] = 1 + risp[i][j]
            else:
                risp[i+1][j+1] = max(risp[i+1][j],risp[i][j+1])
    if sol_style == "length":
        return risp[m][n]
    else:
        solution = {}
        while m > 0 and n > 0:
            if s[m-1] == t[n-1]:
                solution[(m-1, n-1)] = s[m-1]
                m-=1
                n-=1
            elif risp[m-1][n] > risp[m][n-1]:
                m-=1
            else:
                n-=1
        return solution


def check_input(TAc, LANG, ENV, line):
    if line[0] not in string.ascii_letters:
        TAc.print(LANG.render_feedback('error-first-not-character', '#ERROR: The first element must be the single common character.'), 'red', ['bold'])
        exit(0)
    if line[1] not in string.digits:
        TAc.print(LANG.render_feedback('error-second-not-digit', '#ERROR: The second element must be a digit, corresponding to the index of the common character in the first string.'), 'red', ['bold'])
        exit(0)
    if line[2] not in string.digits:
        TAc.print(LANG.render_feedback('error-third-not-digit', '#ERROR: The third element must be a digit, corresponding to the index of the common character in the second string.'), 'red', ['bold'])
        exit(0)
    if int(line[1]) not in range(ENV['m']):
        TAc.print(LANG.render_feedback('error-second-not-index', f"#ERROR: The second element must be the index of the single common character in the first string. Must be in the range {{0, {ENV['m']}}}."), 'red', ['bold'])
        exit(0)
    if int(line[2]) not in range(ENV['n']):
        TAc.print(LANG.render_feedback('error-second-not-index', f"#ERROR: The second element must be the index of the single common character in the first string.. Must be in the range {{0, {ENV['n']}}}."), 'red', ['bold'])
        exit(0)
    return True


def check_sol(TAc, LANG, ENV, user_sol, s, t):
    sol = get_sol(s, t, len(s), len(t), "length")
    if sol != len(user_sol):
        TAc.print(LANG.render_feedback('error-wrong-sol', f'#ERROR: Your solution differs from the correct one. Your length is {len(user_sol)}, the correct solution length is {sol}.'), 'red', ['bold'])
        return False 
    if ENV['sol_style'] == 'subsequence':
        i = 0
        j = 0
        for char in user_sol:
            s_found = True
            t_found = True
            while i < len(s) and s_found:
                if char == s[i]:
                    s_found = False
                i += 1
            while j < len(t) and t_found:
                if char == t[j]:
                    t_found = False
                j += 1
            if s_found:
                TAc.print(LANG.render_feedback('error-no-matching-char', f'#ERROR: Your solution include a character ({char}) which is not included in the one of the first string.'), 'red', ['bold'])
                return False
            if t_found:
                TAc.print(LANG.render_feedback('error-no-matching-char', f'#ERROR: Your solution include a character ({char}) which is not included in the one of the second string.'), 'red', ['bold'])
                return False
    if ENV['sol_style'] == 'annotated_subseq':
        sorted_keys = sorted(user_sol)
        temp_s = -1
        temp_t = -1
        for pair in sorted_keys:
            if pair[0] == temp_s:
                TAc.print(LANG.render_feedback('error-index-s-duplicate', f'#ERROR: The index {pair[0]} has been referenced twice. You can select a character of a string just one time.'), 'red', ['bold'])
                return False
            if pair[1] == temp_t:
                TAc.print(LANG.render_feedback('error-index-t-duplicate', f'#ERROR: The index {pair[1]} has been referenced twice. You can select a character of a string just one time.'), 'red', ['bold'])
                return False
            if pair[1] < temp_t:
                TAc.print(LANG.render_feedback('error-index-t-unordered', f'#ERROR: The index {pair[1]} is lower than the previous index {temp_t}, but indexes, for both s and t string, must be referenced once and in non decreasing order.'), 'red', ['bold'])
                return False
            if s[pair[0]] != user_sol.get(pair):
                TAc.print(LANG.render_feedback('error-s-no-matching-char', f'#ERROR: The char in position {pair[0]} of the first string is not: {s[pair[0]]}'), 'red', ['bold'])
                return False
            if user_sol.get(pair) != t[pair[1]]:
                TAc.print(LANG.render_feedback('error-t-no-matching-char', f'#ERROR: The char in position {pair[1]} of the second string is not: {t[pair[1]]}'), 'red', ['bold'])
                return False 
            temp_s = pair[0]
            temp_t = pair[1]
    return True


def process_user_sol(TAc, LANG, raw_sol, instance):
    
    sol = {}
    for i, line in enumerate(raw_sol):
        values = line.split()
        for j, e in enumerate(values):
            if e == '1':
                if instance[0][i] == instance[1][j]:
                    sol[(i, j)] = (instance[0][i])  
                else:
                    TAc.print(LANG.render_feedback('solution-no-matching-char', f"The solution.txt file generated by your model contains a wrong character match {instance[0][i]}-{instance[1][j]}."), "red", ["bold"])
                    exit(0)       
    return sol
    