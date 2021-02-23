#!/usr/bin/env python3
from sys import stderr, exit

def convert2number(s):
    try: 
        risp = int(s)
        return risp
    except (TypeError, ValueError):
        pass
    try: 
        risp = float(s)
        return risp
    except (TypeError, ValueError):
        return None

def get_line():
    raw_line = input().strip()
    if raw_line[0] != "#":            
        return [tk.strip() for tk in raw_line.split("#")[0].split(sep)], None
    key = raw_line[1:].strip().split()[0].upper()
    if key == "END" or key == "NEXT":
        return None, key 
    return None, "GEN_COMMENT"
    

def get_one_numeric_table(sep=None, should_be_int=False, should_be_nat=False, row_names_start_from=0, col_names_start_from=0, checks=[]):
    """ When sep=None, the fields are separated by sequences of white characters. When sep="," then a .csv format is assumed, but you can specify use other separator characters or string. A "#" starts a comment for the rest of the line.   
       Examples:
       >[tk.strip() for tk in "wfwqf,   wqfwqfq, wfwfq".split(None)]
       returns ['wfwqf,', 'wqfwqfq,', 'wfwfq']
       > [tk.strip() for tk in "wfwqf,   wqfwqfq, wfwfq".split(",")]
       returns ['wfwqf', 'wqfwqfq', 'wfwfq']
    """
    print('# waiting for a rectangular table of numbers (a matrix). Insert a closing line "# END" after the last row of the table.')
    def get_line():
        raw_line = input().strip()
        if raw_line[0] != "#":            
            return [tk.strip() for tk in raw_line.split("#")[0].split(sep)], None
        key = raw_line[1:].strip().split()[0].upper()
        if key == "END" or key == "NEXT":
            return None, key 
        return None, "GEN_COMMENT"

    
    first_line, cmd = get_line() 
    while first_line == None:
        first_line, cmd = get_line()

    last_col = len(first_line) -1

    table_submitted = [ list(map(convert2number, first_line)) ]
    if any(_== None for _ in table_submitted[-1]):
        print(f"# Error (in the table format): All entries in your table should be numbers. Just check row {len(table_submitted)-1+row_names_start_from} in your file for a first occurrence of a type mismatch.")
        exit(1)
    def one_by_one_check():
        for col, val in zip(range(len(table_submitted[-1])), table_submitted[-1]):
            if should_be_int or should_be_nat:
                if type(val) != int:
                    print(f"# Error (in the table format): the entry ({len(table_submitted)-1+row_names_start_from},{col+col_names_start_from}) in your table should be an integer number. However, the value {val} is a non integer float with decimal part.")
                    exit(1)        
            if should_be_nat:
                if val<0:
                    print(f"# Error (in the table format): the entry ({len(table_submitted)-1+row_names_start_from},{col+row_names_start_from}) in your table should be a natural (i.e., non-negative) number. However, you entered the {val}<0 for that entry.")
                    exit(1)        
            for check in checks:
                check(row_index_name=len(table_submitted)-1+row_names_start_from, col_index_name=col+col_names_start_from, entry_val=val)
    one_by_one_check()

    next_line, cmd = get_line() 
    while cmd != "END":
        if cmd == "NEXT":
            print("# Warning: I have asked for one single table! I will assume this line was a comment and proceed reading and loading the previous table line by line.")
        elif next_line != None:
            if len(next_line) != last_col+1:
                print(f"# Error (in the table format): The row {len(table_submitted)+row_names_start_from} (rows are counted starting from {row_names_start_from}) of your table contains {len(next_line)} elements whereas all previous rows contain {last_col+1} elements.")
                exit(1)
            table_submitted.append(list(map(convert2number, next_line)))
            if any(_== None for _ in table_submitted[-1]):
                print(f"# Error (in the table format): All entries in your table should be numbers. Just check row {len(table_submitted)-1+row_names_start_from} in your file for a first occurrence of a type mismatch.")
                exit(1)
            one_by_one_check()

        next_line, cmd = get_line()
    print("# FILE GOT")
    return table_submitted
