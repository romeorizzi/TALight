#!/usr/bin/env python3

def num_sol(n):
    # risps_correct[num_open][num_closed] = number of different prefixes of well-formed formula with <num_open> open parentheses and <num_closed> closed parentheses.
    risps_correct = [ [1] * (n+2) for _ in range(n+1)]
    for num_open in range(1,n+1):
        risps_correct[num_open][0] = risps_correct[num_open-1][1]
        for num_closed in range(1,n+1):
            risps_correct[num_open][num_closed] = risps_correct[num_open][num_closed-1] + risps_correct[num_open-1][num_closed+1]

    return risps_correct[n][0]

def unrank(n, pos, sorting_criterion="loves_opening_par"):
    if n == 0:
        return ""
    """(  ... )  ...
           A      B
    """    
    count = 0
    for n_in_A in range(n) if sorting_criterion=="loves_closing_par" else reversed(range(n)):
        num_A = num_sol(n_in_A)
        num_B = num_sol(n - n_in_A -1)
        if count + num_A*num_B > pos:
            break
        count += num_A*num_B
    return "(" + unrank(n_in_A, (pos-count) // num_B) + ")" + unrank(n - n_in_A -1, (pos-count) % num_B)


def recognize(tiling, TAc, LANG):
    #print(f"tiling={tiling}")

    pos = 0
    n_tiles = 0
    char = None
    while pos < len(tiling):
        if tiling[pos] != '[':
            TAc.print(tiling, "yellow", ["underline"])
            TAc.print(LANG.render_feedback("wrong-tile-opening", f'No. The tile in position {n_tiles} does not start with "[" (it starts with "{tiling[pos]}" instead). Your tiling is not correctly encoded.'), "red", ["bold"])
            return False
        n_tiles += 1
        if tiling[pos+1] == ']':
            pos += 2
        else:
            if tiling[pos+3] != ']':
                TAc.print(tiling, "yellow", ["underline"])
                TAc.print(LANG.render_feedback("wrong-tile-closing", f'No. The tile in position {n_tiles}, namely {tiling[pos:pos+4]}, does not end wih "]" (it ends with "{tiling[pos+3]}" instead). Your tiling is not correctly encoded.'), "red", ["bold"])
                return False
            for pos_fill in {pos+1,pos+2}
            if tiling[pos_fill] in {'[',']'}:
                TAc.print(tiling, "yellow", ["underline"])
                TAc.print(LANG.render_feedback("wrong-tile-filling", f'No. The tile in position {n_tiles}, namely {tiling[pos:pos+4]}, has a forbidden filling character (namely, "{tiling[pos_fill-pos]}"). Your tiling is not correctly encoded.'), "red", ["bold"])
                return False
            pos += 4
    return True
