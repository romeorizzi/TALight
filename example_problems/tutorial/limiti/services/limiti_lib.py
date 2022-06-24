#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fractions import Fraction
import numpy as np
import math
from sympy import *
from math import *
import random

correct = ['Bene!', 'Molto bene!', 'Corretto!', 'Ok!','Ben fatto!']
wrong=['Mmmm non sono molto sicuro che sia esatto, riprova:','Non credo che sia corretto, ritenta:','Prova a ricontrollare, ritenta:']
end=['Alla prossima!', 'E\' stato un piacere, alla prossima!']

def instance_to_array(input_str):
    instance_str=input_str.split(", ")
    return instance_str

def instance_to_number(instance_str):
    instance = list(map(eval, instance_str))
    return instance

def instance_randgen(set_cardinality:int,seed:int):
    assert set_cardinality>0
    instance_constants=['e','pi']
    instance_functions=['cos','sin','sqrt']
    random.seed(seed)
    instance = []
    integer=(set_cardinality//2)//2
    decimal=set_cardinality//2 - integer
    fraction=(set_cardinality-integer-decimal)//2
    math_constants=(set_cardinality-integer-decimal-fraction)//2
    math_functions=set_cardinality-integer-decimal-fraction-math_constants
    for i in range (integer):
        random.seed(seed+i)
        instance.append(str(random.randint(-20,20)))
    for i in range (decimal):
        random.seed(seed+i)
        instance.append(format(random.uniform(-20,20), '.2f'))
    for i in range (fraction):
        random.seed(seed+i)
        instance.append(str(random.randint(-70,70))+'/'+str(random.randint(2,15)))
    for i in range (math_constants):
        random.seed(seed+i)
        instance.append(random.choice(instance_constants)+'*'+str(random.randint(2,5)))
    for i in range (math_functions):
        random.seed(seed+i)
        funct=random.choice(instance_functions)
        instance.append(funct+'('+(str(random.randint(3,400))if funct=='sqrt' else 'pi'+'*'+str(random.randint(1,11))+'/'+str(random.randint(1,6)))+')')
    random.shuffle(instance)
    return instance


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

def disequazione():
    a = float(input("inserire a: "))
    b = float(input("inserire b: "))
    c = float(input("inserire c: "))
    if a == 0:
        if b == 0:
            print('no benee')
            return('Input non valido')
        else:
            if c == 0:
                if b>0:
                    return("x > 0")
                else:
                    return("x < 0")
            else:
                if b>0:
                    return("x > " + str(-c/b))
                else: 
                    return("x < " + str(-c/b))
    else:
        delta = b**2 - (4*a*c)
        print("La disequazione da risolvere e': ", a, "x^2 +", b, "x +", c, "> 0")
        if delta < 0 and a > 0:
            return ("La soluzione e' l'insieme dei numeri R")
        elif delta < 0 and a < 0:
            return("La soluzione in R e' l'insieme vuoto")
        elif delta >= 0 and a > 0:
            x1 = ((-b) + math.sqrt(delta))/(2*a)
            x2 = ((-b) - math.sqrt(delta))/(2*a)
            print("La soluzione e' l'intervallo esterno delle radici\n")
            if x1 < x2:
                return("x < " + str(x1) + " e x > " + str(x2))
            else:
                return("x < " + str(x2) + " e x > " + str(x1))
        elif delta >= 0 and a < 0:
            print("La soluzione e' nell'intervallo interno tra le radici\n")
            x1 = ((-b) + math.sqrt(delta))/(2*a)
            x2 = ((-b) - math.sqrt(delta))/(2*a)
            if x1 > x2:
                return(" "+ str(x2) + " < x < "+str(x1))
            else:
                return(" "+ str(x1) + " < x < "+str(x2))
