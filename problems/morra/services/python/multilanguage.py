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
    TAcprint("No! ", "red", "on_blue", ["blink"], end="")

def TAcOK():
    global numOK
    numOK += 1
    TAcprint("OK! ", "green", "on_blue", end="")

def TAcGotBored():
    TAcprintprint("! (I got bored)", "green", "on_blue")

def TAcFinished():
    TAcprint(f"! (We have finished) Correct answers: {numOK}/{numOK+numNO}", "green", "on_blue")


# OLD STUFF:

def old_print_lang(*args,**kwargs):
  message1, *other_messages = args
  msg1_code, *msg1_rendering = message1
  msg1_text=eval(f"f'{messages_book[msg1_code]}'")
  if 'end' in kwargs:
      backup_end = kwargs['end']
  else:
      backup_end = None      
  if len(other_messages)>0:
    kwargs['end'] = ""
  TAcprint(msg1_text, *msg1_rendering, **kwargs)
  if len(other_messages)>0:
      kwargs['end'] = backup_end
      print_lang(*other_messages, **kwargs)

