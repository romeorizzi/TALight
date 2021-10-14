#!/usr/bin/env python3
"""This file contains the useful functions used in more services of the 'Pirellone' problem."""
from TALinputs import TALinput
from bot_interface import service_server_requires_and_gets_the_only_file

import pirellone_lib as pl


def process_instance(ENV, TAc, LANG):
    if ENV['input_mode'] == 'random':
        # Get random seed
        seed = pl.gen_pirellone_seed()
        # Get instance
        try:
            instance, certificate= pl.gen_pirellone(ENV['m'], ENV['n'], seed, with_yes_certificate=True)
        except RuntimeError:
            TAc.print(LANG.render_feedback("error", f"Can't generate an unsolvable matrix {ENV['m']}x{ENV['n']}."), "red", ["bold"])
            exit(0)
        TAc.print(LANG.render_feedback("seed", f"The seed is: {seed}"), "yellow", ["bold"])
        # Print instance
        TAc.print(LANG.render_feedback("instance-title", f"The matrix {ENV['m']}x{ENV['n']} is:"), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("instance", f"{pl.pirellone_to_str(instance)}"), "white", ["bold"])
        # Returns instance and optimal solution
        return instance, pl.make_optimal(certificate) if pl.is_solvable_seed(seed) else pl.NO_SOL

    elif ENV['input_mode'] == 'seed':
        if ENV['seed'] == 0:
            TAc.print(LANG.render_feedback("no-mandatory-seed", f"If you select (input_mode='seed') then the (seed) argument must be differente from 000000"), "red", ["bold"])
            exit(0)
        # Get instance
        try:
            instance, certificate = pl.gen_pirellone(ENV['m'], ENV['n'], ENV['seed'], with_yes_certificate=True)
        except RuntimeError:
            TAc.print(LANG.render_feedback("error", f"Can't generate an unsolvable matrix {ENV['m']}x{ENV['n']}."), "red", ["bold"])
            exit(0)
        # Print instance
        TAc.print(LANG.render_feedback("instance-title", f"The matrix {ENV['m']}x{ENV['n']} is:"), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("instance", f"{pl.pirellone_to_str(instance)}"), "white", ["bold"])
        # Returns instance and optimal solution
        return instance, pl.make_optimal(certificate) if pl.is_solvable_seed(ENV['seed']) else pl.NO_SOL


    elif ENV['input_mode'] == 'terminal':
        TAc.print(LANG.render_feedback("waiting", f"#? waiting for the pirellone {ENV['m']}x{ENV['n']}.\nFormat: each line is a row of the matrix and each colomun must be separeted by space.\nAny line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the raw_sol of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself."), "yellow")
        TAc.print(LANG.render_feedback("instance-title", f"Matrix {ENV['m']}x{ENV['n']}:"), "yellow", ["bold"])
        # Get pirellone instance
        instance = list()
        for _ in range(ENV['m']):
            instance.append(TALinput(int, num_tokens=ENV['n'], sep=' ', TAc=TAc))
        # Returns instance and optimal solution
        return instance, pl.get_opt_sol(instance)

    # elif ENV['input_mode'] == 'TA_transfer_files_bot':
    #     TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input file (handler `pirellone.txt`)."), "yellow")
    #     # get pirellone instance
    #     instance_str = service_server_requires_and_gets_the_only_file().decode()
    #     instance = pl.get_pirellone_from_str(instance_str)
    #     # Get optimal solution
    #     sol = pl.get_opt_sol(instance)
    

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
            TAc.print(LANG.render_feedback('sol-bad-format', f"The solution file have a bad format: {raw_sol}"), "red", ["bold"])
            print_correct_sol_format(TAc, LANG)
        elif err_name == 'seq-regex':
            TAc.print(LANG.render_feedback('sol-bad-format', f"The solution file have a bad format: {err.args[1]} not match the regex."), "red", ["bold"])
            print_correct_sol_format(TAc, LANG)
        elif err_name == 'seq-row-m':
            TAc.print(LANG.render_feedback('sol-bad-format', f"The solution file have a bad format: the row={err.args[1]} switch exceeds {m}"), "red", ["bold"])
            print_correct_sol_format(TAc, LANG)
        elif err_name == 'seq-col-n':
            TAc.print(LANG.render_feedback('sol-bad-format', f"The solution file have a bad format: the col={err.args[1]} switch exceeds {n}"), "red", ["bold"])
            print_correct_sol_format(TAc, LANG)
        elif err_name == 'subset-regex':
            TAc.print(LANG.render_feedback('sol-bad-format', f"The solution file have a bad format: {err.args[1]} not match the regex."), "red", ["bold"])
            print_correct_sol_format(TAc, LANG)
        elif err_name == 'subset-row-m':
            TAc.print(LANG.render_feedback('sol-bad-format', f"The solution file have a bad format: the row={err.args[1]} switch exceeds {m}"), "red", ["bold"])
            print_correct_sol_format(TAc, LANG)
        elif err_name == 'subset-col-n':
            TAc.print(LANG.render_feedback('sol-bad-format', f"The solution file have a bad format: the col={err.args[1]} switch exceeds {n}"), "red", ["bold"])
            print_correct_sol_format(TAc, LANG)
        else:
            TAc.print(LANG.render_feedback('unknown-error', f"Unknown error: {err_name}"), "red", ["bold"])
        exit(0)


