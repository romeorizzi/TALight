#!/usr/bin/env python3
import subprocess, os, re, random
from sys import exit
from time import monotonic, sleep

from multilanguage import Env, Lang, TALcolors

import pirellone_lib as pl
import model_utils as mu
from utils_lang import printCorrectSolFormat, parse_sol


# METADATA OF THIS TAL_SERVICE:
problem="model_pirellone"
service="try_GMPL_model"
args_list = [
    ('mode',str),
    ('sol_style',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Get input and perform optimal solution with pirellone_lib
try:
    input_str = mu.receive_modelling_files(TAc, LANG)
except RuntimeError as err:
    err_name = err.args[0]
    # manage custom exceptions:
    if err_name == 'read-error':
        TAc.print(LANG.render_feedback('write-error', f"Fail to create {err.args[1]} file"), "red", ["bold"])
instance = pl.get_pirellone_from_str(input_str)
opt_sol = pl.get_opt_sol(instance)
TAc.print(LANG.render_feedback("in-title", "Solution with PirelloneLib: "), "yellow", ["reverse"])
TAc.print(LANG.render_feedback("in-sol", f"{pl.sol_to_str(instance, opt_sol)}"), "green", ["bold"])

# Perform solution with GPLSOL
try:
    mu.run_GPLSOL()
except RuntimeError as err:
    err_name = err.args[0]
    # manage custom exceptions:
    if err_name == 'process-timeout':
        TAc.print(LANG.render_feedback('process-timeout', "Too much computing time! Deadline exceeded."), "red", ["bold"])
    elif err_name == 'process-call':
        TAc.print(LANG.render_feedback('process-call', "The call to glpsol on your .dat file returned error."), "red", ["bold"])
    elif err_name == 'process-exception':
        TAc.print(LANG.render_feedback('process-exception', "Processing returned with error."), "red", ["bold"])
        
# Read GPLSOL solution
if ENV['mode'] == 'create_output':
    try:
        out_sol = parse_sol(mu.get_path_of('out'), ENV['sol_style'], len(opt_sol[0]), len(opt_sol[1]), ENV, TAc, LANG)
        TAc.print(LANG.render_feedback("out-title", "Solution with GPLSOL: "), "yellow", ["reverse"])  
        TAc.print(LANG.render_feedback("out_sol", f"{pl.sol_to_str(instance, opt_sol)}"), "green", ["bold"])
    except RuntimeError as err:
        err_name = err.args[0]
        # manage custom exceptions:
        if err_name == 'read-error':
            TAc.print(LANG.render_feedback('read-error', "Fail to read the output file of GPLSOL"), "red", ["bold"])
        elif err_name == 'output-not-exist':
            TAc.print(LANG.render_feedback('output-not-exist', f"GLPSOL failed to create {mu.OUT_FILENAME} file"), "red", ["bold"])
            printCorrectSolFormat(TAc, LANG)
        elif err_name == 'output-bad-format':
            TAc.print(LANG.render_feedback('output-bad-format', "The output file have a bad format."), "red", ["bold"])
            printCorrectSolFormat(TAc, LANG)
        elif err_name == 'subset-bad-format':
            TAc.print(LANG.render_feedback('subset-bad-format', "The output file have a bad format for subset style."), "red", ["bold"])
            printCorrectSolFormat(TAc, LANG)
        elif err_name == 'seq-bad-format':
            TAc.print(LANG.render_feedback('seq-bad-format', "The output file have a bad format for sequence style."), "red", ["bold"])
            printCorrectSolFormat(TAc, LANG)