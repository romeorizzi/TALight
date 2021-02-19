#!/usr/bin/python3
#import TAlight  dove collocare le funzioni scritte una volta per tutte a bagaglio comune dei problemi.
import sys
import yaml
from termcolor import colored, cprint
# https://pypi.org/project/termcolor/
# to install termcolor:
# pip install termcolor
# to correctly visualize ASCII escapes (for supporting colors) on Windows maybe a filter based on colorama, on the client side, could work:
#https://python.libhunt.com/colorama-alternatives
#https://pythonawesome.com/simple-cross-platform-colored-terminal-text-in-python/
#from colorama import init
#init()

text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
print(text)
cprint('Hello, World!', 'green', 'on_red')

print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
print_red_on_cyan('Hello, World!')
print_red_on_cyan('Hello, Universe!')

for i in range(10):
    cprint(i, 'magenta', end=' ')

cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)



def internal_error(error_nickname, message):  # this function should go in a problem-independent library
   cprint(f"({error_nickname}) Internal error (never fault of the problem solver, detectable with local testing):", 'red', 'on_cyan', attrs=['bold'])
   cprint(message, 'on_cyan')
   #print(f"({error_nickname}) Internal error (never fault of the problem solver, detectable with local testing):")
   #print(message)
   sys.exit(2)
            
def format_error(feedback_nickname, goal, subtask, message = None):  # this function should go in a problem-independent library
   """Format error. This is fault of the problem solver (on a side that often it is not relevant at all, only a lack of care in the programming issue). Either it must be served here in the checkers writing parsing code (takes a lot of time and load on the problem maker. Also: it makes lenghtly adapting old problems), or format defined and assessed via yaml file). Most of the times (all CMS-like problems) we can obtain, for each goal, a template solution which manages input/output and only calls a function out from a simple yaml file + small script in a minimal language defined by us"""
   cprint(f"({feedback_nickname}) Format error.", 'red', 'on_cyan', attrs=['bold'], end=" ")
   cprint(f"You should review the format of the file you have submitted for [problem={codeproblem}, goal={goal}, subtask={subtask}]. (You can do it in local, also taking profit of the format checking script made available to you.\n", 'on_cyan')
   #print(f"({feedback_nickname}) Format error.", end=" ")
   #print(f"You should review the format of the file you have submitted for [problem={codeproblem}, goal={goal}, subtask={subtask}]. (You can do it in local, also taking profit of the format checking script made available to you.\n")
   if message != None:
      cprint("More precisely, pay attention to this:", 'on_cyan')
      #print("More precisely, pay attention to this:")
      print(message)
   sys.exit(0)

def solution_error(feedback_nickname, goal, subtask, message = None):  # this function should go in a problem-independent library
   """True feedback on the problem. There are errors in the solution submitted. This is fault of the problem solver."""
   #cprint(f"({feedback_nickname}) Error found in the solution you submitted for [problem={codeproblem}, goal={goal}, subtask={subtask}].\n", 'red', 'on_cyan', attrs=['bold'])
   print(f"({feedback_nickname}) Error found in the solution you submitted for [problem={codeproblem}, goal={goal}, subtask={subtask}].\n")
   if message != None:
      cprint("More precisely, pay attention to this:", 'on_cyan')
      #print("More precisely, pay attention to this:")
      print(message)
   sys.exit(0)

def solution_OK(feedback_nickname, goal, subtask, message = None):  # this function should go in a problem-independent library
   cprint(f"({feedback_nickname}) OK. Your solution to [problem={codeproblem}, goal={goal}, subtask={subtask}] is a feasible one.", 'green', attrs=['bold'])
   #print(f"({feedback_nickname}) OK. Your solution to [problem={codeproblem}, goal={goal}, subtask={subtask}] is a feasible one.")
   if message != None:
      print(message)
   sys.exit(0)

def solution_perfect(feedback_nickname, goal, subtask, lesson = None, next_challenge = None):  # this function should go in a problem-independent library
   cprint(f"({feedback_nickname}) OK. Your solution to [problem={codeproblem}, goal={goal}, subtask={subtask}] is perfect!", 'green', attrs=['bold'])
   #print(f"({feedback_nickname}) OK. Your solution to [problem={codeproblem}, goal={goal}, subtask={subtask}] is perfect!")
   if lesson != None:
      cprint("What have we learned:", 'red')
      #print("What have we learned:")
      print(lesson)
   if next_challenge != None:
      cprint("What next:", 'red')
      #print("What next:")
      print(next_challenge)
   sys.exit(0)


# PROBLEM SPECIFIC PART:   
codeproblem = "tiling_mxn-boards_by_1x2-boards"  
M=20
N=20

with open("eval_submission.it.yaml", 'r') as stream:
    try:
        api = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

def is_tilable(m, n):
   return 1 - (m%2)*(n%2)


