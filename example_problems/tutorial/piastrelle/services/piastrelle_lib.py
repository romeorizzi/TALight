#!/usr/bin/env python3

def num_sol(n):
    if n==1:
        return 1
    if n==2:
        return 2
    solu=num_sol(n-1)+num_sol(n-2)
    return solu

# def unrank(n, pos, sorting_criterion="loves_long_tiles"):
    
#     return "(" + unrank(n_in_A, (pos-count) // num_B) + ")" + unrank(n - n_in_A -1, (pos-count) % num_B)
def unrank(n):
    if num_sol(n)==1:
        return ['[]']
    if num_sol(n)==2:
        return ['[][]', '[--]']
    solu1=[]
    solu2=[]
    for i in range(num_sol(n-1)):
        solu1.append('[]' + unrank(n-1)[i])
    for j in range(num_sol(n-2)):
        solu2.append('[--]' + unrank(n-2)[j])
    return solu1 + solu2


def recognize(tiling, TAc, LANG):
    #print(f"tiling={tiling}")

    pos = 0
    n_tiles = 0
    char = None
    while pos < len(tiling):
        if tiling[pos] != '[':
            TAc.print(tiling, "yellow", ["underline"])
            TAc.print(LANG.render_feedback("wrong-tile-opening", f'No. The tile in position {n_tiles+1} does not start with "[" (it starts with "{tiling[pos]}" instead). Your tiling is not correctly encoded.'), "red", ["bold"])
            return False
        n_tiles += 1
        if tiling[pos+1] == ']':
            pos += 2
        else:
            if pos+3 < len(tiling) and tiling[pos+3] != ']':
                TAc.print(tiling, "yellow", ["underline"])
                TAc.print(LANG.render_feedback("wrong-tile-closing", f'No. The tile in position {n_tiles}, starting with {tiling[pos:pos+3]}, does not end wih "]" (it ends with "{tiling[pos+3]}" instead). Your tiling is not correctly encoded.'), "red", ["bold"])
                return False
            for pos_fill in {pos+1,pos+2}:
                if tiling[pos_fill] in {'[',']'}:
                    TAc.print(tiling, "yellow", ["underline"])
                    TAc.print(LANG.render_feedback("wrong-tile-filling", f'No. The tile in position {n_tiles}, starting with {tiling[pos:pos+4]}, has a forbidden filling character (namely, "{tiling[pos_fill]}"). Your tiling is not correctly encoded.'), "red", ["bold"])
                    return False
            pos += 4
    return True




