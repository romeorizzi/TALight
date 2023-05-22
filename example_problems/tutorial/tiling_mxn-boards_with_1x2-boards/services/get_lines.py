#!/usr/bin/env python3
from sys import stderr, exit

def get_line():
    raw_line = input().strip()
    if raw_line[0] != "#":            
        return raw_line, None
    key = raw_line[1:].strip().split()[0].upper()
    if key == "END" or key == "NEXT":
        return None, key 
    return None, "GEN_COMMENT"
    

def get_lines_from_stream(same_length = True, order_matters = False, unique = True, checks=[]):
    """ Puts the sequence of lines fed in into a list or a set (which one of the two depends on the value of the parameter 'order_matters'). In the case of a set the parameter `unique` set to True has the effect to assess unicity in the input stream. The input stream is ended with a line like '# END'."""
    print('#? waiting for a stream of lines. Insert a closing line "# END" after the last row of the table.')
    def get_line():
        raw_line = input().strip()
        if raw_line[0] != "#":            
            return raw_line, None
        key = raw_line[1:].strip().split()[0].upper()
        if key == "END" or key == "NEXT":
            return None, key 
        return None, "GEN_COMMENT"
    
    first_line, cmd = get_line() 
    while first_line == None:
        first_line, cmd = get_line()

    if order_matters:
        collected_lines = [first_line]
    else:
        collected_lines = {first_line}

    previous_line = first_line
    next_line, cmd = get_line() 
    while cmd != "END":
        if cmd == "NEXT":
            print("# Warning: I have asked for one single stream! I will assume this line was a comment and proceed reading and loading the previous table line by line.")
        elif next_line != None:
            if same_length and len(next_line) != len(previous_line):
                print(f"# Error (in the input stream of lines): The line {len(collected_lines)} has length different than the previous lines in the stream. This is not a valid stream here.")
                exit(1)
            previous_line = next_line
            if order_matters:
                collected_lines.append(next_line)
            else:
                if unique and (not order_matters) and next_line in collected_lines:
                    print(f"# Error (in the input stream of lines): The line {len(collected_lines)} is identical to a previous line in the stream. Repetitions are not valid here.")
                    exit(1)
                collected_lines.add(next_line)

        next_line, cmd = get_line()
    print("# FILE GOT")
    return collected_lines
