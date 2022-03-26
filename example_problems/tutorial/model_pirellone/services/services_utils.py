#!/usr/bin/env python3
"""This file contains the useful functions used in more services of the 'Pirellone' problem."""
import random

from TALinputs import TALinput
from bot_file_exchange_sym_interface import service_server_requires_and_gets_the_only_file

import pirellone_lib as pl


def process_instance(ENV, TAc, LANG):
    if ENV['instance_spec'] == 'random':
        # Get random seed
        seed = pl.gen_instance_seed()
        # Get instance
        try:
            # instance, certificate= pl.gen_instance(ENV['m'], ENV['n'], seed, with_yes_certificate=True)
            instance, certificate= pl.gen_instance(4, 4, seed, with_yes_certificate=True)
        except RuntimeError:
            TAc.print(LANG.render_feedback("error", f"Can't generate an unsolvable matrix {ENV['m']}x{ENV['n']}."), "red", ["bold"])
            exit(0)
        TAc.print(LANG.render_feedback("seed", f"The seed is: {seed}"), "yellow", ["bold"])
        # Print instance
        TAc.print(LANG.render_feedback("instance-title", f"The matrix {len(instance)}x{len(instance[1])} is:"), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("instance", f"{pl.instance_to_str(instance)}"), "white", ["bold"])
        # Returns instance and optimal solution
        return instance, pl.make_optimal(certificate) if pl.is_solvable_seed(seed) else pl.NO_SOL

    elif ENV['instance_spec'] == 'seed':
        if ENV['seed'] == 0:
            TAc.print(LANG.render_feedback("no-mandatory-seed", f"If you select (instance_spec='seed') then the (seed) argument must be differente from 000000"), "red", ["bold"])
            exit(0)
        # Get instance
        try:
            instance, certificate = pl.gen_instance(ENV['m'], ENV['n'], ENV['seed'], with_yes_certificate=True)
        except RuntimeError:
            TAc.print(LANG.render_feedback("error", f"Can't generate an unsolvable matrix {ENV['m']}x{ENV['n']}."), "red", ["bold"])
            exit(0)
        # Print instance
        TAc.print(LANG.render_feedback("instance-title", f"The matrix {ENV['m']}x{ENV['n']} is:"), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("instance", f"{pl.instance_to_str(instance)}"), "white", ["bold"])
        # Returns instance and optimal solution
        return instance, pl.make_optimal(certificate) if pl.is_solvable_seed(ENV['seed']) else pl.NO_SOL


    elif ENV['instance_spec'] == 'terminal':
        TAc.print(LANG.render_feedback("waiting", f"#? waiting for the pirellone {ENV['m']}x{ENV['n']}.\nFormat: each line is a row of the matrix and each colomun must be separeted by space.\nAny line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the raw_sol of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself."), "yellow")
        TAc.print(LANG.render_feedback("instance-title", f"Matrix {ENV['m']}x{ENV['n']}:"), "yellow", ["bold"])
        # Get pirellone instance
        instance = list()
        for _ in range(ENV['m']):
            instance.append(TALinput(int, num_tokens=ENV['n'], sep=' ', TAc=TAc))
        # Returns instance and optimal solution
        return instance, pl.get_opt_sol(instance)

    # elif ENV['instance_spec'] == 'TA_transfer_files_bot':
    #     TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input file (handler `pirellone.txt`)."), "yellow")
    #     # get pirellone instance
    #     instance_str = service_server_requires_and_gets_the_only_file().decode()
    #     instance = pl.get_instance_from_str(instance_str)
    #     # Get optimal solution
    #     sol = pl.get_opt_sol(instance)
    

def get_user_sol(ENV, TAc, LANG, style):
    TAc.print(LANG.render_feedback("usersol-title", "Your solution: "), "yellow", ["reverse"])
    # Get the user solution
    user_sol = list()
    if style == 'seq':
        user_sol = TALinput(str,regex="^\s*|(r|c)(0|[1-9][0-9]{0,2})$", regex_explained="a single row or column (with indexes starting from 0). Example 1: r0 to specify the first row. Example 2: c2 to specify the third column.", token_recognizer=lambda move,TAc,LANG: pl.check_one_move_seq(move,ENV['m'],ENV['n'],TAc,LANG), line_explained="a subset of rows and columns where indexes start from 0. Example: r0 c5 r2 r7", TAc=TAc, LANG=LANG)
    if style == 'subset':
        # Get rows
        user_sol_rows = TALinput(bool, num_tokens=ENV['m'], line_explained=f"a line consisting of {ENV['m']} binary digits (0/1) separated by spaces, one for each row. A row gets switched iff the corresponding digit is a 1. Example: {' '.join(str(random.randint(0,1)) for _ in range(ENV['m']))}", TAc=TAc, LANG=LANG)
        user_sol.append(user_sol_rows)
        # Get cols
        user_sol_cols = TALinput(bool, num_tokens=ENV['n'], line_explained=f"a line consisting of {ENV['n']} binary digits (0/1) separated by spaces, one for each column. A column gets switched iff the corresponding digit is a 1. Example: {' '.join(str(random.randint(0,1)) for _ in range(ENV['n']))}", TAc=TAc, LANG=LANG)
        user_sol.append(user_sol_cols)
    return user_sol


