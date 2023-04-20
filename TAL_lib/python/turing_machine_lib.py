#!/usr/bin/env python3
from doctest import OutputChecker
import random, re, copy
from sys import exit

alphabet = '#-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ '
reserved_chars = '<>(),'


def random_seq(seedParam, maxLengh):
    if seedParam=='random_seed':
        random.seed()
        seed = random.randrange(0,1000000)
        print("seed: " + str(seed))
    else:
        seed = int(seedParam)
        print("seed: " + str(seed))

    random.seed(seed)
    length = random.randint(2, maxLengh)
    sequence = []
    for i in range(length):
        sequence.append(random.randint(0, 1))
    return sequence

#TODO:
# X Controllare che l'istruzione inizi e finisca con una parentesi tonda
# X Togliere gli spazi
# X Controllare che i nomi degli stati non contengano spazi
# X Controllare che il movimento sia indicato solo con i simboli <>-
# X Controllare che gli elementi siano divisi da virgole
# X Controllare che i caratteri letti e scritti siano un singolo carattere
# X Controllare che gli stati non contengano -
# X Controllare che la stringa sia formata solo dai caratteri del mio alfabeto
# X controllare questo tipo di errore: (A,B ,0, AB ,1,>)
# X Controllare che gli elementi 0 e 2 non contengano spazi compresi tra caratteri alfanumerici
# X Controllare che gli stati e i caratteri scritti e letti non contengano caratteri speciali

def getRules(text):
    text = text.upper()
    rules = {}
    i = 0
    for line in text.splitlines():
        # X Controllare che la stringa sia formata solo dai caratteri del mio alfabeto
        for c in line:
            if c not in alphabet and c not in reserved_chars:
                print("L'istruzione contiene caratteri non ammessi")
                raise TypeError("Bad Format")

        line = line.strip()
        
        # X Controllare che l'istruzione inizi con una parentesi tonda
        if (line[0] != '('):
            print("L'istruzione è formata in maniera errata: deve iniziare con una parentesi tonda aperta")
            raise TypeError("Bad Format")
        
        # X Controllare che l'istruzione finisca con una parentesi tonda
        if (line[-1] != ')'):
            print("L'istruzione è formata in maniera errata: deve finire con una parentesi tonda chiusa")
            raise TypeError("Bad Format")
        line = line[1:-1]
        # X Controllare che gli elementi siano divisi da virgole
        elements = line.split(",")
        # X controllare questo tipo di errore: (A,B ,0, AB ,1,>)
        if(len(elements) != 5):
            print("L'istruzione è formata in maniera errata: devono esserci 5 elementi divisi da virgola")
            raise TypeError("Bad Format")
        # Controllare che gli elementi 0 e 2 non contengano spazi compresi tra caratteri alfanumerici
        if(re.search(r'\w\s+\w', elements[0]) or re.search(r'\w\s+\w', elements[2])):
            print("Lo stato non può contenere spazi")
            raise TypeError("Bad Format")
        # X Controllare che gli stati non contengano caratteri riservati
        for c in elements[0]:
            if c not in alphabet:
                print("Lo stato non può contenere caratteri speciali")
                raise TypeError("Bad Format")
        for c in elements[2]:
            if c not in alphabet:
                print("Lo stato non può contenere caratteri speciali")
                raise TypeError("Bad Format")
            
        # X Controllare che gli stati non contengano -
        if(re.search('-', elements[0]) or re.search('-', elements[2])):
            print("Lo stato non può contenere -")
            raise TypeError("Bad Format")
        
        # In ogni elemento di elements, elimino gli spazi
        for el in range(len(elements)):
            elements[el] = elements[el].strip()
            
        # X Controllare che i caratteri letti e scritti siano un singolo carattere
        if(len(elements[1]) != 1 or len(elements[3]) != 1):
            print("Il carattere letto e scritto devono essere un singolo carattere")
            raise TypeError("Bad Format")
        
        # X Controllare che i caratteri scritti e letti non contengano caratteri riservati
        if elements[1] not in alphabet:
            print("Il carattere letto non può essere un carattere speciale")
            raise TypeError("Bad Format")
        if elements[3] not in alphabet:
            print("Il carattere scritto non può essere un carattere speciale")
            raise TypeError("Bad Format")
        
        if(elements[0] not in rules):
            rules[elements[0]] = {}
        # X Controllare che il movimento sia indicato solo con i simboli <>-
        if(elements[-1] != "<" and elements[-1] != ">" and elements[-1] != "-"):
            print("Il movimento può essere indicato solo con i simboli < > -")
            raise TypeError("Bad Format")
        
        rules[elements[0]][elements[1]] = [elements[2], elements[3], elements[4], i]
        # incremento numero di riga
        i += 1

    return rules