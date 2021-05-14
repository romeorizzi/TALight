import random

def check_input_vector(vec, TAc, LANG):
    for i in range(1,len(vec)):
        if vec[i] == vec[i-1]:
            TAc.print(LANG.render_feedback("equal-values", f'No. Your vector contains entries with the same value vec[{i-1}] = {vec[i-1]} =vec[{i}].'), "red", ["bold"])
            exit(0)
        if vec[i] < vec[i-1]:
            TAc.print(LANG.render_feedback("decrease", f'No. Your vector is not incrisingly sorted: vec[{i-1}] = {vec[i-1]} > {vec[i]} = vec[{i}].'), "red", ["bold"])
            exit(0)

def random_vector(n, seed="any"):
    if seed=="any":
        random.seed()
        seed = random.randrange(0,1000000)
    else:
        seed = int(seed)

    random.seed(seed)
    vec = [random.randint(-10, 1000) for _ in range(n)]
    vec = set(vec) # we remove any duplicates
    vec = list(vec) 
    vec.sort()  # and we sort the list of elements
    
    return vec,seed

def spot_magic_index(vec):
    magic_indexes = []
    for i in range(len(vec)):
        if vec[i]==i:
            magic_indexes.append(i)
    return magic_indexes


questions = 0
recursions = 0

def magic_index(array, l, u):
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
      return magic_index(array, l, mid - 1)

    #ci chiediamo sempre se l'elemento corrente 'smezzato' è minore del suo indice 
    #(non serve sommare una question sotto nell'uguale perchè si va ad esclusione coi primi due)
    questions += 1
    if array[mid] < mid:
      recursions += 1
      return magic_index(array, mid + 1, u)

    if array[mid] == mid:  # se è un magic index, aggiungilo
      recursions += 2
      return magic_index(array, l, mid - 1) + [mid] + magic_index(array, mid + 1, u)