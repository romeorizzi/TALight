#!/usr/bin/env python3

from TALinputs import TALinput
from bot_interface import service_server_requires_and_gets_file

import pirellone_lib as pl


def get_inputs(ENV, TAc, LANG):
    instance = list()
    sol = None

    if ENV['input_mode'] == 'terminal':
        TAc.print(LANG.render_feedback("waiting", f"#? waiting for the pirellone {ENV['m']}x{ENV['n']}.\nFormat: each line is a row of the matrix and each colomun must be separeted by space.\nAny line beggining with the '#' character is ignored.\nIf you prefer, you can use the 'TA_send_txt_file.py' util here to send us the lines of a file. Just plug in the util at the 'rtal connect' command like you do with any other bot and let the util feed in the file for you rather than acting by copy and paste yourself."), "yellow")
        TAc.print(LANG.render_feedback("instance-title", f"Matrix {ENV['m']}x{ENV['n']}:"), "yellow", ["bold"])
        # Get pirellone instance
        for _ in range(ENV['m']):
            instance.append(TALinput(int, num_tokens=ENV['n'], sep=' ', TAc=TAc))
        # Get optimal solution
        sol = pl.get_sol(instance)

    elif ENV['input_mode'] == 'file':
        TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input file (handler `pirellone.txt`)."), "yellow")
        # Get pirellone instance
        instance_str = service_server_requires_and_gets_file('pirellone.txt').decode()
        instance = pl.get_pirellone_from_str(instance_str)
        # Print Pirellone
        TAc.print(LANG.render_feedback("instance-title", f"Matrix {ENV['m']}x{ENV['n']}:"), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("instance", f"{pl.get_str_from_pirellone(instance)}"), "white", ["bold"])
        # Get optimal solution
        sol = pl.get_sol(instance)

    else:
        # Generate pirellone instance
        (instance, seed, switches_row, switches_col) \
            = pl.gen_pirellone(ENV['m'], ENV['n'], ENV['seed'], with_yes_certificate=True)
        # Print Pirellone
        TAc.print(LANG.render_feedback("instance-seed-title", f"Matrix {ENV['m']}x{ENV['n']} (of seed {seed}): "), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("instance", f"{pl.get_str_from_pirellone(instance)}"), "white", ["bold"])
        # Get optimal solution
        sol = pl.get_sol_from(switches_row, switches_col)
        
    return instance, sol