def process_user_sol(ENV, TAc, LANG, raw_sol, sol_style=None, m=None, n=None):
    """From a solution string, parse it and return the solution"""
    sol_style = ENV['sol_style'] if (sol_style == None) else sol_style
    m = ENV['m'] if (m == None) else m
    n = ENV['n'] if (n == None) else n
    assert sol_style != None
    assert m != None
    assert n != None
    try:
        # Parse the raw solution
        return pl.parse_sol(raw_sol, sol_style, m, n)
    except RuntimeError as err:
        err_name = err.args[0]
        # manage custom exceptions:
        if err_name == 'sol-bad-format':
            TAc.print(LANG.render_feedback('sol-bad-format', f"[sol-bad-format]: The solution file have a bad format: {raw_sol}"), "red", ["bold"])
        elif err_name == 'seq-regex':
            TAc.print(LANG.render_feedback('seq-regex', f"[seq-regex]: The solution file have a bad format: {err.args[1]} not match the regex."), "red", ["bold"])
        elif err_name == 'seq-row-m':
            TAc.print(LANG.render_feedback('seq-row-m', f"[seq-row-m]: The solution file have a bad format: the row={err.args[1]} switch exceeds {m}"), "red", ["bold"])
        elif err_name == 'seq-col-n':
            TAc.print(LANG.render_feedback('seq-col-n', f"[seq-col-n]: The solution file have a bad format: the col={err.args[1]} switch exceeds {n}"), "red", ["bold"])
        elif err_name == 'subset-regex':
            TAc.print(LANG.render_feedback('subset-regex', f"[subset-regex]: The solution file have a bad format: {err.args[1]} not match the regex."), "red", ["bold"])
        elif err_name == 'subset-row-m':
            TAc.print(LANG.render_feedback('subset-row-m', f"[subset-row-m]: The solution file have a bad format: the row={err.args[1]} switch exceeds {m}"), "red", ["bold"])
        elif err_name == 'subset-col-n':
            TAc.print(LANG.render_feedback('subset-col-n', f"[subset-col-n]: The solution file have a bad format: the col={err.args[1]} switch exceeds {n}"), "red", ["bold"])
        else:
            TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name}"), "red", ["bold"])
        exit(0)


def print_separator(TAc, LANG):
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])


def check_sol_with_feedback(ENV, TAc, LANG, instance, opt_sol_subset, user_sol, m, n):
    # Init
    opt_sol_seq = pl.subset_to_seq(opt_sol_subset)
    if ENV['sol_style'] == 'seq':
        user_sol_subset = pl.seq_to_subset(user_sol, m, n)
        user_sol_seq = user_sol
    else:
        user_sol_seq = pl.subset_to_seq(user_sol)
        user_sol_subset = user_sol

    # Case1: instance unsolvable
    if opt_sol_subset == pl.NO_SOL:
        if user_sol == pl.NO_SOL:
            TAc.OK()
            TAc.print(LANG.render_feedback('correct-unsolvable', "This instance is not solvable."), "green", ["bold"])
        else:
            TAc.NO()
            TAc.print(LANG.render_feedback('wrong-unsolvable', "This instance is not solvable!"), "red", ["bold"])
        return

    # Case2: user said that a solvable instance is unsolvable
    if user_sol == pl.NO_SOL:
        TAc.NO()
        TAc.print(LANG.render_feedback('wrong-solvable', "This instance is solvable!"), "red", ["bold"])
        return

    # Case3: check if is correct
    is_correct, certificate_of_no = pl.check_sol(instance, user_sol_subset)
    if is_correct:
        TAc.OK()
        TAc.print(LANG.render_feedback('correct', "The solution is correct."), "green", ["bold"])
    else:
        TAc.NO()
        TAc.print(LANG.render_feedback('error', f"The solution is not correct. The pirellone cell in row={certificate_of_no[0]} and col={certificate_of_no[1]} stays on."), "red", ["bold"])
        return

    # Case4: check if is minimal
    if ENV['sol_style'] == 'seq':
        if len(opt_sol_seq) != len(user_sol_seq):
            TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "yellow", ["bold"])
            return
    elif ENV['sol_style'] == 'subset':
        if not pl.is_optimal(user_sol_subset):
            TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "yellow", ["bold"])
            return
    TAc.print(LANG.render_feedback('minimal', "The solution is minimal!"), "green", ["bold"])
