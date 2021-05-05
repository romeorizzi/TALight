#!/opt/virtualenvs/python3/bin/python
import sys
import random

def num_permutazioni(n):
  """ritorna il numero di permutazioni di n oggetti"""
  if n==0:
    return 1
  else:
    return n*num_permutazioni(n-1)

def num_permutazioni2(n):
  """ritorna il numero di permutazioni di n oggetti"""
  if n==0:
    return 1
  risp=0
  for first in range(n):
    risp += num_permutazioni2(n-1)
  return risp

def stampa_permutazioni(lista, history=""):
  """stampa una per riga le possibili permutazioni degli elementi in lista, ciascuna prefissata da history"""
  if len(lista)==0:
    print(history)
  for first in lista:
    lista_altri = [ele for ele in lista if ele != first]
    stampa_permutazioni(lista_altri, history+" "+first)

def genera_le_permutazioni1(lista, history=""):
  """generatore ricorsivo per la lista delle possibili permutazioni degli elementi in lista. Il contratto della ricorsione e di generare le permutazioni prfissando ciascuna di esse con gli elementi in history"""
  if len(lista)==0:
    yield history
  for first in lista:
    lista_altri = [ele for ele in lista if ele != first]
    for perm in genera_le_permutazioni1(lista_altri, history+" "+first):
        yield perm


def genera_le_permutazioni(lista):
  """generatore ricorsivo per la lista delle possibili permutazioni degli elementi in lista. Il contratto della ricorsione e di generare le permutazioni prefissando ciascuna di esse con gli elementi in history"""
  if len(lista)==0:
    yield ""
  for first in lista:
    lista_altri = [ele for ele in lista if ele != first]
    for perm in genera_le_permutazioni(lista_altri):
        yield first + " " + perm



def rank_permutazione(perm, lista):
  """restituisco la posizione in cui la permutazione <perm> si trovi collocata entro la lista delle permutazioni degli elementi di lista. Le posizioni partono da 0."""
  pass

def unrank_permutazione(rank, lista, history=""):
  """restituisco la permutazione in posizione rank tra le permutazioni degli elementi in lista, ciascuna prefissata da history"""
  assert 0 <= rank < num_permutazioni(len(lista))
  #print(f"rank={rank}, lista={lista}")
  if len(lista)==0:
    return history
  for first in lista:
    if rank < num_permutazioni(len(lista) -1):
      lista_altri = [ele for ele in lista if ele != first]
      return unrank_permutazione( rank, lista_altri, history+" "+first)
    else:
      rank -= num_permutazioni(len(lista) -1)

# un primo esempio di generator (si veda più sotto per il suo utilizzo come iterator)
def permutazione_random(lista):
  while len(lista) > 0:
    ele = random.choice(lista)
    lista = [e for e in lista if e != ele]
    yield ele


lista = ['A', 'B', 'C', 'D']
print(num_permutazioni(len(lista)))
stampa_permutazioni(lista)

print(num_permutazioni(len(lista)))
for i in range(num_permutazioni(len(lista))):
  print(unrank_permutazione(i, lista))

# WITH REPETITIONS POSSIBLE:
print(f"primo esempio di scelta random con distribuzione uniforme, CON REINSERIMENTO, dalla lista={lista}:")
print(random.choices(lista, weights=None, k=3))

# WITH NO REPETITION:
print(f"primo esempio di scelta random con distribuzione uniforme, SENZA REINSERIMENTO, dalla lista={lista}:")
print(random.sample(lista, k=3))

# WITH REPETITIONS POSSIBLE:
print("stampiamo 4 permutazioni scelte a caso (con ripetizione)")
for rank in random.choices(range(num_permutazioni(len(lista))), weights=None, k=4):
    print(unrank_permutazione(rank, lista))

# WITH NO REPETITION:
print("stampiamo 4 permutazioni scelte a caso (senza ripetizione)")
for rank in random.sample(range(num_permutazioni(len(lista))), k=4):
    print(unrank_permutazione(rank, lista))

# PRIMO ESEMPIO DI USO DI UN ITERATORE PRODOTTO DA UN GENERATORE:
print(f"Ora (primo esempio d'uso di un iteratore da noi costruito implementando un generator) stampo uno ad uno gli elementi di una permutazione random di {lista}")
for e in permutazione_random(lista):
  print(e,end = " ")
print()

# ORA IMPIEGHIAMO L'ESEMPIO DI GENERATORE RICORSIVO:
print(f"Ora (esempio d'uso di un iteratore da noi costruito implementando un generator ricorsivo) stampo uno ad uno gli elementi di una permutazione random di {lista}")
for p in genera_le_permutazioni1(lista, history=""):
    print(p)

print("sopra era una versione ibrida che voleva evidenziare come la struttura fosse la stessa che quella dell'unranking. Next l'ultima versione")
for p in genera_le_permutazioni(lista):
    print(p)

