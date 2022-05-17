#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import math

def alfabeto(variable):
    for word in {'sqrt','log','pow','factorial','exp','cos','sin','tan','acos','asin','atan','pi','e','inf'}:
        if word in variable:
            variable=variable.replace(word,'math.'+word)
    if '^' in variable:
        variable=variable.replace('^','**')
    return variable

def get_file_str_from_path(path):
    """Returns the contents of the file as a string from the selected path."""
    file=open(path, 'r')
    return file.read()

def get_instance_from_txt(instance):
    istanza=instance.split('\n')
    function=istanza[0]
    x_0=istanza[1]
    c=istanza[2]
    return function,x_0,c

def x_0_infinito(x_0,eps_N):
    M = input('\nInserisci il tuo valore per M: ')
    M=alfabeto(M)
    M = eval(M,{"epsilon":eps_N,"N":eps_N,"math":math})
    assert M > 0, "Hai inserito una M negativa!"
    start_end_point=M+0.000000000000001
    intervallo= np.linspace(start_end_point, 1000, 3000) if x_0=='inf' else np.linspace(-1000, -start_end_point, 3000)
    return M,intervallo

def x_0_finito(x_0,eps_N):
    delta = input('\nInserisci il tuo valore per delta: ')
    delta=alfabeto(delta)
    print(delta)
    delta = eval(delta,{"epsilon":eps_N,"N":eps_N,"math":math})
    assert delta > 0, "Hai inserito un delta negativo!"
    intervallo= np.linspace(x_0-delta, x_0+delta, 50)
    return delta, intervallo