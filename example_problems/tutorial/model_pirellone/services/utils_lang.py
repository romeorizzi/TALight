#!/usr/bin/env python3

from TALinputs import TALinput
from bot_interface import service_server_requires_and_gets_the_only_file


import pirellone_lib as pl


def process_inputs(ENV, TAc, LANG):
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
        TAc.print(LANG.render_feedback("instance", f"{pl.get_str_from_pirellone(instance)}"), "white", ["bold"])

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
        TAc.print(LANG.render_feedback("instance", f"{pl.get_str_from_pirellone(instance)}"), "white", ["bold"])
        # Abort if this instance is unsolvable
        if not pl.is_solvable_seed(ENV['seed']):
            TAc.print(LANG.render_feedback("unsolvable-instance", f"The submissive instance is unsolvable. This service manage only solvable seed"), "red", ["bold"])
            exit(0)

    elif ENV['input_mode'] == 'terminal':
        TAc.print(LANG.render_feedback("waiting", f"#? waiting for the pirellone {ENV['m']}x{ENV['n']}.\nFormat: each line is a row of the matrix and each colomun must be separeted by space.\nAny line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself."), "yellow")
        TAc.print(LANG.render_feedback("instance-title", f"Matrix {ENV['m']}x{ENV['n']}:"), "yellow", ["bold"])
        # Get pirellone instance
        for _ in range(ENV['m']):
            instance.append(TALinput(int, num_tokens=ENV['n'], sep=' ', TAc=TAc))
        # Abort if this instance is unsolvable
        if not pl.is_solvable(instance):
            TAc.print(LANG.render_feedback("unsolvable-instance", f"The submissive instance is unsolvable. This service manage only solvable seed"), "red", ["bold"])
            exit(0)

    # elif ENV['input_mode'] == 'TA_transfer_files_bot':
    #     TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input file (handler `pirellone.txt`)."), "yellow")
    #     # get pirellone instance
    #     instance_str = service_server_requires_and_gets_the_only_file().decode()
    #     instance = pl.get_pirellone_from_str(instance_str)
    #     # Get optimal solution
    #     sol = pl.get_sol(instance)

    if ENV['coding']:
        sol_style = ENV['coding']
    else:
        sol_style = 'seq'
    
    if switches_col != None and switches_row != None:
        sol = pl.get_sol_from(switches_row, switches_col, sol_style)
    else:
        sol = pl.get_sol(instance, sol_style)

    return instance, sol