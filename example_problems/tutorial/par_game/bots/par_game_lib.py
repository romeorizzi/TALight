#!/usr/bin/env python3
import random

def recognize(formula_of_parentheses, TAc, LANG, error_feedback=True):
    """If the input formula is well formed then return True.
       Otherwise return false and, if error_feedback=True, then explain in full where the problem is."""
    assert type(formula_of_parentheses)==str
    num_dangling_open = 0
    for char, i in zip(formula_of_parentheses,range(1,len(formula_of_parentheses)+1)):
        if char == '(':
            num_dangling_open += 1
        else:
            if num_dangling_open == 0:
                if error_feedback:
                    TAc.print(LANG.render_feedback("not-well-formed-formula", "We have a problem. The following formula in not well formed:"), "red", ["bold"])
                    TAc.print(formula_of_parentheses, "yellow", ["underline"])
                    TAc.print(LANG.render_feedback("unfeasible", f"Indeed on position {i} there is no open parenthesis left to be closed:", {'i': i}), "red", ["bold"])
                    TAc.print(formula_of_parentheses, "yellow", ["underline"])
                    print(" "*(i-1),end="")
                    TAc.print(LANG.render_feedback("pointer", '^ unmatched ")"'), "yellow", ["underline"])
                return False
            num_dangling_open -= 1

    if num_dangling_open > 0:
        if error_feedback:
            TAc.print(LANG.render_feedback("not-well-formed-formula", "We have a problem. The following formula in not well formed:"), "red", ["bold"])
            TAc.print(formula_of_parentheses, "yellow", ["underline"])
            TAc.print(LANG.render_feedback("unfinished", f"Indeed {num_dangling_open} open parenthesis are left unclosed. The formula contains more '(' than ')' characters.", {'num_dangling_open': num_dangling_open}), "red", ["bold"])
        return False
    return True

def init_string(length):
    gen_s=''
    for _ in range(length):
        gen_s+='_'
    return gen_s

def reinit_string(gen_s):
    length=len(gen_s)
    gen_s=''
    for _ in range(length):
        gen_s+='_'
    return gen_s

def generate_string(gen_s):
    length=len(gen_s)
    is_not_ok=True
    parenthesis=['(',')']
    while is_not_ok:
        gen_s=reinit_string(gen_s)
        for _ in range(length):
            gen_s=gen_s.replace('_', random.choice(parenthesis), 1)
        is_not_ok=not recognize(gen_s,None,None,False)
    return gen_s

def random_wff(length):
    if length==0:
        return ''
    if length%2!=0:
        return None
    gen_s=init_string(length)
    gen_s=generate_string(gen_s)
    return gen_s

def verify_char(wff):
    for c in wff:
        if c!='(' and c!=')':
            return False
    return True

def find_friend_open(wff, base=0):
    if wff[base]==')':
        return None
    level=0
    for index in range(base+1, len(wff)):
        if wff[index]==')' and level==0:
            return index
        elif wff[index]=='(':
            level+=1
        elif wff[index]==')' and level>0:
            level-=1

def find_friend_close(wff, base=0):
    if wff[base]=='(' or base>len(wff):
        return None
    level=0
    for index in range(base-1, -1, -1):
        if wff[index]=='(' and level==0:
            return index
        elif wff[index]==')':
            level-=1
        elif wff[index]=='(' and level<0:
            level+=1

def find_all(string, substring):
    index=0
    indexes=[]
    while True:
        index=string.find(substring,index)
        if index==-1:
            return indexes
        indexes.append(index)
        index+=1

def find_move(wff):
    for index in range(len(wff)):
        if wff[index]=='(':
            index_friend=find_friend_open(wff, index)
            wff_remove=wff[index:index_friend+1]
            wff_part_first=wff[:index]
            wff_part_second=wff[index:]
            wff_final=wff_part_first+wff_part_second.replace(wff_remove, '', 1)
            if grundy_val(wff_final)==0:
                return wff_final

def find_moves(wff, rmv_dup=False):
    moves=[]
    for index in range(len(wff)):
        if wff[index]=='(':
            index_friend=find_friend_open(wff, index)
            wff_remove=wff[index:index_friend+1]
            wff_part_first=wff[:index]
            wff_part_second=wff[index:]
            wff_final=wff_part_first+wff_part_second.replace(wff_remove, '', 1)
            if grundy_val(wff_final)==0:
                moves.append(wff_final)
    if rmv_dup:
        moves=list(dict.fromkeys(moves))
    return moves

def find_all_moves(wff, rmv_dup=False):
    moves=[]
    for index in range(len(wff)):
        if wff[index]=='(':
            index_friend=find_friend_open(wff, index)
            wff_remove=wff[index:index_friend+1]
            wff_part_first=wff[:index]
            wff_part_second=wff[index:]
            wff_final=wff_part_first+wff_part_second.replace(wff_remove, '', 1)
            moves.append(wff_final)
    if rmv_dup:
        moves=list(dict.fromkeys(moves))
    return moves

def verify_moves(wff, new_wff):
    moves=find_all_moves(wff)
    for index,move in enumerate(moves):
        if move=='':
            moves[index]=')('
    for move in moves:
        if move==new_wff:
            return True
    return False

def computer_move(wff):
    if grundy_val(wff)==0:
        return random.choice(find_all_moves(wff, True))
    return find_move(wff)

def grundy_val(wff):
    if wff=='':
        return 0
    level=0
    wff_mod=wff.replace(')(',')^(')
    max_level=0
    for index in range(len(wff)):
        par=wff[index]
        if par=='(':
            if wff[index+1]==')':
                wff_mod=wff_mod.replace('()','1',1)
            elif wff[index+1]=='(':
                level+=1
                if max_level<level:
                    max_level=level
        elif par==')':
            level-=1
    for i in range(0, max_level+1):
        wff_mod=wff_mod.replace('('+str(i)+')', str(i+1))
    wff_mod=wff_mod.replace(')', ')+1')
    return eval(wff_mod)

# TESTS
if __name__ == "__main__":
    # GRUNDY-SPRAGUE THEORY FUNCTIONS:
    print('Test: grundy_val(wff)')
    wffs = ['()','(())','()(())','((()))','()((()))','()()','(()()(()))','()()()(())','(()()()()(()))','(()(())())', '((())()(()))','(())(()())','(()(())((())))','(()(())((())))(()(()))','(())()()(())(()())','(((((((((())))))))))','(((((())))))()','((((((())))))())','(())()((((((())))))())','()()(())()((((((())))))())()','(())()()(())()()(())','(())()()((())()()(())())','((())()()((())()()(())()))','(((((())))))(())','((((((())))))(()))']
    ref_values = [1,2,3,3,2,0,3,3,3,3,2,3,1,5,1,10,7,8,11,10,2,0,1,4,5]
    index=0
    for wff in wffs:
        #print(wff)
        #print(grundy_val(wff))
        assert recognize(wff,None,None,False)
        assert grundy_val(wff) == ref_values[index]
        index+=1
    print('==> OK')