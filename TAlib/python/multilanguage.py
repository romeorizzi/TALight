#!/usr/bin/env python3

from sys import stderr, exit

yaml_is_installed = True
try:
    import yaml
except Exception as e:
    yaml_is_installed = False
    print("# Recoverable Error: ", end="", file=stderr)
    print(e, file=stderr)
    print("# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.\n# (To enjoy a feedback in a supported language install the python package yaml. The languages supported by a problem service appear as the options for the lang parameter listed by the command `rtal list`)", file=stderr)

termcolor_is_installed = True
try:
    from termcolor import colored, cprint
except Exception as e:
    termcolor_is_installed = False
    print("# Recoverable Error: ", end="", file=stderr)
    print(e, file=stderr)
    print("# --> We proceed using no colors. Don't worry.\n# (To enjoy colors install the python package termcolor.)", file=stderr)
    
colored_print = None
numNO = 0
numOK = 0

def set_colors(with_colors):
    global colored_print
    colored_print = with_colors and termcolor_is_installed
    
def select_book_and_lang(service_name, ENV_lang):
    messages_book_file = service_name + "." + ENV_lang + ".yaml"
    if not yaml_is_installed:
        return None
    try:
      with open(messages_book_file, 'r') as stream:
        try:
          messages_book = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
          print(f"# Recoverable Error: The messages_book file `{messages_book_file}` for multilingual feedback is corrupted (not a valid .yaml file)\n# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
          print(exc, file=stderr)
          return None
    except IOError as ioe:
          print(f"# Recoverable Error: The messages_book file `{messages_book_file}` for multilingual feedback could not be accessed.\n# --> We proceed with no support for languages other than English. Don't worry: this is not a big issue.", file=stderr)
          print(ioe, file=stderr)
          return None
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

