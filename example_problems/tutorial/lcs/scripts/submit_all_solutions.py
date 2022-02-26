#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse

import defaults_general as def_gen
import defaults_problem_specific as def_ps
from utils import * 

PROBLEM_NAME = def_ps.PROBLEM_NAME
SERVER = def_gen.SERVERS_LIST[def_gen.SERVER]
SOL_FORMAT = def_ps.SOL_FORMAT
SOL_EXT = def_ps.AVAILABLE_FORMATS['solution'][SOL_FORMAT]
INST_FORMAT = def_ps.INST_FORMAT
INST_EXT = def_ps.AVAILABLE_FORMATS['instance'][INST_FORMAT]
REL_PATH_SOLUTIONS = def_gen.REL_PATH_SOLUTIONS
REL_PATH_INSTANCES = def_gen.REL_PATH_INSTANCES
REL_PATH_CERTIFICATES = def_gen.REL_PATH_CERTIFICATES
PATH_SOLUTIONS = os.path.join(os.getcwd(),REL_PATH_SOLUTIONS)
PATH_INSTANCES = os.path.join(os.getcwd(),REL_PATH_INSTANCES)
PATH_CERTIFICATES = os.path.join(os.getcwd(),REL_PATH_CERTIFICATES)

usage=f"""\nSono lo script che sottomette tutte le tue soluzioni per il problema '{PROBLEM_NAME}', come contenute nel folder '{PATH_SOLUTIONS}'. Puoi utilizzarmi per validare le tue soluzioni e raccogliere del feedback (sottomissione anonima, per altro sempre consigliata anche prima di procedere con sottomissione con token identificativo) oppure per effettuare una sottomissione con token, nel quale caso ti verrà richiesto di inserire il tuo TALight personal token. Mi concentro sulle sole soluzioni nel formato specificato con l'argomento opzionale --sol_format (default: '{SOL_FORMAT}') tra i seguenti formati consentiti:\n   {list(def_ps.AVAILABLE_FORMATS['solution'].keys())}. Stabilisco il formato di soluzioni ed istanze guardando alle estensioni dei file, assumendo tu abbia utilizzato quelle proposte dal problema ({list(def_ps.AVAILABLE_FORMATS['solution'].items())} per le soluzioni, {list(def_ps.AVAILABLE_FORMATS['instance'].items())} per le istanze). Tuttavia, puoi richiedere di filtrare su altre estensioni (inclusa quella vuota, per noi l'estensione di un filename parte subito a destra del suo primo punto) chiamandomi con le opzioni --sol_ext e --inst_ext. (Dovrai comunque, a maggior ragione, specificare il formato ove differisca da quello di default.)
Il nucleo di un filename è la stringa che inizia subito a destra dell'ultimo carattere '_' (se non presente il nucleo è un prefisso) e termina subito prima del primo carattere '.'. Il mio compito è inviare al servizio `rtal connect {PROBLEM_NAME} check_sol` ogni file contenuto nel folder '{PATH_SOLUTIONS}' e con la giusta estensione, però anche accoppiato con le istanze che gli corrispondono. Nel caso di una sottomissione con token, invio al servizio `rtal connect {PROBLEM_NAME}` solo quei file il nucleo dei cui filenames rispetta la regex [0-9][0-9][0-9] a codifica in rappresentazione decimale di un numero naturale positivo n nell'intervallo [1,999], assumendo esso contenga una soluzione in formato '{SOL_FORMAT}' per l'istanza n della collection (ossia quella con instance_id=n). Posso procedere in questo pratico modo anche qualora tu non intenda utilizzare il token per ottenere una registrazione sul server, qualora tu voglia comunque riferire le tue soluzioni alle istanze nella collection. Se tuttavia tu intendi riferire le tue soluzioni ad altre istanze, magari da tè prodotte, esse dovranno trovarsi entro la cartella '{PATH_INSTANCES}', corrispondere nel formato, ed io manderò in valutazione quelle sole coppie (istanza,soluzione) fitrate come detto sopra e dove i filename abbiano medesimo nucleo. Nel caso di sottomissioni con token mi occupo anche di salvare nel folder '{PATH_CERTIFICATES}' i certificati di avvenuta sottomissione.
Ti converrà lanciarmi da dove mi troverai collocato, una volta decompresso l'archivio '{PROBLEM_NAME}.tar' che potrai scaricarti in locale col comando `rtal get {PROBLEM_NAME}`. Puoi regolare il mio comportamento alle tue consuetudini modificando i valori di default contenuti nei file `defaults_general.py` e `defaults_problem_specific.py` oppure, di volta in volta, valorizzando le opzioni consentite dalla sintassi per la riga di comando:

Usage: {os.path.basename(sys.argv[0])}  {{ JUST_GET_FEEDBACK | SUBMIT }}  {{ MY_INSTANCES | CATALOGUE_INSTANCES }} [--sol_format] [--inst_format] [--sol_ext] [--inst_ext] [--sol_folder] [--inst_folder]

   where the two alternative options for the 'mode' argument are:
   * SUBMIT: act a real sumbission! In this case you will be required to introduce your personal token.
   * JUST_GET_FEEDBACK [default]: when your intantion is only to get a feedback or validation on your solutions. For this you do not need to be enrolled in the course or exam.

   the three alternative options for the 'mode_feedback' argument are:
   * MY_INSTANCES [default]: to get feedback on your own instances and solutions. In this case the names of the instance_files and solution_files have to match (i.e., have the same kernel).
   * CATALOGUE_INSTANCES: when your intention is only to get a feedback or validation of your solutions to the instances in the catalogue. In this case only the solutions whose filename's kernel is a correct instance_id will be sent for evaluation being matched on the instances on the server.

Roughly speaking, this script will issue an rtal check_sol service request for every solution file in your local {PATH_SOLUTIONS} folder whose filename's kernel is the decimal representation of a number that could be the instance_id of an instance in the catalogue stored on the server.
However, when you are not submitting your solutions but only asking the service to check them and provide you with a feedback, then you can use instances which do not correspond to the instances on the catalogue. In this case, the script can be asked to issue an rtal check_sol service request for every (instance_file,solution_file) pair of files whose names match, with instance_file in your local {PATH_INSTANCES} folder and solution_file in your local {PATH_SOLUTIONS} folder. In this case, the file names are not required to contain the decimal representation of a number. Two filenames match when they have the same kernel.

HINT 1: in conclusion, the suggestion is to pay attention to place every solution in a file whose basename matches the basename of the file containing the instance. The rule for what matches is that, if the name of the instance is one of the following: 
   instance_026.with_m_and_n.txt
   instance_026.only_strings.txt
   instance_026.my_own.long.extension
then it matches any one of the following:
   sol_026.with_m_and_n.subseq.txt
   solution_026.with_m_and_n.subseq.txt
   my_sol_026.with_m_and_n.annotated_subseq.txt
   my_own_sol_026.my_own.long.extension
More in general, we seek identity of the kernel, i.e., the substring of the filename that ends at the first dot (if any) and begins at the first underscore (if any).
Hence, matching is an equivalence relation and all of the following would match:
   micky_mouse, mouse, 123_mouse.my_own.long.extension

HINT 2: both for instances and for solutions I would suggest to stick with the default extensions.

NOTE: the ext and kernel functions defined in the utils.py file specify the bare details of the notion of match and what gets filtered.

"""


