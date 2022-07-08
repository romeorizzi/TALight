#!/usr/bin/env python3
# -*- coding:latin-1-*-

import random
from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

args_list=[]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')

def input_ip():
  ip=TALinput(int ,num_tokens=4, regex= f"regex: ^((\d)+)((\.)+)$ ", TAc=TAc ,sep='.')
  tooMuch=0
  for i in range(4):
    if ip[i]>255:
      tooMuch+=1

  if tooMuch>1:
    TAc.print("\nERROR\nIn an IP address the numbers range from a minimum of 0 to a maximum of 255 inclusive", "red", ["bold"])
    exit(0)
  
  return ip

def subnet_mask():
  """This function will generate, in a pseudo-random way, the subnet mask"""
  numeroSubNet=random.randint(1,3);
  subnet=""
  if numeroSubNet == 1:
    subnet="255.255.255.0"
    return subnet
  elif numeroSubNet == 2:
    subnet="255.255.0.0"
    return subnet
  else: 
    subnet="255.0.0.0"
    return subnet 
  

def net_address(subnet):
  """This function will generate, in a pseudo-random way, the network address"""
  n1=0
  n2=0
  n3=0
  n4=0
  numeri=[];
  separetedStrings= subnet.split(".");
  for i in range (len(separetedStrings)) :
    numeri.append( int(separetedStrings[i]))
    
  if numeri[0]==255 and numeri[1]==0:
    n1=random.randint(1,255)
  elif numeri[1]==255 and numeri[2]==0:
    n1=random.randint(1,255)
    n2=random.randint(1,255)
  else:
    n1=random.randint(1,255)
    n2=random.randint(1,255)
    n3=random.randint(1,255)
  numeroIndirizzoInternet=[n1,n2,n3,n4]  
  return numeroIndirizzoInternet
