#!/usr/bin/env python3
from typing import List, Dict, Tuple

def display_matrix(M, rlabels=None, clabels=None):
    import numpy as np
    import pandas
    x = np.array(M)
    return pandas.DataFrame(x, columns=clabels, index=rlabels)

def matrix2markdown(rows, rlabels=None, clabels=None):
    from pandas import DataFrame
    from tabulate import tabulate
    dict = {"": rlabels}
    for label,j in zip(clabels,range(len(clabels))):
        dict[label] = [ rows[i][j] for i in range(len(rows))]
    df = DataFrame(dict).set_index("")
    return tabulate(df, tablefmt="pipe", headers="keys")


def description2markdown(description_as_yaml:List[List]):
    markdown_str = ''
    for spec,content in description_as_yaml:
        if spec == 'string2markdown':
            markdown_str += content + "  \n" 
        elif spec == 'fstring2markdown':
            markdown_str += eval(f"f'{content}'") + "  \n" 
        elif spec == 'display_table':
            markdown_str += '\n' + matrix2markdown(rows=content['Matrix'], rlabels=content['rlabels'], clabels=content['clabels']) + "  \n"
    return markdown_str


if __name__ == "__main__":
    A=[[1,2,3],[4,5,6]]
    d = display_matrix(A, rlabels=['gatti','cani'], clabels=['uomini','topi','elefanti'])
    print(d)

# Outputs:
#        uomini  topi  elefanti
# gatti       1     2         3
# cani        4     5         6

# Next we see how to print out this data as a Markdown table:
    CapacityMax= 36 
    labels= ['A','B','C','D','E','F','G','H','I','L','M','N'] 
    costs=  [ 15, 16, 17, 11, 13,  5,  7,  3,  1, 12,  9,  7] 
    vals=   [ 50, 52, 54, 40, 45, 17, 18,  7,  8, 42, 30, 22]                                                                    
# in the context, when translating from .instance to .yaml, of interpreting the following yaml string:
    yaml = {'description_0': [{'markdown':"In ogni richiesta del presente esercizio lo zaino disponibile avrà capienza al più $CapacityMax$ = __{CapacityMax}__  e dovrai scegliere quali prendere da un sottoinsieme degli oggetti con nome, peso e valore come da seguente tabella:"},{'display_table':{'rlabels':['peso','val'],'clabels':labels,'Mat':[costs,vals]}}] }

# Starting from:

    clabels = ['A','B','C','D','E','F','G','H','I','L','M','N']
    rlabels = ['peso','val']
    rows = [[15,  16, 17, 11, 13,  5,  7,  3,  1, 12,  9,  7],
            [ 50, 52, 54, 40, 45, 17, 18,  7,  8, 42, 30, 22]]

    print(matrix2markdown(rows, rlabels, clabels))

# Outputs:
# |      |   A |   B |   C |   D |   E |   F |   G |   H |   I |   L |   M |   N |
# |:-----|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|
# | peso |  15 |  16 |  17 |  11 |  13 |   5 |   7 |   3 |   1 |  12 |   9 |   7 |
# | val  |  50 |  52 |  54 |  40 |  45 |  17 |  18 |   7 |   8 |  42 |  30 |  22 |
#
# which is what we want!

# now starting from:

    description_0 = [['fstring2markdown',"In ogni richiesta del presente esercizio lo zaino disponibile avrà capienza al più $CapacityMax$ = __{CapacityMax}__  e dovrai scegliere quali prendere da un sottoinsieme degli oggetti con nome, peso e valore come da seguente tabella:"],['display_table',{'rlabels':['peso','val'],'clabels':labels,'Matrix':[costs,vals]}]]
    # which offers the general description that shoul be placed just before task 0+1 (it is also possible that no task will follow, which means that this offers a concusion)


    print(description2markdown(description_0))

# Outputs:
# In ogni richiesta del presente esercizio lo zaino disponibile avrà capienza al più $CapacityMax$ = __33__  e dovrai scegliere quali prendere da un sottoinsieme degli oggetti con nome, peso e valore come da seguente tabella:  
# 
# |      |   A |   B |   C |   D |   E |   F |   G |   H |   I |   L |   M |   N |
# |:-----|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|
# | peso |  15 |  16 |  17 |  11 |  13 |   5 |   7 |   3 |   1 |  12 |   9 |   7 |
# | val  |  50 |  52 |  54 |  40 |  45 |  17 |  18 |   7 |   8 |  42 |  30 |  22 |  
