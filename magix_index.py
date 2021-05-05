questions = 0
recursions = 0

def magix_index(array, l, u):
  global questions
  global recursions

  if l == u and l > 0:
    # ci chiediamo sempre se ho un elemento è un Magic index
    questions += 1
    if array[l] == l:        
        return [l]
    return []

  if l > u:
    return []

  #ci chiediamo sempre se il valore del lower è maggiore dell'indice del lower
  questions += 1
  if array[l] > l:
    return []

  #ci chiediamo sempre se il valore dell'upper è minore dell'indice dell'upper
  questions += 1
  if array[u] < u:
    return []

  #ci chiediamo sempre se i valori degli estremi sono uguali ai loro indici
  questions += 2
  if array[l] == l and array[u] == u:
    return array[l:u + 1]

  else:
    mid = (l + u) // 2

    #ci chiediamo sempre se l'elemento corrente 'smezzato' è mag del suo indice
    questions += 1
    if array[mid] > mid:      
      recursions += 1
      return magix_index(array, l, mid - 1)

    #ci chiediamo sempre se l'elemento corrente 'smezzato' è minore del suo indice 
    #(non serve sommare una question sotto nell'uguale perchè si va ad esclusione coi primi due)
    questions += 1
    if array[mid] < mid:
      recursions += 1
      return magix_index(array, mid + 1, u)

    if array[mid] == mid:  # se è un magic index, aggiungilo
      recursions += 2
      return magix_index(array, l, mid - 1) + [mid] + magix_index(array, mid + 1, u)


a = [-6, -5, -4, -3, -2, -1, 0, 2, 8, 9, 20, 66]

print('La lista di magic index di',a,'è:', magix_index(a, 0, len(a) - 1))
print('Il numero di domande minime per risolvere magix_index con questo vettore è:',questions)
print('Il numero di chiamate ricorsive per risolvere magix_index con questo vettore è:', recursions)