def print_correct_sol_format(TAc, LANG):
    """Print how to format the solution"""
    TAc.print(LANG.render_feedback('print-correct-sol-format', \
        """        If you want to get your model validated, then from your .mod file
        you should create a file named 'output.txt' containing the final
        solution for your instance. Namely, if the puzzle has no solution,
        then the file named 'output.txt' should contain the string 
        "NO SOLUTION". Nel caso in cui non sia possibile spegnere tutte le
        luci del Pirellone con gli interruttori speciali, il file `output.txt`
        offre la stringa "NO SOLUTIONS". Altrimenti, il file `output.txt` 
        deve contenere due linee per indicare su quali interruttori deve 
        agire il custode.

        La prima linea contiene una sequenza di $M$ valori ($0$ oppure
        $1$) separati da uno spazio.
        L'$i$-esimo valore della sequenza indica se il custode deve
        agire sull'interruttore dell'$i$-esima riga (valore = $1$)
        oppure no (valore = $0$).

        Analogamente, la seconda linea contiene una sequenza di $N$
        valori ($0$ oppure $1$) separati da uno spazio, per rappresentare le
        operazioni che il custode deve effettuare sugli interruttori di
        colonna.  Il $j$-esimo valore della sequenza indica se il
        custode deve agire sull'interruttore della $j$-esima colonna
        oppure no.""" \
    ), "yellow", ["bold"])


def print_separator(TAc, LANG):
    """Print a separator string"""
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])


def check_sol_with_feedback(ENV, TAc, LANG, instance, opt_sol_subset, user_sol):
    # Init
    if ENV['sol_style'] == 'seq':
        opt_sol_seq = pl.subset_to_seq(opt_sol_subset)

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

    # Case3: equals solutions
    if user_sol == (opt_sol_seq if ENV['sol_style'] == 'seq' else opt_sol_subset):
        TAc.OK()
        TAc.print(LANG.render_feedback('correct-optimal', "The solution is correct and optimal."), "green", ["bold"])
        return

    # Case4: check if is minimal
    if ENV['sol_style'] == 'seq':
        if len(user_sol) != len(opt_sol_seq):
            TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "yellow", ["bold"])
        # Ok now is better use subset style for check the solution
        user_sol = pl.seq_to_subset(user_sol, ENV['m'], ENV['n'])
    else:
        if not pl.is_optimal(user_sol):
            TAc.print(LANG.render_feedback('not-minimal', "This sequence is not minimal."), "yellow", ["bold"])

    # Case5: check if is correct
    is_correct, certificate_of_no = pl.check_sol(instance, user_sol)
    if is_correct:
        TAc.OK()
        TAc.print(LANG.render_feedback('correct', "The solution is correct."), "green", ["bold"])
        return
    else:
        TAc.NO()
        TAc.print(LANG.render_feedback('error', f"The solution is not correct. The pirellone cell in row={certificate_of_no[0]} and col={certificate_of_no[1]} stays on."), "red", ["bold"])
        return