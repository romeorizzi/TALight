#!/usr/bin/python
"""una soluzione semplice, che non si preoccupa di rispettare il protocollo per il dialogo col manager della sottoposizione offerto dal servizio solve."""

MAXN = 100000
memo_risp = [None] * (MAXN+1)
memo_risp[0] = memo_risp[1] = 1

for n in range(2,MAXN+1):
  memo_risp[n] = memo_risp[n - 1] + memo_risp[n - 2]

def num_piastrellature(n):
  assert n >= 0
  return memo_risp[n]
  
def rank_piastrellatura(n, p):
  "restituisce il rank della piastrellatura p di un bagno di dimensione n"
  assert n >= 0
  assert len(p)==3*n
  if n==0:
    assert p == ""
    return 0;
  if n==1:
    assert p == "[-]"
    return 0;
  if p[:3] == "[-]":
    return rank_piastrellatura(n-1, p[3:]);
  elif p[:6] == "[----]":
    return num_piastrellature(n-1)+rank_piastrellatura(n-2, p[6:]);
  else:
    assert(False)

def unrank_piastrellatura(n, rank, history=""):
  "restituisce la piastrellatura di rango rank tra le piastrellature di un bagno di dimensione n, prefissata da history"
  #print(f"called with {n=}, {rank=}, {history=}")
  assert n >= 0
  assert rank < num_piastrellature(n);
  if n == 0:
    return history
  elif n == 1:
    #return history+"[-]"
    return unrank_piastrellatura(n - 1, rank, history + "[-]")
  elif rank < num_piastrellature(n-1):
     return unrank_piastrellatura(n - 1, rank, history + "[-]")
  else:
     return unrank_piastrellatura(n - 2, rank-num_piastrellature(n-1), history + "[----]")



n = int(input("n="))
           print(f"Le piastrellature sono {num_piastrellature(n)}.")

r = int(input("r="))
piast = unrank_piastrellatura(n, r, "")
print(f'La {r}-esima piastrellatura di un bagno 1x{n} è {piast}');

print(f'{rank_piastrellatura(n, piast)=}');
