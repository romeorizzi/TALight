#!/usr/bin/env python3
from sys import stdout, stderr, exit
import re

def try_to_convert(tk, tk_type, regex, TAc=None):
    if tk_type == bool:
        try: 
            risp = bool(tk)
            return int(risp)
        except (TypeError, ValueError):
            return None
    elif tk_type == int:
        try: 
            risp = int(tk)
            return risp
        except (TypeError, ValueError):
            return None
    elif tk_type == float:
        try: 
            risp = float(tk)
            return risp
        except (TypeError, ValueError):
            return None
    elif tk_type == str:
        if tk.upper() == "END":
            return "end"
        if tk.upper() == "#END":
            return "#end"
        matched = re.match(regex, tk)
        if bool(matched):
            return tk
        else:
            return None
    else:
        for out in [stdout, stderr]:
            TAc.print(f"Internal error (please, report it to the problem maker): the TALinputs library does not support the '{tk_type}' token type. The problem maker should either extend the library or adapt to it.", "yellow", ["bold"], file=out)
        exit(1)

def TALinput(token_type, num_tokens=None, sep=None, exceptions = set({}), comment_lines_start_with='#', regex="^((\S)+)$", regex_explained=None, line_recognizer=None, TAc=None, LANG=None):
    """this function is mainly meant to parse input lines comprising one or more tokens of type 'token_type'. The separation in tokens is performed by the python standard split method: if 'sep'=None then runs of consecutive whitespace characters are regarded as a single separator, otherwise the argument 'sep' should be one single character like ',' and the input line is separated into fields like the ones of a .csv file). If 'num_tokens' is set to a positive natural number (rather than let to its default None value) and the number of tokens does not correspond then the function tells the problem solver that she has not respected the problem protocol and drops the channel. The function mainly returns the list of the tokens after they have been interpreted as the objects of type 'token_type' they are meant to represent. The argument 'exceptions' contains a set of input strings that are considered valid input lines (end returned verbatim to the caller) even though they do not offer a valid representation of an object of type `token_type` (or do not split in tokens which all do). Usually, these 'exceptions' strings will be then interpreted as commands that the problem maker had decided to allow. After this, if the first character of the line input by the problem solver occurs in the parameter string 'comment_lines_start_with' then the function returns None (usually, as a consequence of this, the line is simply ignored as a whole (unless it occurs, as a whole, in the set 'exceptions' and then is interpreted as a meta-level command). All other valid input strings are turned into the list of objects their tokns represent. (We insist: the function returns the actual objects rather than just the plain string representation of them.) When the conversion from string to object fails then a standardized, clear, and easily recognizable error specific to the data type is printed and the service channel is dropped. The set of available data types is meant to be extensible by the problem-maker who can add code to this 'TALinputs.py' file (warning: since this is a library module common to all problems one should check that the other problems still work before committing/pushing and the changes should be incremental and agreed upon within the same problem collection repo, not to impair your other running problems at the next commit-push. Yours, or of your collaborators or community). The last two parameters are meaningful only when 'token_type'=str. In this case, the function checks that each string token respects the regex before returning it to the caller. It is important to make sure that none of the possible input strings that split in string tokens respecting the regex occur in the 'exception' list nor begin with a character in the 'comment_lines_start_with' string since these lines are ignored or immediately returned by the function before the tokenization and the checking of the tokens against the regex. If you are unconfident with regular expressions, first explanations and good regex online services are at https://extendsclass.com/regex-tester.html or at https://regexr.com/). When the check against the regex fails then a clear, and easily recognizable error is printed and the service server is halted. This error can be personalized without modifying this file by resorting on parameter 'regex_explained'. This offers a rudimentary but simple and quite effective solution which has turned out to be fully satisfactory up to now. It works out as follows: first the problem solver is told about the token string parsing problem and the regexp that had to be respected by her token is printed verbatim. Then, if 'regex_explained' is not None, then the following line is also printed before dropping the service channel: 'In practice, the expected string should be {regex_explained}'."""
    while True:
        input_line = input()
        if input_line in exceptions:
            return (input_line,)
        if len(input_line) == 0:
            if num_tokens > 1 or token_type != str:
                TAc.print(f"You have entered an unexpected empty line. I assume you want to drop this TALight service call. See you next time ;))", "yellow")
                exit(0)
            else:
                tokens = [""] 
                break
        if input_line[0] not in comment_lines_start_with:
            tokens = input_line.split() 
            break
    if len(tokens) != num_tokens:
        for out in [stdout, stderr]:
            TAc.print("Input error from the problem-solver:", "red", ["bold"], file=out,end=" ")
            print(f"the server was expecting a line with {num_tokens} tokens but the line you entered:\n{input_line}\ncontains {len(tokens)} != {num_tokens} tokens.\n", file=out)
            TAc.print("I am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", "yellow", file=out)
            if sep != None:
               TAc.print(f"The token separation character for this problem service is '{sep}'.", file=out)
        exit(0)
    vals = []
    for token, i in zip(tokens,range(1,1+len(tokens))):
        vals.append(try_to_convert(token, token_type, regex, TAc=TAc))
        if vals[-1] == None:
            if token_type == str:
                for out in [stdout, stderr]:
                    TAc.print("Input error from the problem-solver:", "red", ["bold"], file=out,end=" ")
                    if len(tokens) > 1:
                        print(f"Input error from the problem-solver:  when it got to the {i}-th token:\n'{token}'\nof your input line\n'{input_line}'\nthe server was actually expecting a string matching the regex:\n{regex}\nbut the string you entered does not comply the regex.\n", file=out)
                    else:
                        print(f"Input error from the problem-solver:  the server was actually expecting a string matching the regex:\n{regex}\nbut the string you entered does not comply the regex.\n", file=out)
                    if regex_explained != None:
                        print(f"In practice, the expected string should be {regex_explained}", file=out)
                    TAc.print(f"\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", "yellow", file=out)
            else:
                for out in [stdout, stderr]:
                    TAc.print("Input error from the problem-solver:", "red", ["bold"], file=out,end=" ")
                    print(f"Input error from the problem-solver: the server was expecting a token of type {token_type} when it got to the {i}-th token:\n'{token}'\nof your input line\n'{input_line}'.\n", file=out)
                    TAc.print("I am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", "yellow", file=out)
            exit(1)
        if line_recognizer != None and not line_recognizer(vals[-1], TAc, LANG):
            return (None,)
    return [val for val in vals]

