#!/usr/bin/env python3
import os
import sys
import random
import math
from datetime import datetime

from termcolor import colored
from contextlib import redirect_stdout
from sys import setrecursionlimit

setrecursionlimit(10**8)

AVAILABLE_FORMATS = {'instance':{'simple':'simple.txt', 'with_len':'with_len.txt', 'collage_dat':'collage.dat'},'solution':{'all_solutions': 'all_solutions.txt'}}
DEFAULT_INSTANCE_FORMAT='with_len'
DEFAULT_SOLUTION_FORMAT='all_solutions'

MAX_NUM_COL = 256
NMAX=1000

seq=[]
memo = [[0 for __ in range(NMAX)] for _ in range(NMAX)]

def format_name_to_file_extension(format_name, format_gender):
    assert format_gender in AVAILABLE_FORMATS, f'No format has been adopted for objects of the gender `{format_gender}`.'
    assert format_name in AVAILABLE_FORMATS[format_gender], f'Format_name `{format_name}` unsupported for objects of gender {format_gender}.'
    return AVAILABLE_FORMATS[format_gender][format_name]

def file_extension_to_format_name(file_extension):
    for format_gender in AVAILABLE_FORMATS:
        for format_name in AVAILABLE_FORMATS[format_gender]:
            if AVAILABLE_FORMATS[format_gender][format_name] == file_extension:
                return format_name
    assert False, f'No adopted format is associated to the file_extension `{file_extension}`.'

def format_name_expand(format_name, format_gender):
    long_format_name = format_name_to_file_extension(format_name, format_gender)
    format_list = long_format_name.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = None
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]
    return format_primary, format_secondary


'''  
  GENERATORE DI ISTANZE 
'''
def instance_to_str(instance, format_name=DEFAULT_INSTANCE_FORMAT):
    """This function returns the string representation of the given <instance> provided in format <instance_format_name>"""
    format_primary, format_secondary = format_name_expand(format_name, 'instance')
    if format_primary == 'dat':
        return instance_to_dat_str(instance, format_name)
    if format_primary == 'txt':
        return instance_to_txt_str(instance, format_name)

def instance_to_txt_str(instance, format_name="with_len"):
    """Of the given <instance>, this function returns the .txt string in format <format_name>"""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
    rainbow = instance['rainbow'] 
    #seq_len = instance['seq_len']
    output= f''

    if format_name == "with_len":
      seq_len = instance['seq_len']
      output += f'{seq_len}\n'

    # Devo specificare la riga dell'array, anche se ce n'è una sola...
    #for i in rainbow[0]:
    for i in rainbow:
      output += str(i) + ' '

    output += '\n'

    return output

def get_instance_from_str(instance_as_str, instance_format_name=DEFAULT_INSTANCE_FORMAT):
    """This function returns the instance it gets from its string representation as provided in format <instance_format_name>."""
    format_primary, format_secondary = format_name_expand(instance_format_name, 'instance')
    if format_primary == 'dat':
       return get_instance_from_dat(instance_as_str, instance_format_name)
    if format_primary == 'txt':
      return get_instance_from_txt(instance_as_str, instance_format_name)

def get_instance_from_txt(instance_as_str, format_name):
    """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
    assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
    instance = {}
    str_to_arr = instance_as_str.split()

    if format_name != "with_len":
      instance['rainbow'] = str_to_arr
      #instance['seq_len'] = len(str_to_arr)

    else:
      instance['rainbow'] = str_to_arr[1:]
      instance['seq_len'] = len(str_to_arr[1:])
    
    return instance

def instance_to_dat_str(instance,format_name='collage_dat'):
  """Of the given <instance>, this function returns the .dat string in format <format_name>"""
  assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{format_name}` unsupported for objects of category `instance`.'
  rainbow = ' '.join(map(str, instance['rainbow']))
  seq_len = instance['seq_len']

  output = f"param n := {seq_len};                  # Number of stripes in the rainbow\n"
  output += "param: RAINBOW COLORS "
  output += f":= {rainbow} "
  output += ";\nend;"
    
  return output

def get_instance_from_dat(instance_as_str, format_name):
  """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
  assert format_name in AVAILABLE_FORMATS['instance'], f'Format_name `{instance_format_name}` unsupported for objects of category `instance`.'
  split_instance = instance_as_str.split(";")
  instance = {}

  instance['seq_len'] = int(get_param(split_instance[0])) # assign seq_len
  instance['rainbow'] = list(ast.literal_eval(get_param(split_instance[1]).replace("] [","],[").replace(" ","")))

  return instance

