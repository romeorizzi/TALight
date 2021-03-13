#!/usr/bin/env python3

def num_sol(num_pairs):
    # risps_correct[num_open][num_closed] = number of different prefixes of well-formed formula with <num_open> open parentheses and <num_closed> closed parentheses.
    risps_correct = [ [1] * (num_pairs+2) for _ in range(num_pairs+1)]
    for num_open in range(1,num_pairs+1):
        risps_correct[num_open][0] = risps_correct[num_open-1][1]
        for num_closed in range(1,num_pairs+1):
            risps_correct[num_open][num_closed] = risps_correct[num_open][num_closed-1] + risps_correct[num_open-1][num_closed+1]

    return risps_correct[num_pairs][0]

def unrank(n_pairs, pos, sorting_criterion="loves_opening_par"):
    if n_pairs == 0:
        return ""
    """(  ... )  ...
           A      B
    """    
    count = 0
    for n_pairs_in_A in range(n_pairs) if sorting_criterion=="loves_closing_par" else reversed(range(n_pairs)):
        num_A = num_sol(n_pairs_in_A)
        num_B = num_sol(n_pairs - n_pairs_in_A -1)
        if count + num_A*num_B > pos:
            break
        count += num_A*num_B
    return "(" + unrank(n_pairs_in_A, (pos-count) // num_B) + ")" + unrank(n_pairs - n_pairs_in_A -1, (pos-count) % num_B)


def recognize(formula_of_parentheses, TAc, LANG):
    #print(f"formula_of_parentheses={formula_of_parentheses}")
    num_dangling_open = 0
    for day, i in zip(formula_of_parentheses,range(1,len(formula_of_parentheses)+1)):
        if day == '(':
            num_dangling_open += 1
        else:
            if num_dangling_open == 0:
                TAc.print(formula_of_parentheses, "yellow", ["underline"])
                TAc.print(LANG.render_feedback("unfeasible", f"No. On position {i} there is no open parenthesis left to be closed. This formula is not well formed."), "red", ["bold"])
                return False
            num_dangling_open -= 1

    if num_dangling_open > 0:
        TAc.print(formula_of_parentheses, "yellow", ["underline"])
        TAc.print(LANG.render_feedback("unfinished", f"No. You have left {num_dangling_open} open parenthesis unclosed. This formula is not well formed. It contains more '(' than ')' characters."), "red", ["bold"])
        return False
    return True
