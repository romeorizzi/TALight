#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse

import defaults_general as def_gen
import defaults_problem_specific as def_ps
from utils import * 

PROBLEM_NAME = def_ps.PROBLEM_NAME
YOUR_SOLVER_EXECUTABLE_COMMAND=def_ps.YOUR_SOLVER_EXECUTABLE_COMMAND
SOL_FORMAT = def_ps.SOL_FORMAT
SOL_EXT = def_ps.AVAILABLE_FORMATS['solution'][SOL_FORMAT]
INST_FORMAT = def_ps.INST_FORMAT
INST_EXT = def_ps.AVAILABLE_FORMATS['instance'][INST_FORMAT]
REL_PATH_SOLUTIONS = def_gen.REL_PATH_SOLUTIONS
REL_PATH_INSTANCES = def_gen.REL_PATH_INSTANCES
PATH_SOLUTIONS = os.path.join(os.getcwd(),REL_PATH_SOLUTIONS)
PATH_INSTANCES = os.path.join(os.getcwd(),REL_PATH_INSTANCES)
SOL_FILE_PREFIX = def_gen.SOL_FILE_PREFIX

usage=f"""\nSono lo script che impiega un programma risolutore da tè realizzato, che sà risolvere una singola istanza del problema in esame, per produrre le tue soluzioni per tutte le istanze contenute in un folder da tè indicato (di default, il folder '{PATH_INSTANCES}') e le colloca nel folder da tè indicato (di default, il folder '{PATH_SOLUTIONS}'). Mi concentro sulle sole istanze nel formato specificato con l'argomento opzionale --inst_format (default: '{INST_FORMAT}') tra i seguenti formati consentiti:\n   {list(def_ps.AVAILABLE_FORMATS['instance'].keys())}. Stabilisco il formato di istanze e soluzioni guardando alle estensioni dei file, assumendo tu abbia utilizzato quelle proposte dal problema ({list(def_ps.AVAILABLE_FORMATS['instance'].items())} per le istanze), {def_ps.AVAILABLE_FORMATS['solution'].items()} per le soluzioni. Tuttavia, puoi richiedere di filtrare su altre estensioni (inclusa quella vuota, per noi l'estensione di un filename parte subito a destra del suo primo punto) chiamandomi con le opzioni --sol_ext e --inst_ext. (Dovrai comunque, a maggior ragione, specificare il formato ove differisca da quello di default.)
Il nucleo di un filename è la stringa che inizia subito a destra dell'ultimo carattere '_' (se non presente il nucleo è un prefisso) e termina subito prima del primo carattere '.'. Il file che conterrà la soluzione avrà per nome il nucleo del file d'istanza per la quale la soluzione è stata prodotta, mentre l'estensione sarà quella del formato scelto per la soluzione oppure quella eventualmente specificata con l'opzione --sol_ext.
Ti converrà lanciarmi da dove mi troverai collocato, una volta decompresso l'archivio '{PROBLEM_NAME}.tar' che potrai scaricarti in locale col comando `rtal get {PROBLEM_NAME}`. Puoi regolare il mio comportamento alle tue consuetudini modificando i valori di default contenuti nei file `defaults_general.py` e `defaults_problem_specific.py` oppure, di volta in volta, valorizzando le opzioni consentite dalla sintassi per la riga di comando.

It is assumed that your solver program reads instances from stdin and writes solutions on stdout. 
Roughly speaking, this script will run your solver program on every instance file in your local {PATH_INSTANCES} folder whose extension is the one you have directly (via the --inst_ext argument) or indirectly (via the --inst_format argument, or otherwise just its default value) specified, and will put the solution obtained in a file placed in your local {PATH_SOLUTIONS} folder. The extension can be specified either via the instance format (default value of the --sol_format argument is {SOL_FORMAT}) or the --sol_ext argument. The name of this file will be the kernel of the name of the file with the instance prefixed with the string `{SOL_FILE_PREFIX}`. You can change this prefix via the --sol_file_prefix argument.

NOTE: the ext and kernel functions defined in the utils.py file specify the bare details of the notions of kernel and long extensions. The kernel is the part of the filename that is maintained from the instance to the solution.

ADVICE: both for instances and for solutions I would suggest to stick with the default extensions.

"""


