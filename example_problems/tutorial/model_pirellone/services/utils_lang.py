#!/usr/bin/env python3
"""This file contains the useful functions used in more services of the 'Pirellone' problem."""
import os, re

from TALinputs import TALinput
from bot_interface import service_server_requires_and_gets_the_only_file

import pirellone_lib as pl


def process_instance(ENV, TAc, LANG):
    instance = list()
    sol = None
    switches_col = None
    switches_row = None

    if ENV['input_mode'] == 'random':
        # Get random seed
        seed = pl.gen_pirellone_seed(solvable=True)
        # Get instance
        try:
            (instance, switches_row, switches_col) \
                 = pl.gen_pirellone(ENV['m'], ENV['n'], seed, with_yes_certificate=True)
        except RuntimeError:
            TAc.print(LANG.render_feedback("error", f"Can't generate an unsolvable matrix {ENV['m']}x{ENV['n']}."), "red", ["bold"])
            exit(0)
        TAc.print(LANG.render_feedback("seed", f"The seed is: {seed}"), "yellow", ["bold"])
        # Print instance
        TAc.print(LANG.render_feedback("instance-title", f"The matrix {ENV['m']}x{ENV['n']} is:"), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("instance", f"{pl.pirellone_to_str(instance)}"), "white", ["bold"])

    elif ENV['input_mode'] == 'seed':
        if ENV['seed'] == 0:
            TAc.print(LANG.render_feedback("no-mandatory-seed", f"If you select (input_mode='seed') then the (seed) argument must be differente from 000000"), "red", ["bold"])
            exit(0)
        # Get instance
        try:
            (instance, switches_row, switches_col) \
                 = pl.gen_pirellone(ENV['m'], ENV['n'], ENV['seed'], with_yes_certificate=True)
        except RuntimeError:
            TAc.print(LANG.render_feedback("error", f"Can't generate an unsolvable matrix {ENV['m']}x{ENV['n']}."), "red", ["bold"])
            exit(0)
        # Print instance
        TAc.print(LANG.render_feedback("instance-title", f"The matrix {ENV['m']}x{ENV['n']} is:"), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("instance", f"{pl.pirellone_to_str(instance)}"), "white", ["bold"])
        # Abort if this instance is unsolvable
        if not pl.is_solvable_seed(ENV['seed']):
            TAc.print(LANG.render_feedback("unsolvable-instance", f"The submissive instance is unsolvable. This service manage only solvable seed."), "red", ["bold"])
            exit(0)

    elif ENV['input_mode'] == 'terminal':
        TAc.print(LANG.render_feedback("waiting", f"#? waiting for the pirellone {ENV['m']}x{ENV['n']}.\nFormat: each line is a row of the matrix and each colomun must be separeted by space.\nAny line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself."), "yellow")
        TAc.print(LANG.render_feedback("instance-title", f"Matrix {ENV['m']}x{ENV['n']}:"), "yellow", ["bold"])
        # Get pirellone instance
        for _ in range(ENV['m']):
            instance.append(TALinput(int, num_tokens=ENV['n'], sep=' ', TAc=TAc))
        # Abort if this instance is unsolvable
        if not pl.is_solvable(instance):
            TAc.print(LANG.render_feedback("unsolvable-instance", f"The submissive instance is unsolvable. This service manage only solvable seed."), "red", ["bold"])
            exit(0)

    # elif ENV['input_mode'] == 'TA_transfer_files_bot':
    #     TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input file (handler `pirellone.txt`)."), "yellow")
    #     # get pirellone instance
    #     instance_str = service_server_requires_and_gets_the_only_file().decode()
    #     instance = pl.get_pirellone_from_str(instance_str)
    #     # Get optimal solution
    #     sol = pl.get_opt_sol(instance)
    
    
    if switches_col != None and switches_row != None:
        sol = pl.get_opt_sol_from(switches_row, switches_col)
    else:
        sol = pl.get_opt_sol(instance)

    return instance, sol


def process_user_seq_sol(ENV, TAc, LANG, user_inputs):
    # Adjust solution to mange the case 'zero moves'
    if user_inputs == ['']:
        user_inputs.clear()
        return
    # Check the m,n ranges
    for command in user_inputs:
        if command[0] == 'r':
            if int(command[1:]) > ENV['m']:
                TAc.print(LANG.render_feedback("row-index-exceeds-m", f"# Error! In your solution the move ({command}) is not applicable. Indeed: {command[1:]} > {ENV['m']}."), "red", ["bold"])
                exit(0)
        else:
            if int(command[1:]) > ENV['n']:
                TAc.print(LANG.render_feedback("col-index-exceeds-m", f"# Error! In your solution the move ({command}) is not applicable. Indeed: {command[1:]} > {ENV['m']}."), "red", ["bold"])
                exit(0)


def printCorrectSolFormat(TAc, LANG):
    TAc.print(LANG.render_feedback('print-correct-sol-format', \
        """If you want to get your model validated, then from your .mod file you should create a file named 'output.txt' containing the final solution for your instance. Namely, if the puzzle has no solution, then the file named 'output.txt' should contain the string "NO SOLUTION". Nel caso in cui non sia possibile spegnere tutte le luci del Pirellone
        con gli interruttori speciali, il file `output.txt` offre la stringa "NO SOLUTIONS". Altrimenti, il file `output.txt` deve contenere due linee per indicare
        su quali interruttori deve agire il custode.

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
        oppure no."""), "yellow", ["bold"])


# TODO: improve it
def parse_sol(sol_path, sol_style, m, n, ENV, TAc, LANG):
    """Read file, parse it and returns the solution in sol_style."""
    if not os.path.exists(sol_path):
        raise RuntimeError('output-not-exist')
    try:
        with open(sol_path, 'r') as file:
            lines = file.readlines()
            if len(lines) > 2 or \
               (len(lines) == 1 and lines[0] != pl.NO_SOL) or \
               (len(lines) == 1 and sol_style == 'subset') or \
               (len(lines) == 2 and sol_style == 'seq'):
                raise RuntimeError('output-bad-format')
            user_sol = list()
            if sol_style=="subset":
                if (any(not re.match(f"^(0|1){{{m}}}$", e) for e in lines[0]) or \
                    any(not re.match(f"^(0|1){{{m}}}$", e) for e in lines[1])):
                    raise RuntimeError('subset-bad-format')
                user_sol.append([int(e) for e in lines[0].split()])
                user_sol.append([int(e) for e in lines[1].split()])
            else:
                if not re.match("^(|(r|R|c|C)[1-9][0-9]*)$", lines[0]):
                    raise RuntimeError('seq-bad-format')
                user_sol = lines[0].split()
                process_user_seq_sol(ENV, TAc, LANG, user_sol)
    except os.error as e:
        raise RuntimeError('read-error', e)
    except (IndexError, ValueError) as e:
        raise RuntimeError('output-bad-format')