def check_decision(goal, subtask):
   """
   Se subtask=1 si chiede di verificare solo la prima riga di risposte (per griglie con m=1, ossia di una sola riga).
   Se subtask=2 si chiede di verificare solo le prime due righe di risposte (per m=1 e m=2).
   Se subtask=3 vanno verificate tutte le MxN risposte.
   """

   def fstr(template):
    return eval(f"f'{template}'")

   global M
   if subtask <= 2:
      M = subtask
   for i in range(1,M+1):
      try:
         risp_line_full = sys.stdin.readline()
         risp_line = risp_line_full.rstrip()
      except EOFError:
         tmpstr1=api["too-few-lines"]
         format_error("too-few-lines", goal, subtask, eval(f"f'{tmpstr1}'"))
      if len(risp_line) != N:
         if len(risp_line_full)-len(risp_line) == 1:
           tmpstr1=api["wrong-line-length-single-newline-char"]
           format_error("wrong-line-length-single-newline-char", goal, subtask, eval(f"f'{tmpstr1}'"))
         else:  
           tmpstr1=api["wrong-line-length-more-newline-chars"]
           format_error("wrong-line-length-more-newline-chars", goal, subtask, eval(f"f'{tmpstr1}'"))
      for j in range(1,N+1):
         if risp_line[j-1] not in {"0","1"}:
            tmpstr1=api["wrong-char-bool"]
            format_error("wrong-char-bool", goal, subtask, eval(f"f'{tmpstr1}'"))
         if int(risp_line[j-1]) != is_tilable(i, j):
            if is_tilable(i, j):
               tmpstr1=api["wrong0-answ"]
               solution_error("wrong0-answ", goal, subtask, eval(f"f'{tmpstr1}'"))
            else:
               tmpstr1=api["wrong1-answ"]
               solution_error("wrong1-answ", goal, subtask, eval(f"f'{tmpstr1}'"))

   if M==1:          
        solution_perfect("perfect1-1-challenge", goal, subtask, api["perfect1-1-lesson"], api["perfect1-1-challenge"])
   elif M==2:          
        solution_perfect("perfect1-2-challenge", goal, subtask, api["perfect1-2-lesson"], api["perfect1-2-challenge"])
   else:          
        solution_perfect("perfect1-3-challenge", goal, subtask, api["perfect1-3-lesson"], api["perfect1-3-challenge"])

def check_tiling(goal, subtask):
   """
   Valutiamo il tiling offerto anche se esso è per una griglia più grande che come inteso dal subtask scelto.
   """

   def fstr(template):
    return eval(f"f'{template}'")

   m, n = map(int, sys.stdin.readline().split())
   
   if not ( (0 <= m <= 20) and (0 <= n <= 20)):
      tmpstr1=api["out-of-range-m-n"]
      format_error("out-of-range-m-n", goal, subtask, eval(f"f'{tmpstr1}'"))

   booked = [False] * 20
   for i in range(1,m+1):
      try:
         risp_line_full = sys.stdin.readline()
         risp_line = risp_line_full.rstrip()
      except EOFError:
         tmpstr1=api["too-few-lines"]
         format_error("too-few-lines", goal, subtask, eval(f"f'{tmpstr1}'"))
      if len(risp_line) != n:
         if len(risp_line_full)-len(risp_line) == 1:
           tmpstr1=api["wrong-line-length-single-newline-char"]
           format_error("wrong-line-length-single-newline-char", goal, subtask, eval(f"f'{tmpstr1}'"))
         else:  
           tmpstr1=api["wrong-line-length-more-newline-chars"]
           format_error("wrong-line-length-more-newline-chars", goal, subtask, eval(f"f'{tmpstr1}'"))
      for j in range(1,n+1):
         if booked[j-1] and risp_line[j-1] != "S":
            i = i-1
            tmpstr1=api["wrong-N"]
            format_error("wrong-N", goal, subtask, eval(f"f'{tmpstr1}'"))
         if risp_line[j-1] not in {"N","S","W","E"}:
            tmpstr1=api["wrong-char-card-point"]
            format_error("wrong-char-card-point", goal, subtask, eval(f"f'{tmpstr1}'"))
         if risp_line[j-1] == "S" and booked[j-1] == False:
            tmpstr1=api["wrong-S"]
            format_error("wrong-S", goal, subtask, eval(f"f'{tmpstr1}'"))
         if risp_line[j-1] == "E" and (j==1 or risp_line[j-1] != "W"):
            tmpstr1=api["wrong-E"]
            format_error("wrong-E", goal, subtask, eval(f"f'{tmpstr1}'"))
         if risp_line[j-1] == "W" and (j==n or risp_line[j+1] != "E"):
            tmpstr1=api["wrong-W"]
            format_error("wrong-W", goal, subtask, eval(f"f'{tmpstr1}'"))
         if risp_line[j-1] == "N":
            if i==m:
               tmpstr1=api["wrong-N"]
               format_error("wrong-N", goal, subtask, eval(f"f'{tmpstr1}'"))
            booked[j-1] == True
   solution_perfect("perfect2-challenge", goal, subtask)
   
      
        
tmpstr1=api["goal2-task3"]
#internal_error("goal2-task3", eval(f"f'{tmpstr1}'"))
internal_error("goal2-task3", tmpstr1)

check_decision("decision", 1)
check_tiling("tiling", 1)