if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=usage,
    epilog="""-------------------""")
    parser.add_argument('--your_solver', type=str, help=f"use this optional argument to specify the executable command that launches your solver. It could be something like 'phython my_solver.py' or '{YOUR_SOLVER_EXECUTABLE_COMMAND}'.", default=YOUR_SOLVER_EXECUTABLE_COMMAND)
    parser.add_argument('--sol_folder', type=str, help=f'use this optional argument to specify a different name/location for the folder containing the files with your solutions (the default is {PATH_SOLUTIONS}.', default=PATH_SOLUTIONS)
    parser.add_argument('--inst_folder', type=str, help=f'use this optional argument to specify a different name/location for the folder containing the files with your instances (the default is {PATH_INSTANCES}.', default=PATH_INSTANCES)
    parser.add_argument('--sol_format', type=str, help=f'use this optional argument to specify the intended format of your solutions (the default is {SOL_FORMAT}).')
    parser.add_argument('--inst_format', type=str, help=f'use this optional argument to specify the intended format of your instances (the default is {INST_FORMAT}).')
    parser.add_argument('--sol_ext', type=str, help=f'use this optional argument to specify the extension to be given to the generated files containing the solutions. If you omit this argument then the accepted extension is the standard one for the solution format used.')
    parser.add_argument('--inst_ext', type=str, help=f'use this optional argument to specify the extension that you accept for the files containing instances. All other files in the folder with the instances will be ignored (filtered away). If you omit this argument then the accepted extension is the standard one for the instance format used.')
    parser.add_argument('--sol_file_prefix', type=str, help=f'use this optional argument to specify the prefix of the names of generated files containing the solutions.', default=SOL_FILE_PREFIX)

    args = parser.parse_args()

    if args.sol_format:
        SOL_FORMAT=args.sol_format
        SOL_EXT = def_ps.AVAILABLE_FORMATS['solution'][SOL_FORMAT]
    if args.inst_format:
        INST_FORMAT=args.inst_format
        INST_EXT = def_ps.AVAILABLE_FORMATS['instance'][INST_FORMAT]
    if args.sol_ext:
        SOL_EXT = args.sol_ext
    if args.inst_ext:
        INST_EXT = args.inst_ext

    if not os.path.exists(args.inst_folder):    
        print(f"{CRED}ERROR{CEND}: the folder with your stored instances does not exist.\nMissing folder:\n     {args.inst_folder}\nCreate it and fill it up properly, then you can start me again.")
        exit(1)
    list_instances = [ f for f in os.listdir(args.inst_folder) if ext(f) == INST_EXT]
    #print(f"{list_instances=}")
        
    if not os.path.exists(args.sol_folder):    
        print(f"{CRED}ERROR{CEND}: the folder with your stored solution does not exist.\nMissing folder:\n     {args.sol_folder}\nCreate it, then you can start me again.")
        exit(1)

        
    commands_list = []
    for instance_file in list_instances:
        solution_file = args.sol_file_prefix + kernel(instance_file) +'.'+SOL_EXT
        commands_list.append(f"{args.your_solver} < {os.path.join(args.inst_folder,instance_file)} > {os.path.join(args.sol_folder,solution_file)}")

    def go_through_commands(commands_list, dry_run):
        for command,i in zip(commands_list,range(len(commands_list))):
            if dry_run:
                print(f"\n {str(i+1).zfill(3)}. {command}")
            else:
                print(f"\n\n{CRED}I am going to run the following command:\n    {CGREEN}{command}{CEND}")
                confirm_to_continue(allow_skip_all = True)
                os.system(command)
        
    print(f"\n{CBOLD}LISTA DEI {len(commands_list)} COMANDI CHE INTENDIAMO LANCIARE PER RISOLVERE {len(commands_list)} ISTANZE E GENERARE I RELATIVI FILE DI SOLUZIONE:{CEND}\n")
    go_through_commands(commands_list, dry_run=True)
    print(f"\n{CBOLD}PRESO VISIONE DELLA LISTA DI {len(commands_list)} COMANDI CHE ESEGUIREMO PER GENERARE {len(commands_list)} SOLUZIONI?{CEND}\n")
    confirm_to_continue(allow_skip_all = False)
    go_through_commands(commands_list, dry_run=False)

