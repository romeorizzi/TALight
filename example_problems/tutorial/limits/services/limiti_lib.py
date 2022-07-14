#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from re import X
from unicodedata import decimal
import numpy as np
from sympy import *
from math import *
import random
import decimal
from sympy import Symbol, symbols,solve

correct = random.choice(['Bene!', 'Molto bene!', 'Ok!','Ottimo!'])
wrong=['Mmmm non sono molto sicuro che sia esatto, riprova:','Non credo che sia corretto, ritenta:','Prova a ricontrollare, ritenta:']
end=['Alla prossima!', 'E\' stato un piacere, alla prossima!']
def args_confronto(stringa):
    posiz_1=stringa.find("confronto")+10
    comma_position=stringa.find(',')
    arg_1=stringa[posiz_1:comma_position]
    parenthesis_position=stringa.find(')')
    arg_2=stringa[comma_position+1:parenthesis_position]
    return arg_1,arg_2
def majorant(max_value):
    majorant=random.randint(max_value+1,max_value+random.randint(1,10))
    return majorant
def not_in_set_parameter(condition,max_value):
    not_in_set=random.randint(-10,60)
    my_k=(not_in_set-1)/int(condition[0]) if '+' in condition else (not_in_set)/int(condition[0])
    while (not_in_set>=max_value or my_k.is_integer()):
        not_in_set-=random.randint(1,3)
        my_k=(not_in_set-1)/int(condition[0]) if '+' in condition else (not_in_set)/int(condition[0])
    return not_in_set
def not_max_but_in_set_parameter(condition,max_value):
    not_max_but_in_set=random.randint(-10,60)
    my_k=(not_max_but_in_set-1)/int(condition[0]) if '+' in condition else (not_max_but_in_set)/int(condition[0])
    while (not_max_but_in_set>=max_value or not my_k.is_integer()):
        not_max_but_in_set-=random.randint(1,3)
        my_k=(not_max_but_in_set-1)/int(condition[0]) if '+' in condition else (not_max_but_in_set)/int(condition[0])
    return not_max_but_in_set
def non_appartiene_e_non_maggiorante(condition,min_value):
    non_maggiorante=random.randint(-10,60)
    my_k=(non_maggiorante-1)/int(condition[0]) if '+' in condition else (non_maggiorante)/int(condition[0])
    while (non_maggiorante<=min_value or my_k.is_integer()):
        non_maggiorante+=random.randint(1,3)
        my_k=(non_maggiorante-1)/int(condition[0]) if '+' in condition else (non_maggiorante)/int(condition[0])
    return non_maggiorante
def appartiene_ma_non_maggiorante(condition,min_value):
    non_maggiorante=random.randint(-10,60)
    my_k=(non_maggiorante-1)/int(condition[0]) if '+' in condition else (non_maggiorante)/int(condition[0])
    while (non_maggiorante<=min_value or not my_k.is_integer()):
        non_maggiorante+=random.randint(1,3)
        my_k=(non_maggiorante-1)/int(condition[0]) if '+' in condition else (non_maggiorante)/int(condition[0])
    return non_maggiorante
def appartiene_ma_non_maggiorante_without_parameter(power,min_value,sup_value):
    propose=random.randint(-20,30)
    if sup_value!=inf:
        if power==2:
            propose=abs(propose)
        if min_value!=None:
            while not (propose<sup_value and propose>min_value):
                if propose>=sup_value:
                    propose-=1
                elif propose<=min_value:
                    propose+=1
        else:
            while propose>=sup_value:
                propose-=1
    elif sup_value==inf:
        if power==2:
            propose=abs(propose)
            min_value=abs(min_value)
        while propose<=min_value:
            propose+=1
    return propose
def not_in_set_without_parameter_min(power,min_value,sup_value):
    propose=random.randint(-20,30)
    if sup_value!=inf:
        if power==2:
            propose=-abs(propose)
            sup_value=-abs(sup_value)
            while propose>=sup_value:
                propose-=1
        else:
            while propose>=min_value:
                propose-=1
    elif sup_value==inf:
        if power==2:
            propose=abs(propose)
            min_value=abs(min_value)
        while propose>=min_value:
            propose-=1
    return propose

