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

# TODO:
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
        if line.startswith('#') or line == '':
            continue
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

        if (elements[0] != '0' and i == 0):
            print("Lo stato iniziale (lo stato corrente della prima istruzione) deve essere 0")
            raise TypeError("Bad Format")

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
        # rules[readstate][readtape] = [writestate, writetape, movement, currline]
        # incremento numero di riga
        i += 1

    return rules

def tick(rules, sequence):
    stepcount = 0
    lastmove = '-'
    tapepos = 0
    currstate = '0'
    currtickline = 0
    stopped = False
    text = sequence.copy()
    while not stopped:
        if text[tapepos] not in rules[currstate] and text[tapepos] != ' ':
            # stampa l'errore con parametri
            print("ERRORE!\nNon è presente nessuna regola per il caso: stato corrente " + currstate + " e carattere letto " + text[tapepos])
            raise TypeError("Bad Format")
        rule = rules[currstate][text[tapepos]] if text[tapepos] != ' ' else rules[currstate]['-']
        text[tapepos] = " " if rule[1] == '-' else rule[1]
        lastmove = rule[2]
        currstate = rule[0]
        currtickline = rule[3]
        tapepos += 1 if lastmove == '>' else -1 if lastmove == '<' else 0
        stepcount += 1
        if tapepos < 0:
            text.insert(0, ' ')
            tapepos = 0
        if tapepos >= len(text):
            text.append(' ')
        # Cambiare questa istruzione
        if currstate not in rules:
            stopped = True

    return text

