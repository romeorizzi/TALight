#!/usr/bin/env python3
from hanoi_lib import generate_move, parse_move


def print_move_error(code, TAc, LANG):
    '''Print the cause of invalid move.'''
    if code == 1:
        TAc.print(LANG.render_feedback("code1", f'-> Invalid disk: not exist'), "red", ["reverse"])
    elif code == 2:
        TAc.print(LANG.render_feedback("code2", f'-> Invalid Peg: not exist'), "red", ["reverse"])
    elif code == 3:
        TAc.print(LANG.render_feedback("code3", f'-> Invalid move: current and target can\'t be equal'), "red", ["reverse"])
    elif code == 4:
        TAc.print(LANG.render_feedback("code4", f'-> Wrong current or state: they don\'t coincide'), "red", ["reverse"])
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


def get_regex(format, lang):
    '''Get regex and regex_explained for TAInput.'''
    if format == 'extended':
        if lang == 'it':
            regex="^muovi disco \d{1,1000} dal piolo [A-Z] al piolo [A-Z]$"
            regex_explained="muovi disco D dal piolo C al piolo T (dove D=DISCO, C=CORRENTE and T=OBIETTIVO)"
        else:
            regex="^move disk \d{1,1000} from [A-Z] peg to [A-Z] peg$"
            regex_explained="move disk D from C peg to T peg (where D=DISK, C=CURRENT and T=TARGET)"
    else:
        if lang == 'it':
            regex="^\d{1,1000}:[A-Z][A-Z]$"
            regex_explained="D:CT (where D=DISCO, C=CORRENTE and T=OBIETTIVO)"
        else:
            regex="^\d{1,1000}:[A-Z][A-Z]$"
            regex_explained="D:CT (where D=DISK, C=CURRENT and T=TARGET)"
    return (regex, regex_explained)


def get_formatted_move(move, format, lang):
    '''From <move> transform it a formatted string'''
    if format == 'extended':
        d, c, t = parse_move(move)
        if lang == 'it':
            return f'muovi disco {d} dal piolo {c} al piolo {t}'
        else:
            return f'move disk {d} from {c} peg to {t} peg'
    else:
        return move


def get_std_move(move, format, lang):
    '''From <move> transform it a standard string. E.g: 1:AB'''
    if format == 'extended':
        words = move.split()
        if lang == 'it':
            d = words[2]
            c = words[5]
            t = words[8]
        else:
            d = words[2]
            c = words[4]
            t = words[7]
        return generate_move(d, c, t)
    return move



# TESTS
if __name__ == "__main__":
    it_move = 'muovi disco 1 dal piolo A al piolo C'
    en_move = 'move disk 1 from A peg to C peg'
    std_move = '1:AC'

    assert get_std_move(it_move, 'extended', 'it') == '1:AC'
    assert get_std_move(en_move, 'extended', 'en') == '1:AC'
    assert get_std_move(std_move, 'minimal', 'it') == '1:AC'
    assert get_std_move(std_move, 'minimal', 'en') == '1:AC'

    assert it_move == get_formatted_move(std_move, 'extended', 'it')
    assert en_move == get_formatted_move(std_move, 'extended', 'en')
    assert std_move == get_formatted_move(std_move, 'minimal', 'it')
    assert std_move == get_formatted_move(std_move, 'minimal', 'en')