# For the future, we plan to offer more than one possible extensions to the TALinput function above that inputs one single token.
# One such likely extension is:
#
#def TALinput_csv_line
#
# However, we should also try to introduce these more complex forms of preformatted inputs only gradually. Let's first try to make the best use of few and simple primitives that can be general and solid and introduce the more complex ones when their use, purpose and reach becomes clear.
# We have understood one thing on this front: more tools might be better than trying to hit too many birds with one single stone.

# The following function, at present, is just the remaining of an extension where the line contains different tokens of different types. We made it too early and we later realized that, for the time being, the cases it was meant to cover could be covered with a convenient extension to the TALinput function above.  

def TALinput_line(tokens_type, regex="^((\S)+)$", regex_explained=None, line_recognizer=None, comment_or_command_lines_start_with='#', last_line_command=None):
    """returns False only when the `last_line_command` parameter is a string like 'end' and the input line is a command line like '#end' or '#end'. (This is useful when we are reading a open number of lines.) Otherwise it either stops the service server execution signaling a violation of the protocol error, or returns a list of tokens of the type and format prescribed in the expected_tokens list argument."""
    if last_line_command != None:
        last_line_command = last_line_command.upper()
    while True:
        input_line = input()
        if len(input_line) == 0:
            print(f"You have entered an unexpected empty line. I assume you want to drop this TALight service call. See you next time ;))")
            exit(0)
        if input_line[0] not in ignore_lines_start_with:
            break
        if input_line[1:].split()[0].upper() == stopping_line:
            return False
    tokens = input_line.split() 
    if len(tokens) != len(tokens_type):
        for out in [stdout, stderr]:
            print(f"Input error from the problem-solver: the server was expecting a line with {len(tokens_type)} tokens but the line you entered:\n{input_line}\ncontains {len(tokens)} != {len(tokens_type)} tokens.\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=out)
        exit(0)
    vals = []
    for tk, tk_type, i in zip(tokens,tokens_type,range(1,1+len(tokens))):
        vals.append(try_to_convert(tk, tk_type,regex, TAc=TAc))
        if vals[-1] == None:
            if tk_type == str:
                for out in [stdout, stderr]:
                    print(f"Input error from the problem-solver:  when parsing the {i}-th token of your input line, namely the string:\n{tk}\nthe server was actually expecting a string matching the regex:\n{regex}\nbut the string you entered does not comply the regex.\n", file=out)
                    if regex_explained != None:
                        print(f"In practice, the expected string should be either 'end' (to close the input) or {regex_explained}", file=out)
                    print(f"\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=out)
            else:
                for out in [stdout, stderr]:
                    print(f"Input error from the problem-solver: the server was expecting a token of type {tk_type} when it got the token '{tk}'.\nI am dropping the communication because of violation of the intended protocol between problem solver and problem maker.", file=out)
            exit(1) 
    return (val for val in vals)
