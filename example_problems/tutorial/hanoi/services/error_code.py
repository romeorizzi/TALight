#!/usr/bin/env python3


def print_move_error(code, TAc, LANG):
    if code == 1:
        TAc.print(LANG.render_feedback("code1", f'-> Invalid disk: not exist'), "red", ["reverse"])
    elif code == 2:
        TAc.print(LANG.render_feedback("code2", f'-> Invalid Peg: not exist'), "red", ["reverse"])
    elif code == 3:
        TAc.print(LANG.render_feedback("code3", f'-> Invalid move: current and target can\'t be equal'), "red", ["reverse"])
    elif code == 4:
        TAc.print(LANG.render_feedback("code4", f'-> asdWrong current or state: they don\'t coincide'), "red", ["reverse"])
    elif code == 5:
        TAc.print(LANG.render_feedback("code5", f'-> Invalid move: Toddler can\'t move last disk'), "red", ["reverse"])
    elif code == 6:
        TAc.print(LANG.render_feedback("code6", f'-> Invalid move: can\'t make a counterclockwise move'), "red", ["reverse"])
    elif code == 7:
        TAc.print(LANG.render_feedback("code7", f'-> Invalid move: can\'t move big disk on small disk'), "red", ["reverse"])
    elif code == 8:
        TAc.print(LANG.render_feedback("code8", f'-> Invalid disk: is blocked'), "red", ["reverse"])
    elif code == 0:
        TAc.print(LANG.render_feedback("code0", f'-> Correct move'), "red", ["reverse"])
    else:
        TAc.print(LANG.render_feedback("codeErr", f'-> This codeError is invalid'), "red", ["reverse"])