def not_in_set_without_parameter_max(power,min_value,sup_value):
    propose=random.randint(-20,30)
    if power==2:
        propose=-abs(propose)
        sup_value=-abs(sup_value)
        while propose>=sup_value:
            propose-=1
    else:
        if min_value!=None:
            while propose>=min_value:
                propose-=1
        else:
            while propose>=sup_value:
                propose-=1
    return propose
def args_subset(stringa):
    posiz_start=stringa.find("max_in_sottoinsieme")+20
    comma_position=stringa.find(',')
    parenthesis_position=stringa.find(')')
    start=stringa[posiz_start:comma_position]
    end=stringa[comma_position+1:parenthesis_position]
    return start,end

def indices(stringa,n,source):
    indices=set()
    if 'max_in_sottoinsieme' in stringa:
        start,end=args_subset(stringa)
        for i in range(eval(start,{'n':n}),eval(end,{'n':n})+1):
            indices.add(i)
    elif 'confronto' in stringa:
        def elem(indices,argument,n,source):
            if source!='open':
                if argument.isdigit() or eval(argument,{'n':n})<=n:
                    indices.add(int(eval(argument,{'n':n})))
                else:
                    indices.add(str(argument))
            else:
                eval_argument=eval(argument,{'n':n})
                indices.add(eval_argument)

        arg_1,arg_2=args_confronto(stringa)
        elem(indices,arg_1,n,source)
        elem(indices,arg_2,n,source)
    return indices

def core_function_max_finite_set_proof(indices_list,user_command,checked_set,n,cardinality):
    command_index=indices(user_command,n,cardinality)
    # print(f'command index {command_index}')
    # print(f'indices list {indices_list}')
    position_command_indices=[]
    for item in command_index:
        position_command_indices.append(checked_set.index(item))
    indices_list.append(command_index)
    max_elem=checked_set[min(position_command_indices)]
    to_remove=set()
    new_index_set=set()
    for j in range(0,len(indices_list)-1):
        intersection=command_index & indices_list[j]
        # print(f'sto guardando {indices_list[j]}, con command index {command_index}')
        if bool(intersection):
            position_common_indices=[checked_set.index(item) for item in intersection]
            max_common=checked_set[min(position_common_indices)]
            position_j=[checked_set.index(item) for item in indices_list[j]]
            max_j=checked_set[min(position_j)]
            # print(f'max common {max_common} max j {max_j}')
            if checked_set.index(max_common)<=checked_set.index(max_elem) and checked_set.index(max_common)>=checked_set.index(max_j):
                new_index_set.update(command_index)
                new_index_set.update(indices_list[j])
                to_remove.add(j)
                to_remove.add(-1)
            elif checked_set.index(max_common)>checked_set.index(max_elem) and checked_set.index(max_common)==checked_set.index(max_j):
                new_index_set.update(indices_list[j])
                new_index_set.update(command_index)
                to_remove.add(j)
                to_remove.add(-1)
    if bool(to_remove):
        for i in to_remove:
            del indices_list[i]
    if bool(new_index_set):
        indices_list.append(new_index_set)
    # print(f'indices list {indices_list}')
    return indices_list,max_elem