if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=usage,
    epilog="""-------------------""")
    parser.add_argument('mode', type=str, choices=['JUST_GET_FEEDBACK', 'SUBMIT'], help='choose one option in the set { JUST_GET_FEEDBACK | SUBMIT }. In order to submit you are also asked to supply your personal TALight token', default='JUST_GET_FEEDBACK')
    parser.add_argument('mode_feedback', type=str, choices=['MY_INSTANCES', 'CATALOGUE_INSTANCES'], help='choose one option in the set { MY_INSTANCES | CATALOGUE_INSTANCES }. When you are submitting then this option is forcibly set to CATALOGUE_INSTANCES hence twikering this argument is useless. Otherwise, setting this option to MY_INSTANCES (which is also the default value) will refer your solutions to the instances contained into your local {PATH_INSTANCES} folder. This script will then issue an rtal check_sol service request for every (instance_file,solution_file) pair of files whose names match, with instance_file in your local {PATH_INSTANCES} folder and solution_file in your local {PATH_SOLUTIONS} folder.', default='MY_INSTANCES')
    parser.add_argument('--sol_folder', type=str, help=f'use this optional argument to specify a different name/location for the folder containing the files with your solutions (the default is {PATH_SOLUTIONS}).', default=PATH_SOLUTIONS)
    parser.add_argument('--inst_folder', type=str, help=f'use this optional argument to specify a different name/location for the folder containing the files with your instances (the default is {PATH_INSTANCES}).', default=PATH_INSTANCES)
    parser.add_argument('--sol_format', type=str, help=f'use this optional argument to specify the intended format of your solutions (the default is {SOL_FORMAT}).')
    parser.add_argument('--inst_format', type=str, help=f'use this optional argument to specify the intended format of your instances (the default is {INST_FORMAT}).')
    parser.add_argument('--sol_ext', type=str, help=f'use this optional argument to specify the extension that you accept for the files containing solutions. All other files in the folder with the solutions will be ignored (filtered away). If you omit this argument then the accepted extension is the standard one for the solution format used.')
    parser.add_argument('--inst_ext', type=str, help=f'use this optional argument to specify the extension that you accept for the files containing instances. All other files in the folder with the instances will be ignored (filtered away). If you omit this argument then the accepted extension is the standard one for the instance format used.')

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

    if not os.path.exists(args.sol_folder):    
        print(f"{CRED}ERROR{CEND}: the folder with your stored solution does not exist.\nMissing folder:\n     {args.sol_folder}\nCreate it and fill it up properly, then you can start me again.")
        exit(1)

    if args.mode == 'JUST_GET_FEEDBACK' and args.mode_feedback == 'MY_INSTANCES':
        list_solutions = [ f for f in os.listdir(PATH_SOLUTION) if ext(f) == SOL_EXT ]
    else:
        list_solutions = [ f for f in os.listdir(PATH_SOLUTION) if ext(f) == SOL_EXT and is_instance_id(kernel(f)) ]
    #print(f"{list_solutions}")

    list_instances = None
    if args.mode == 'JUST_GET_FEEDBACK' and args.mode_feedback == 'MY_INSTANCES': 
        if not os.path.exists(args.inst_folder):    
            print(f"{CRED}ERROR{CEND}: the folder with your stored instances does not exist.\nMissing folder:\n     {args.inst_folder}\nCreate it and fill it up properly, then you can start me again.")
            exit(1)
        list_instances = [ f for f in os.listdir(args.inst_folder) if ext(f) == INST_EXT]
        #print(f"{list_instances}")
    
    def command_submission(solution_file, instance_id):
        return f"rtal connect {PROBLEM_NAME} -x {{PERSONAL_TOKEN}} -o {PATH_CERTIFICATES} check_sol -fsolution={os.path.join(args.sol_folder),solution_file} -asol_format={SOL_FORMAT} -ainstance_id={instance_id}"
        
    def command_feedback_catalogue(solution_file, instance_id):
        return f"rtal connect {PROBLEM_NAME}  check_sol -fsolution={os.path.join(args.sol_folder),solution_file} -asol_format={SOL_FORMAT} -ainstance_id={instance_id}"
        
    def command_feedback_catalogue(solution_file, instance_file):
        return f"rtal connect {PROBLEM_NAME} -fsolution={os.path.join(args.sol_folder),solution_file} -asol_format={SOL_FORMAT} -finstance={os.path.join(args.inst_folder),instance_file} -ainstance_format={INST_FORMAT}"

    calls_list = []
    for solution_file in list_solutions:
        if args.mode == 'SUBMIT':
            instance_id = int(kernel(solution_file))
            calls_list.append(command_submission(solution_file, instance_id))
        elif args.mode_feedback == 'CATALOGUE_INSTANCES':
            instance_id = int(kernel(solution_file))
            calls_list.append(command_submission(solution_file, instance_id, PERSONAL_TOKEN))
        else:
            for instance_file in list_instances:
                if kernel(instance_file) == kernel(solution_file)
                calls_list.append(command_feedback_catalogue(solution_file, instance_file))


    def go_through_calls(calls_list, dry_run, PERSONAL_TOKEN, PERSONAL_TOKEN_FOR_DISPLAY):
        for command,i in zip(calls_list,range(len(calls_list))):
            command_for_display = command.format({'PERSONAL_TOKEN': PERSONAL_TOKEN_FOR_DISPLAY})
            if dry_run:
                print(f"\n {str(i+1).zfill(3)}. {command_for_display}")
            else:
: PERSONAL_TOKEN})
                print(f"\n\n{CRED}I am going to make the following service call:\n    {CGREEN}{command_for_display}{CEND}")
                confirm_to_continue(allow_skip_all = True)
                command_for_execution = command.format({'PERSONAL_TOKEN': PERSONAL_TOKEN})
                os.system(command_for_execution)
        
    print(f"\n{CBOLD}QUADRO DELLE NOSTRE RICHIESTE AL SERVIZIO `rtal connect {PROBLEM_NAME} check_sol`:{CEND}\n")
    go_through_calls(calls_list, dry_run=True, PERSONAL_TOKEN=None, PERSONAL_TOKEN_FOR_DISPLAY='<PERSONAL_TOKEN_NEEDED>')
    if args.mode != 'SUBMIT':
        confirm_to_continue(allow_skip_all = False)
    else:
        YOUR_PERSONAL_TOKEN=input("Trattandosi di sottomissioni, se vuoi procedere devi inserire il tuo TALight personal token")
        YOUR_PERSONAL_TOKEN=input("Your TALight personal token:")
        print(f"Hai inserito {YOUR_PERSONAL_TOKEN=}")
        confirm_to_continue(allow_skip_all = False)
    go_through_calls(calls_list, dry_run=False, PERSONAL_TOKEN=YOUR_PERSONAL_TOKEN, PERSONAL_TOKEN_FOR_DISPLAY='<YOUR_PERSONAL_TOKEN>')

