#!/usr/bin/env python3

from sys import stderr, exit
import yaml
from termcolor import colored, cprint

colored_print = None
numNO = 0
numOK = 0

def set_colors(with_colors):
    global colored_print
    colored_print = with_colors
    
def select_book_and_lang(service_name, ENV_lang):
    messages_book_file = service_name + "." + ENV_lang + ".yaml"
    with open(messages_book_file, 'r') as stream:
      try:
          messages_book = yaml.safe_load(stream)
      except yaml.YAMLError as exc:
          print(f"problem: The messages_book file `{messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file)", file=stderr)
          print(exc, file=stderr)
          exit(1)
    return messages_book 

def TAcprint(msg_text, *msg_rendering, **kwargs):
  if type(msg_rendering[-1]) == list:
      msg_style = msg_rendering[-1]
      msg_colors = msg_rendering[:-1]
  else:
      msg_style = []
      msg_colors = msg_rendering
  if colored_print:
      print(colored(msg_text, *msg_colors, attrs=msg_style), **kwargs)
  else:
      print(msg_text, **kwargs)


def TAcNO():
    global numNO
    numNO += 1
    TAcprint("No! ", "red", ["blink", "bold"], end="")

def TAcOK():
    global numOK
    numOK += 1
    TAcprint("OK! ", "green", ["bold"], end="")

def TAcGotBored():
    TAcprintprint("! (I got bored)", "white")

def TAcFinished():
    TAcprint(f"! (We have finished) Correct answers: {numOK}/{numOK+numNO}", "white")