def instances_generator(num_instances, scaling_factor: float, seq_len: int, num_col: int, type_seq: int, seed = "random_seed"):
    instances = []
    for _ in range(num_instances):
      instance = {}
      if seed == "random_seed":
        seed = random.randint(100000,999999)
      instance['seq_len'] = seq_len
      instance['rainbow'] = random_rainbow(seq_len, num_col, type_seq, seed)
      instance['num_col'] = num_col
      instance['type_seq'] = type_seq
      instance['seed'] = seed

      seq_len = math.ceil(scaling_factor *  seq_len)

      if seq_len <= 10:
        num_col = math.ceil((seq_len / 100) * 40)

        if(num_col > MAX_NUM_COL):
          num_col = min(num_col, MAX_NUM_COL)

      elif seq_len > 10 and seq_len <= 30:
        num_col = math.ceil((seq_len / 100) * 60)

        if(num_col > MAX_NUM_COL):
          num_col = min(num_col, MAX_NUM_COL)

      elif seq_len < 30 and seq_len <= 100:
        num_col = math.ceil((seq_len / 100) * 70)

        if(num_col > MAX_NUM_COL):
          num_col = min(num_col, MAX_NUM_COL)

      else:
        num_col = math.ceil((seq_len / 100) * 80)

        if(num_col > MAX_NUM_COL):
          num_col = min(num_col, MAX_NUM_COL)

      instance['measured_time'] = None
      instance['answer_correct'] = None
      instances.append(instance)

    return instances

def random_rainbow(seq_len:int, num_col:int, type_seq:int, seed:int):
  random.seed(seed)
  rainbow = []

  # Random con colori uguali adiacenti
  if type_seq == 1:
    values = [i for i in range (num_col)]

    for row in range(0,seq_len):
      rainbow.append(random.choice(values))

  # Random senza colori uguali adiacenti
  elif type_seq == 2:
    oldColor = MAX_NUM_COL

    for row in range(seq_len):
      tmp = random.randint(0, sys.maxsize) % num_col
      tmp = (tmp + (tmp == oldColor)) % num_col;
      oldColor = tmp;
    
      rainbow.append(tmp)

  else:
    exit(0)

  return rainbow


def print_rainbow(rainbow, instance_format=DEFAULT_INSTANCE_FORMAT):
  seq_len = len(rainbow)

  # Commentare questa riga nel caso non si voglia il numero di elementi a video
  if instance_format == "with_len":
    print(seq_len)

  line = ''

  for i in rainbow:
    line += f'{i} '
    
  print(f'{line}')

''' Fine sezione generatori '''


'''
SOLUZIONI
'''
def solutions(instance, print_sol, instance_format=DEFAULT_INSTANCE_FORMAT):
    sols = {}
    if print_sol:
      sheets, sol = calculate_sheets(instance['rainbow'], print_sol)
      sols['calculate_sheets'] = f"{sheets}"
      print_sol = '\n'.join(map(str, reversed(sol.split('\n'))))
      sols['print_sol'] = f"\n{print_sol}\n"
    else:
      sheets = calculate_sheets(instance['rainbow'], print_sol)
      sols['calculate_sheets'] = f"{sheets}"


    return sols

# Recursive solution (faster)
def Min(i:int, j:int):
  if i > j:
    return 0
  
  if i == j:
    return 1
  
  if memo[i][j] > 0:
    return memo[i][j]

  ret = 1 + Min(i+1, j)

  for k in range(i+1,j+1):
    if seq[k] == seq[i]:
      ret = min(ret, Min(i+1, k-1) + Min(k, j))

  memo[i][j] = ret

  return memo[i][j]

# Dynamic Programming solution (slower)
def PD(n):
  for i in range(n, -1, -1):
    for j in range(i-1, n):
      if(i > j):
        memo[i][j] = 0
      elif(i==j):
        memo[i][j] = 1
      else:
        memo[i][j] = 1 + memo[i+1][j];
        for k in range(i+1, j+1):
          if seq[k] == seq[i]:
            memo[i][j] = min(memo[i][j], memo[i+1][k-1] + memo[k][j])
  #return memo[0][n-1]
  sheets = memo[0][n-1]

  foglio_sotto = None
  buf = []
  counti = 0
  sol = ''

  while i<n and n>0:
    if seq[i] == seq[n-1]:
      for h in range(i,n):
        if seq[n-1] != foglio_sotto:
          sol += str(seq[n-1]) + ' '
        else:
          sol += '  '

      sol += ' '.join(map(str,reversed(buf))) +'\n'

      counti = i+1
      for z in range(counti):
        sol += '  '

      buf = []
      foglio_sotto = seq[n-1]

      i+=1
      n-=1

    #elif memo[i][n] >= memo[i+1][n-1]:
    elif memo[i][n-2] >= memo[i+1][n-1]:
      if seq[i] != foglio_sotto:
        sol += str(seq[i]) + ' '
      else:
        sol += '  '
      i+=1

    else:
      if seq[n-1] != foglio_sotto:
        buf.append(seq[n-1])
      else:
        sol += '  '
      n-=1

  return sheets, sol