def get_instance_from_txt(instance_as_str):
    """This function returns the instance it gets from its .txt string representation in format <instance_format_name>."""
    instance = list()
    lines = instance_as_str.split('\n')
    for line in lines:
        if len(line) != 0 and line[0]!='#':
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
    parameter=random.choice([True,False])
    diseq_less=random.choice(['<','<='])
    diseq=random.choice([diseq_grater,diseq_less])
    # parameter=False
    if parameter:
        m=random.randint(1,5)
        cond_1=random.choice([str(m)+'*k', str(m)+'*k+1'])
        x_val=random.randint(-30,60)
        k_val=random.randint(-10,10)
        if diseq in diseq_grater:
            ricerca_x_min=True
            x_for_min=x_val if '=' in diseq else x_val+1
            while ricerca_x_min:
                x_min_value=(x_for_min-1)/m if '+' in cond_1 else (x_for_min)/m
                ricerca_x_min=False if x_min_value.is_integer() else True
                x_for_min+=1
            x_for_min-=1
            x_min='x'+str(x_for_min)
            k_min='k'+str(k_val) if '=' in diseq else 'k'+str(k_val+1)
            x_max=None
            k_max=None
        else:
            ricerca_x_max=True
            x_for_max=x_val if '=' in diseq else x_val-1
            while ricerca_x_max:
                x_max_value=(x_for_max-1)/m if '+' in cond_1 else (x_for_max)/m
                ricerca_x_max=False if x_max_value.is_integer() else True
                x_for_max-=1
            x_for_max+=1
            x_max='x'+str(x_for_max)
            k_max='k'+str(k_val) if '=' in diseq else 'k'+str(k_val-1)
            x_min=None
            k_min=None
        cond_2=random.choice([['x'+diseq+str(x_val), [x_min,x_max]], ['k'+diseq+str(k_val),[k_min,k_max]]])
        condition='x='+str(cond_1)+', '+cond_2[0]
        instance='{x | '+condition+'  k in Z}'
        return ('parameter',instance, cond_1, cond_2[1])
    else:
        diseq_less_1=random.choice(['<','<='])
        def max_sup(x,x_inf,x_sup):
            if diseq in diseq_less:
                max_1=x if '=' in diseq else None
                sup_1=x
                min_1=None
            else:
                min_1=x_value if '=' in diseq else x_value+0.00000000000001
                max_1=None
                sup_1=np.inf
            max_2=x_sup if '=' in diseq_less_1 else None
            sup_2=x_sup
            min_2=x_inf if '=' in diseq_less else x_inf+0.00000000000001
            return max_1,sup_1,min_1,max_2,sup_2,min_2
        linear=random.choice([True,False])
        if linear:
            power=1
            x_value=random.randint(-30,30)
            x_inf=random.randint(-50,50)
            x_sup=x_inf+random.randint(2,30)
            max_1,sup_1,min_1,max_2,sup_2, min_2=max_sup(x_value,x_inf,x_sup)
            condition=random.choice([['x'+diseq+str(x_value), max_1,[min_1,sup_1]], [str(x_inf)+diseq_less+'x'+diseq_less_1+str(x_sup), max_2,[min_2,sup_2]]])
        else:
            power=random.randint(2,3)
            variable='x^'+str(power)
            x_value=random.randint(-10,10)
            x_inf=random.randint(1,5)
            x_sup=x_inf+random.randint(2,5)
            max_1,sup_1,min_1,max_2,sup_2,min_2=max_sup(x_value,x_inf,x_sup)
            if power==2:
                sup_2=abs(sup_2)
                if max_1!=None:
                    max_1=abs(max_1)
                if max_2!=None:
                    max_2=abs(max_2)
            if sup_1!=np.inf and power==2:
                sup_1=abs(sup_1)
                min_1=-sup_1

            condition=random.choice([[variable+diseq+str(x_value**power),max_1,[min_1,sup_1]], [str(x_inf**power)+diseq_less+variable+diseq_less_1+str(x_sup**power), max_2, [min_2,sup_2]]])
        instance='{x in R | '+condition[0]+'}'
        return ('without_parameter'+str(power),instance, condition[1], condition[2])

def find_max_with_parameter(condition,max):
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

def get_file_str_from_path(path):
    """Returns the contents of the file as a string from the selected path."""
    file=open(path, 'r')
    return file.read()

def inf_seq(seed:int):
    random.seed(seed)
    n=Symbol('n')
    # epsilon=Symbol('epsilon')
    n_coeff_1=random.randint(1,3)
    constant_term_1=random.randint(-3,4)
    n_coeff_2=random.randint(1,3)
    constant_term_2=random.randint(-3,4)
    num_1=expand(n_coeff_1*n+constant_term_1)
    num_2=expand(n_coeff_2*n+constant_term_2)
    numerator=random.choice([num_1,expand(num_1*num_2)])
    # num_roots_plus=solve(numerator+epsilon,n)
    # num_roots_minus=solve(numerator-epsilon,n)
    succ_type=random.choice(['poly','fract'])
    # succ_type='poly'
    if succ_type=='poly':
        inf_sequence=numerator
        # print('semplificato ',simplify(inf_sequence-epsilon))
        # print('soluz',solve(inf_sequence-epsilon,n))
    else:
        constant_term_3=random.randint(-3,4)
        den_1=expand(n_coeff_2*n+constant_term_3)
        if degree(numerator)==2:
            denominator=den_1
        else:
            den_2=expand(n_coeff_1*n+constant_term_3)
            denominator=random.choice([den_1,expand(den_1*den_2)])
        inf_sequence=numerator/denominator
        # den_root=solve(denominator,n)
    return inf_sequence