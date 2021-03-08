#!/usr/bin/env python3

def recognize(formula_of_parentheses, TAc, LANG):
    num_dangling_open = 0
    for day, i in zip(formula_of_parentheses,range(1,len(formula_of_parentheses)+1)):
        if day == '(':
            num_dangling_open += 1
        else:
            if num_dangling_open == 0:
                TAc.print(formula_of_parentheses, "yellow", ["underline"])
                TAc.print(LANG.render_feedback("unfeasible", f"No. On position {i} there is no open parenthsis left to be closed. This formula is not well formed."), "red", ["bold"])
                return False
            num_dangling_open -= 1

    if num_dangling_open > 0:
        TAc.print(formula_of_parentheses, "yellow", ["underline"])
        TAc.print(LANG.render_feedback("unfinished", f"No. You have left {num_dangling_open} open parenthesis unclosed. This formula is not well formed. It contains more '(' than ')' characters."), "red", ["bold"])
        return False
    return True
