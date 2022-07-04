#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from asyncio import constants
from fractions import Fraction
from re import X
from unicodedata import decimal
import numpy as np
import math
from scipy import rand
from sympy import *
from math import *
import random
import decimal
correct = random.choice(['Bene!', 'Molto bene!', 'Ok!','Ottimo!'])
wrong=['Mmmm non sono molto sicuro che sia esatto, riprova:','Non credo che sia corretto, ritenta:','Prova a ricontrollare, ritenta:']
end=['Alla prossima!', 'E\' stato un piacere, alla prossima!']

def indices(stringa,n,source):
    indices=set()
    if 'sottoinsieme' in stringa:
        posiz_start=stringa.find("sottoinsieme")+13
        comma_position=stringa.find(',')
        parenthesis_position=stringa.find(')')
        start=eval(stringa[posiz_start:comma_position],{'n':n})
        end=eval(stringa[comma_position+1:parenthesis_position],{'n':n})
        for i in range(start,end+1):
            indices.add(i)
    elif 'confronto' in stringa:
        def elem(indices,argument,n,source):
            if source=='random':
                if len(argument)==2 and argument[0]=='s' and argument[1].isdigit() and int(argument[1])<=n:
                    indices.add(int(argument[1]))
                else:
                    indices.add(str(argument))
            elif source=='generic':
                if argument=='s1' or argument=='sn':
                    indices.add(eval(argument[1],{'n':n}))
                else:
                    try:
                        eval_argument=eval(argument,{'n':n})
                        indices.add(eval_argument)
                    except:
                        indices.add(argument)
        posiz_1=stringa.find("confronto")+10
        comma_position=stringa.find(',')
        arg_1=stringa[posiz_1:comma_position]
        # posiz_1=stringa.find("confronto")+11
        elem(indices,arg_1,n,source)
        parenthesis_position=stringa.find(')')
        arg_2=stringa[comma_position+1:parenthesis_position]
        elem(indices,arg_2,n,source)
    return indices