def calculate_sheets(rainbow, print_sol):
  seq_len = len(rainbow)
  n=0
  prev=-1

  for i in range(seq_len):
    tmp = rainbow[i]

    if tmp != prev:
      seq.append(tmp)
      prev = tmp
      n += 1

  if not print_sol:
    risp = Min(0,n-1)
    return risp
  else:
    risp, sol = PD(n)
    return risp, sol


'''
GOAL SUMMARIES
'''
def print_goal_summary(goal,testcases,num_testcases_passed,num_testcases_correct_ans,num_testcases_wrong_ans,out_of_time, TAc,LANG):
  TAc.print(LANG.render_feedback("summary", f'\n# SUMMARY OF THE RESULTS FOR GOAL "{goal}":\n'), "white", ["bold"])

  for t,i in zip(testcases,range(1,1+len(testcases))):
    if t['answer_correct'] == True:
      TAc.print(LANG.render_feedback("right-ans", f'# TestCase {i}: Correct answer! Took time {t["measured_time"]} on your machine.\n'), "green")
    elif t['answer_correct'] == False:
      TAc.print(LANG.render_feedback("wrong-ans", f'# NO! You gave the wrong solution for the instance with this parameters:\n#seq_len = {t["seq_len"]}, num_col = {t["num_col"]}, seed = {t["seed"]}.\n'), "yellow")
    else:
      TAc.print(LANG.render_feedback("out-of-time-ans", f'# The evaluation has been stopped since your solution took too much time on this or previous instances. The parameters of this instance are:\n#seq_len = {t["seq_len"]}, num_col = {t["num_col"]}, seed = {t["seed"]}.\n'), "white")
       
  if num_testcases_passed == len(testcases):
    TAc.print(LANG.render_feedback("right-in-time", f'# OK! Your solution achieved goal "{goal}".\n'), "green")

  if out_of_time > 0 and num_testcases_wrong_ans == 0:
    TAc.print(LANG.render_feedback("right-not-in-time", f'# OK! Though all answers produced by your solution are correct, still it exceeded the time limit on some instances. As such, you did not achieve goal "{goal}".\n'), "yellow")
  elif num_testcases_wrong_ans != 0:
    TAc.print(LANG.render_feedback("wrong-answ", f'# NO! Your solution gave wrong answers on at least one instance. Your solution does NOT achieve goal "{goal}".\n'), "red")   


def print_summaries(goals,instances,MAX_TIME,out_of_time,TAc,LANG):    
  TAc.print(LANG.render_feedback('summary-of-results', '# SUMMARY OF RESULTS:'), 'green')
  num_instances = {}
  num_instances_passed = {}
  num_instances_correct_ans = {}
  num_instances_wrong_ans = {}
  alive = True

  for goal in goals:
      num_instances[goal] = len(instances[goal])
      num_instances_passed[goal] = 0
      num_instances_correct_ans[goal] = 0
      num_instances_wrong_ans[goal] = 0

      for instance in instances[goal]:
        if instance['answer_correct'] == False:
          num_instances_wrong_ans[goal] += 1
        elif instance['answer_correct'] == True:
          num_instances_correct_ans[goal] += 1

          if instance['measured_time'] <= MAX_TIME:
            num_instances_passed[goal] += 1

      if alive:
        print_goal_summary(goal,instances[goal],num_instances_passed[goal],num_instances_correct_ans[goal],num_instances_wrong_ans[goal], out_of_time, TAc,LANG)

      if num_instances_passed[goal] < num_instances[goal]:
        alive = False

  TAc.print(LANG.render_feedback('short-summary-of-results', '# SUMMARY OF RESULTS:'), 'green')

  for goal in goals:
    if num_instances_passed[goal] == num_instances[goal]:
      TAc.print(LANG.render_feedback('goal-passed', f'# Goal {goal}: PASSED (passed instances: {num_instances_passed[goal]}/{num_instances[goal]} instances)'), 'green', ['bold'])
    else:
      TAc.print(LANG.render_feedback('goal-NOT-passed', f'# Goal {goal}: NOT passed (passed instances: {num_instances_passed[goal]}/{num_instances[goal]} instances, correct answers: {num_instances_correct_ans[goal]}/{num_instances[goal]}, wrong answers: {num_instances_wrong_ans[goal]}/{num_instances[goal]} instances)'), 'red', ['bold'])
  
  TAc.print(f"\n# WE HAVE FINISHED", "white")
