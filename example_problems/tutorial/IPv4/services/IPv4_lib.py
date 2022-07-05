#!/usr/bin/env python3
from os import supports_bytes_environ
import random
from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang



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

#bisogna cancellare tutto quanto
#è tutto sbagliato
#def list_all(numeroIndirizzoInternet):
  ip=input("Enter all IPs address belonging to the network address:\n")
  numeriIP=[]
  numeri=[]
  numeroIndirizzoIp=0
  numeroIndirzzoInternet= ip.split(".")
  for i in range (len(numeroIndirzzoInternet)) :
    numeri.append( int(numeroIndirzzoInternet[i]))
  separetedStrings= ip.split(".")
  for i in range (len(separetedStrings)) :
    numeriIP.append( int(separetedStrings[i]))
  for i in range (256): 
    while numeri[0]!=numeriIP[0] or numeri[1]!=numeriIP[1] or numeri[2]!=numeriIP[2] or numeriIP[3]!=numeroIndirizzoIp:
      print("ERRORE\nRIPORVA\nRicorda di inserire gli indirizzi in ordine crescente: ")
      ip=input()
      separetedStrings = ip.split(".")
      numeriIP=[]
      for g in range (len(separetedStrings)) :
        numeriIP.append( int(separetedStrings[g]))
    print("RIGTH\n\n")
    ip=input("Enter a IP address: ")
    numeriIP=[]
    separetedStrings= ip.split(".")
    for f in range (len(separetedStrings)) :
        numeriIP.append( int(separetedStrings[f]))
    numeroIndirizzoIp+=1   