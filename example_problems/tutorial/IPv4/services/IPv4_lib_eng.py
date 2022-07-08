#!/usr/bin/env python3
# -*- coding:latin-1-*-

import random

from TALinputs import TALinput

def input_ip(TAc,LANG):
  ip=TALinput(str, num_tokens=4, regex="^((\d)+)$", TAc=TAc, sep='.')
  for tk in ip:
      if int(ip[i]) > 255:
          TAc.print(LANG.render_feedback("out-of-range_number_in_ip_address","\nERROR\nAll numbers in an IP address should belong to the closed interval [0,255]"), "red", ["bold"])
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
