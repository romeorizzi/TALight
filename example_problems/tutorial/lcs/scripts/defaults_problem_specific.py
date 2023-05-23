#!/usr/bin/env python3
import os

PROBLEM_NAME = 'lcs'
# FORMATS:
SOL_FORMAT = 'annotated_subseq'
#SOL_FORMAT = 'subseq'
INST_FORMAT = 'only_strings'
#INST_FORMAT = 'with_m_and_n'
AVAILABLE_FORMATS = {'instance':{'only_strings':'only_strings.txt', 'with_m_and_n':'with_m_and_n.txt', 'gmpl_dat1':'dat'},'solution':{'subseq':'subseq.txt', 'annotated_subseq':'annotated_subseq.txt'}}

# YOUR_SOLVER:
YOUR_SOLVER_EXECUTABLE_COMMAND=f"python {os.path.join('..','sol','my_solver.py')}"
#YOUR_SOLVER_EXECUTABLE_COMMAND=f"python {os.path.join('..','sol','my_solver.py')} --sol_format subseq"
#YOUR_SOLVER_EXECUTABLE_COMMAND=f"python {os.path.join('..','sol','my_solver.py')} --inst_format with_m_and_n"
#YOUR_SOLVER_EXECUTABLE_COMMAND=f"python {os.path.join('..','sol','my_solver.py')} --inst_format with_m_and_n --sol_format subseq"