def get_instance_from_txt(instance_as_str):
    """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
    instance = list()
    lines = instance_as_str.split('\n')
    for line in lines:
        if len(line) != 0:
            instance.append(line)
    return instance

def instance_to_array(input_str):
    instance_str=input_str.split('\n')
    return instance_str

def instance_to_number(instance_str):
    instance = list(map(eval, instance_str))
    return instance

def instance_randgen(set_cardinality:int,reference_set:str,seed:int):
    assert set_cardinality>0
    random.seed(seed)
    instance = []
    if reference_set=='natural':
        instance= random.sample(range(50),set_cardinality)
    else:
        assert reference_set=='decimal'
        for i in range (set_cardinality):
            random.seed(seed+i)
            instance.append(format(random.uniform(-50,50), '.2f'))
    return instance

def instance_archimede(seed:int):
    random.seed(seed)
    decimal_number=float(format(random.random(),'.4f'))
    coefficient=format(decimal_number,'.2f')
    instance_constant=random.choice(['e','pi'])
    instance_function=random.choice(['cos','sin','sqrt'])
    constant=coefficient+'*'+instance_constant
    num=random.randint(1,4)
    den=num*2+random.randint(1,4)
    sin_cos_sqrt=(instance_function+'('+str(random.randint(2,100))+')/'+str(random.choice([10,100])))if instance_function=='sqrt' else (instance_function+'(pi'+'*'+str(num)+'/'+str(den)+')')
    final_choice=random.choice([decimal_number,constant,sin_cos_sqrt])
    return final_choice

def instance_density(seed:int):
    random.seed(seed)
    x=decimal.Decimal(str(round(random.random()*random.randint(2,20),4)))
    aggiunta=decimal.Decimal(str(round(random.uniform(0,1)/random.choice([1,10]),4)))
    y=decimal.Decimal(str(round(x+aggiunta,4)))
    return x,y


def instance_inf_set(seed:int):
    random.seed(seed)
    diseq_grater=random.choice(['>','>='])
    parameter=True if seed<350000 else False
    # parameter=False
    if parameter:
        m=random.randint(1,5)
        cond_1=random.choice([str(m)+'*k', str(m)+'*k+1'])
        x=random.randint(5,200)
        k=random.randint(7,15)
        x_min='x'+str(x) if '=' in diseq_grater else 'x'+str(x+1)
        k_min='k'+str(k) if '=' in diseq_grater else 'k'+str(k+1)
        cond_2=random.choice([['x'+diseq_grater+str(x), x_min], ['k'+diseq_grater+str(k),k_min]])
        condition='x='+cond_1+', '+cond_2[0]
        instance='{x | '+condition+'  k in N}'
        return ('parameter',instance, cond_1, cond_2[1])
    else:
        diseq_less=random.choice(['<','<='])
        diseq_less_1=random.choice(['<','<='])
        diseq=random.choice([diseq_grater,diseq_less])
        def max_sup(x,x_inf,x_sup):
            if diseq in diseq_less:
                max_1=x if '=' in diseq else None
                sup_1=x
            else:
                max_1=None
                sup_1=np.inf
            max_2=x_sup if '=' in diseq_less_1 else None
            sup_2=x_sup
            min_2=x_inf if '=' in diseq_less else x_inf+0.00000000000001
            return max_1,sup_1,max_2,sup_2,min_2
        linear=random.choice([True,False])
        if linear:
            power=1
            x=random.randint(-30,30)
            x_inf=random.randint(-50,50)
            x_sup=x_inf+random.randint(2,30)
            max_1,sup_1,max_2,sup_2, min_2=max_sup(x,x_inf,x_sup)
            condition=random.choice([['x'+diseq+str(x), max_1,sup_1], [str(x_inf)+diseq_less+'x'+diseq_less_1+str(x_sup), max_2,[min_2,sup_2]]])
        else:
            power=random.randint(2,3)
            variable='x^'+str(power)
            x=random.randint(-10,10)
            x_inf=random.randint(1,5)
            x_sup=x_inf+random.randint(2,5)
            max_1,sup_1,max_2,sup_2,min_2=max_sup(x,x_inf,x_sup)
            if power==2:
                sup_2=abs(sup_2)
                if max_1!=None:
                    max_1=abs(max_1)
                if max_2!=None:
                    max_2=abs(max_2)
            if sup_1!=np.inf and power==2:
                sup_1=abs(sup_1)
                min_1=-sup_1
            else:
                min_1=None
            condition=random.choice([[variable+diseq+str(x**power),max_1,[min_1,sup_1]], [str(x_inf**power)+diseq_less+variable+diseq_less_1+str(x_sup**power), max_2, [min_2,sup_2]]])
        instance='{x in R | '+condition[0]+'}'
        return ('without_parameter'+str(power),instance, condition[1], condition[2])


def instance_randgen_1(seed:int):
    random.seed(seed)
    diseq_grater=random.choice(['>','>='])
    diseq_less=random.choice(['<','<='])
    diseq_less_1=random.choice(['<','<='])
    diseq=random.choice([diseq_grater,diseq_less])
    parameter=random.choice([True,False])
    # parameter=False
    if parameter:
        m=random.randint(1,5)
        cond_1=random.choice([str(m)+'*k', str(m)+'*k+1'])
        x_sup=random.randint(5,200)
        k_inf=random.randint(1,5)
        k_sup=random.randint(7,15)
        if diseq in diseq_less:
            x_min=0
            k_min=0
            k_max_1='k'+str(k_sup) if '=' in diseq else 'k'+str(k_sup-1)
            x_max_1='x'+str(x_sup) if '=' in diseq else 'x'+str(x_sup-1)
        else:
            x_min='x'+str(x_sup) if '=' in diseq else 'x'+str(x_sup+1)
            k_min='k'+str(k_sup) if '=' in diseq else 'k'+str(k_sup+1)
            x_max_1=None
            k_max_1=None
        min_k=k_inf if '=' in diseq_less_1 else k_inf+1
        k_max_2='k'+str(k_sup) if '=' in diseq_less_1 else 'k'+str(k_sup-1)

        cond_2=random.choice([['x'+diseq+str(x_sup), [x_min,x_max_1]], ['k'+diseq+str(k_sup),[k_min,k_max_1]], [str(k_inf)+diseq_less_1+'k'+diseq_less_1+str(k_sup),[min_k,k_max_2]]])
        condition='x='+cond_1+', '+cond_2[0]
        instance='{x | '+condition+'  k in N}'
        return ('parameter',instance, cond_1, cond_2[1])
    else:
        def max_sup(x,x_inf,x_sup):
            if diseq in diseq_less:
                max_1=x if '=' in diseq else None
                sup_1=x
            else:
                max_1=None
                sup_1=np.inf
            max_2=x_sup if '=' in diseq_less_1 else None
            sup_2=x_sup
            min_2=x_inf if '=' in diseq_less else x_inf+0.00000000000001
            return max_1,sup_1,max_2,sup_2,min_2
        linear=random.choice([True,False])
        if linear:
            x=random.randint(-30,30)
            x_inf=random.randint(-50,50)
            x_sup=x_inf+random.randint(2,30)
            max_1,sup_1,max_2,sup_2, min_2=max_sup(x,x_inf,x_sup)
            condition=random.choice([['x'+diseq+str(x), max_1,sup_1], [str(x_inf)+diseq_less+'x'+diseq_less_1+str(x_sup), max_2,[min_2,sup_2]]])
        else:
            power=random.randint(2,3)
            variable='x^'+str(power)
            x=random.randint(-10,10)
            x_inf=random.randint(1,5)
            x_sup=x_inf+random.randint(2,5)
            max_1,sup_1,max_2,sup_2,min_2=max_sup(x,x_inf,x_sup)
            if power==2:
                min_2='pow2'+str(min_2)
                sup_2=abs(sup_2)
                if max_1!=None:
                    max_1=abs(max_1)
                if max_2!=None:
                    max_2=abs(max_2)
            if sup_1!=np.inf and power==2:
                sup_1=abs(sup_1)
                min_1=-sup_1
            else:
                min_1=None
            condition=random.choice([[variable+diseq+str(x**power),max_1,[min_1,sup_1]], [str(x_inf**power)+diseq_less+variable+diseq_less_1+str(x_sup**power), max_2, [min_2,sup_2]]])
        instance='{x in R | '+condition[0]+'}'
        return ('without_parameter',instance, condition[1], condition[2])

def find_max_with_parameter(condition,max):
    if max!=None:
        if max[0]=='k':
            x_max=eval(condition, {"k": int(max[1:])})
        else:
            i=0
            k_max=int(max[1:])
            k_max=(int(max[1:])-1)/int(condition[0]) if '+' in condition else int(max[1:])/int(condition[0])
            while not k_max.is_integer():
                i+=1
                k_max=int(max[1:])-i
                k_max=(k_max-1)/int(condition[0]) if '+' in condition else k_max/int(condition[0])
            x_max=eval(condition,{'k':k_max})
        return x_max


# TUTTE QUESTE FUNZIONI SOTTO DA RIFARE/ELIMINARE

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

# def get_instance_from_txt(instance):
#     istanza=instance.split('\n')
#     function=istanza[0]
#     x_0=istanza[1]
#     c=istanza[2]
#     return function,x_0,c

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

def disequazione(): # funzione da riguardare
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
