#!/usr/bin/env python3
from sys import stderr, stdout, exit, argv
import os
import ruamel.yaml

usage=f"""
This utility checks that the service synopsis works for every service of a problem. The utility can be asked to check this for every problem in a problem collection.

Usage: argv[0] [ fullname_problem_folder | fullname_problems_collection ]

When no argument is given then it is assumed that the folder is the current one.

When the folder contains a meta.yaml file then it is assumed it is the folder of one problem and that one problem is checked through for any possible service synopsis related inconsistency or fault.

When the folder contains no meta.yaml file then it is assumed that it is a collection of problems (that is, a folder whose subfolders are problems) and then the utility runs its checks for each one of the problems within the folder.  

Assumption:
   rtald is running and serving the problems involved.

Example 1 of use:
    argv[0]

What will happen here:
    if you are in the main folder of a problem (the one containing its meta.yaml file) then the utility will check that one problem. Otherwise, for each direct subfolder of the current folder the utility checks whether it contains a meta.yaml file and, in the positive case, that problem gets checked. 

Example 2 of use:
    argv[0] ~/TALight/example_problems/tutorial/pills
or
    argv[0] ../pills

What will happen here:
    Since pills is one of the problems in our tutorial, we assume that the folder pills contains its meta.yaml file, and the utility checks problem pills.

Example 3 of use:
     argv[0] ~/TALight/example_problems/tutorial
or
     argv[0] ../tutorial

What will happen here:
    All problems in our tutorial will be checked out.
""" 


CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'


def check_one_problem(problem_folder):
    print(f"problem_folder={problem_folder}")
    problem_name=problem_folder.split('/')[-1]
    print(f"problem_name={problem_name}")

    if os.system(f"rtal connect {problem_name} synopsis") != 0:
        return problem_name, False, False, f"Si ottengono errori lanciando il comando:\n   rtal connect {problem_name} synopsis"
    detailed_report = {}

    meta_yaml_file = os.path.join(problem_folder, 'meta.yaml')
    try:
      with open(meta_yaml_file, 'r') as stream:
        try:
            meta_yaml_book = ruamel.yaml.safe_load(stream)
        except:
            for out in [stdout, stderr]:
                print(f'The meta.yaml file \'\'{meta_yaml_file}\'\' could not be loaded as a .yaml file. This is strange because we just got it correcly used here above.', file=out)
            return problem_name, True, False, "Si incontrano problemi nel PARSARE IL FILE meta.yaml"
    
    except IOError as ioe:
        for out in [stdout, stderr]:
            print(f'The meta.yaml file of the problem \'\'{problem_name}\'\' could not be accessed for the required information. The file should have been: \'\'{meta_yaml_file}\'\'. This is strange because we just got it correcly used here above.', file=out)
            print(ioe, file=out)
        return problem_name, True, False, "Si incontrano problemi nell'APRIRE IL FILE meta.yaml"
 
    for service in  meta_yaml_book['services'].keys():
        if os.system(f"rtal connect {problem_name} synopsis -aservice={service}") != 0:
            detailed_report[service] = False
        else:
            detailed_report[service] = True
    
    return problem_name, True, True, detailed_report


if len(argv) > 2:
    print(usage)
    exit(0)

if len(argv) == 1:
    folder_path=os.getcwd()
else:
    folder_path = argv[1]
print(f"folder_path={folder_path}")
if folder_path[-1] in {'/','\\'}:
    folder_path = folder_path[:-1]
reports = []
num_problems = 0
num_wrecked_problems = 0
num_problems_with_wrecked_services = 0
num_TOT_services = 0
num_TOT_wrecked_services = 0
if os.path.isfile(os.path.join(folder_path, 'meta.yaml')):
    reports.append(check_one_problem(problem_folder=folder_path))
else:
    for problem_folder in os.listdir(folder_path):
        problem_folder_fullpath = os.path.join(folder_path, problem_folder)
        if os.path.isdir(problem_folder_fullpath) and os.path.isfile(os.path.join(problem_folder_fullpath, 'meta.yaml')):
            num_problems += 1
            reports.append(check_one_problem(problem_folder=problem_folder_fullpath))
for report in reports:
    problem_name, first_check, early_checks, service_specific_report = report
    print(f"====== REPORT for problem {problem_name}  ======")
    if not first_check:
        num_wrecked_problems += 1
        print(f"{CBOLD}{CRED}NO.{CEND} Already the basic synopsis service for problem {problem_name}  has problems.\n{service_specific_report}")
    elif not early_checks:
        print(f"{CBOLD}{CRED}NO.{CEND} But this is quite strange: the basic synopsis service for problem {problem_name} worked fine but ...\n{service_specific_report}")
    else:
        print(f"{CBOLD}{CGREEN}Ok.{CEND} The basic synopsis service for problem {problem_name} works great!")
        problem_has_got_wrecked_services = False
        for service in service_specific_report.keys():
            num_TOT_services += 1 
            if service_specific_report[service]:
                print(f"{CBOLD}{CGREEN}Ok.{CEND} The synopsis info flows ok for service {service}")
            else:
                print(f"{CBOLD}{CRED}No.{CEND} The synopsis info flow is wrecked for service {service}")
                num_TOT_wrecked_services += 1
                problem_has_got_wrecked_services = True
        if problem_has_got_wrecked_services:
            num_problems_with_wrecked_services += 1
    print("-"*(36+len(problem_name)))

print(f"{CBOLD}=== GROSS SUMMARY ==={CEND}")
print(f"num_problems examined = {num_problems}")
print(f"num_wrecked_problems = {num_wrecked_problems}/{num_problems}")
print(f"num_problems_with_wrecked_services={num_problems_with_wrecked_services}/{num_problems-num_wrecked_problems}")
print(f"num_TOT_services in the {num_problems-num_wrecked_problems} not completely wrecked problems = {num_TOT_services}")
print(f"num_TOT_wrecked_services = {num_TOT_wrecked_services}")
print(f"{CBOLD}---  END  SUMMARY ---{CEND}")

exit(0)



