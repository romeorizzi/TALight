#!/usr/bin/env python3

def display_matrix(M, rlabels=None, clabels=None):
    import numpy as np
    import pandas
    x = np.array(M)
    return pandas.DataFrame(x, columns=clabels, index=rlabels)

if __name__ == "__main__":
    A=[[1,2,3],[4,5,6]]
    d = display_matrix(A, rlabels=['gatti','cani'], clabels=['uomini','topi','elefanti'])
    print(d)
