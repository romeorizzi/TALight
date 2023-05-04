import turingarena as ta
import os

H = 0   # horizontal placement of a tile (2 rows, 3 cols)
V = 1   # vertical placement of a tile (3 rows, 2 cols)

num_offered_tilings = 0
def offer_a_tiling(m,n):
    global num_offered_tilings
    num_offered_tilings += 1

    # run with:
    # turingarena-dev evaluate --store-files solutions/solution.py
    # salva i file nella directory generated-files

    print(f"In caso ti serva un aiuto, o dove tu sia incredulo esso esista, ti ho messo un tiling della griglia ({m},{n}) nel file  generated-files/tiling_{num_offered_tilings}.txt")
    tiling=f"In questo file di testo (file ASCII) trovi un tiling della griglia ({m},{n}):"

    tiling +="""
    
    # TO BE DONE: la composizione di questo file
    # aggiungere righe al file.
    # conviene crearsi descrizione opportuna del tiling in memoria, entro matrici, e poi renderizzare queste in stringa per mezzo di caratteri ASCII opportuni:
    # va studiato anche lo schema con cui realizzare tegole (di più caratteri), mi pare che le ratio 3/5 e 3/4 approssimino bene, tipo:
    #     XXXXX     XXXX     
    #     X   X     X  X     sembrano entrambe abbastanza quadrati (non saprei dire quale di più)
    #     XXXXX     XXXX
    #
    #     e quindi, se ad esempio scegli la 3/4:
    #
    #     XXXXXXXXXXXX
    #     X          X
    #     X__________X    per la (2,3) orizzontale
    #     X          X
    #     X          X
    #     XXXXXXXXXXXX
    #
    #     XXXXXXXX
    #     X      X
    #     X______X        per la (3,2) verticale
    #     X      X
    #     X      X
    #     X______X
    #     X      X
    #     X      X
    #     XXXXXXXX
    #
    #  ma ovviamente va fatto un studio più attento sui caratteri ASCII da adottare e questo può influire sui rapporti e geometrie. E' importante presatare sempre attenzione che poi se ne metto di orizzontali e di verticali si incastrino, ossia il numero totale di caratteri in verticale di una (2,3) deve essere i 3/2 dei caratteri in verticale di una (3,2), ed allo stesso modo devono tornare i rapporti sulla larghezza orizzontale in caratteri. 
    #
    #  da progettare anche la forma della rappresentazione più opportuna del tiling in memoria per facilitare la traduzione visuale. Per l'idea astratta del tiling si può avvalersi invece della soluzione del problema nella cartella solutions (in futuro, con l'esperienza in classe, capiremo se non sia opportuno oscurarla offrendo tiling meno regolari e più caotici. Anche per questo è bene separare le varie fasi che portano a renderizzare l'idea del tiling (l'oggetto combinatorico), entro un file di ASCIIART).
"""

    ta.send_file(tiling, filename=f"tiling_{num_offered_tilings}.txt")




def test_case(m,n):
    def turn_off_construction_goal_flags(m,n):
        if m == 2:
            ta.goals["construction_m2"] = False
        if m <= 10 and n <= 10:
            ta.goals["construction_small"] = False
        ta.goals["construction"] = False

    def turn_off_decision_goal_flags(m,n):
        if m == 2:
            ta.goals["decision_m2"] = False
        if m <= 10 and n <= 10:
            ta.goals["decision_small"] = False
        if m <= 100 and n <= 100:
            ta.goals["decision"] = False
        ta.goals["decision_huge"] = False
        
    with ta.run_algorithm(ta.submission.source) as p:
        print(f"case (m={m}, n={n})")
        tiling_exists = 1
        if (m*n)%6:
            tiling_exists = 0
        if (m <= 1) or (n<=1):
            tiling_exists = 0
        try:
            res = p.functions.is_tilable(m, n)
        except ta.AlgorithmError as e:
            print(f"During the execution of your function is_tilable({m},{n}) we got the following exception:")
            print(e)
            turn_off_decision_goal_flags(m,n)
        else:
            print(f"From your is_tilable({m},{n}) function we expected {tiling_exists}, got {res}")
            if res == tiling_exists:
                print("OK. The two values coincide.")
            else:
                turn_off_decision_goal_flags(m,n)
                if res == 0:
                    turn_off_construction_goal_flags(m,n)
                    print(f"According to your is_tilable function, the {m}x{n}-grid is not tilable with 2,3-bars. However, we believe it is! If you disbelieve this and/or need help to advance, have a look at the tiling offered in the spoiling solution file: ... ")
                    offer_a_tiling(m,n)
                if res != 0:
                    print(f"According to your is_tilable function, the {m}x{n}-grid is tilable. Are you sure?\n In case you can exhibit such a tiling, please contact turingarena.org, we look forward to see it." )
        
        if not tiling_exists or res == 0 or m > 100 or n > 100:
            return

        # BEGIN: testing of the procedure constructing the tiling
        print(f"Ok, since we agree the tiling exists, and an ({m},{n})-board is still reasonably small, let's find out whether your code can actually construct the tiling and measure its efficiency.")
        construction_ok = True
        posed_tiles = 0
        covered = [ [False for _ in range(n+1) ] for _ in range(m+1) ]
        lista_tiles = []
        def place_tile(row,col,dir):
            nonlocal construction_ok
            nonlocal posed_tiles
            nonlocal covered
            nonlocal lista_tiles
            lista_tiles.append((row,col,dir))
            posed_tiles += 1
            if dir == H:
                cells = [ [row,col], [row,col+1], [row,col+2], [row+1,col], [row+1,col+1], [row+1,col+2] ]
            else:    
                cells = [ [row,col], [row+1,col], [row+2,col], [row,col+1], [row+1,col+1], [row+2,col+1] ]
            for cell in cells:
                row = cell[0]
                col = cell[1]
                if row < 1 or col < 1 or row > m or col > n:
                    print(f"La tua tessera fuoriesce dalla scacchiera nella cella ({row},{col}).")
                    construction_ok = False
                    return
                if covered[row][col]:
                    print(f"Due delle tue tegole coprono la cella ({row},{col}).")
                    construction_ok = False
                    return
                covered[row][col] = True

        try:
            print("[mostra il tiling (fino all'eventuale errore), magari in un file esterno da scaricare od un applet]")
            p.procedures.compose_tiling(m, n, callbacks = [place_tile] )
        except ta.AlgorithmError as e:
            print(f"During the execution of your procedure compose_tiling({m},{n}) we got the following exception:")
            print(e)
            turn_off_construction_goal_flags(m,n)
        else:
            if construction_ok:
                if 6*posed_tiles == m*n:
                    print(f"Complimenti! Hai trovato un tiling perfetto della griglia ({m},{n}). Questo è ovviamente ottimo senza ricorrere ad argomenti più fini e linguaggi di NO più misteriosi.")
                else:
                    offer_a_tiling(m,n)
                    print(f"Hai fornito un packing corretto ma esso non è un tiling perfetto quindi non mi è ovvio esso sia ottimo. Per ora mi hai convinto che esista un packing di almeno {posed_tiles}, ossia mi hai dato un lower-bound sul valore ottimo del packing. In esercizi successivi di questo percorso apprenderai come fornire argomenti a supporto dell'ottimalità dei tuoi packing e andiamo a vedere quanto è buono l'upper-bound che sai fornirmi. Tuttavia in questo caso (m={m} e n={n}) esiste un tiling ottimo. Quindi prendiamo per NON buono il packing che hai qui prodotto.")
                    turn_off_construction_goal_flags(m,n)
                print("[vuoi vedere come la tua procedura ha collocato le piastrelle? In questo punto potremmo mettere il tiling prodotto dalla tua procedura dentro in file esterni che il problem-solver possa scaricarsi: sarebbe bella una visualizzazione statica in grafica vettoriale, con le piastrelle numerate nell'ordine di posatura, ma anche un ASCII con solo il log della sequenza delle chiamate a pose_tile da usare per eventuale debug, e comunque visualizzabile in un'applet. Come vedi, ci sono mille modi in cui puoi contribuire a rendere TA piu ricco ed interattivo. Se anche tu come noi pensi 'We don't need no education' non esistare: richiedi progetti e 'brake on through to the other side'.]")
            else:
                turn_off_construction_goal_flags(m,n)
                print("mostra il tiling fino all'errore: ", lista_tiles)

                
def run_all_test_cases():
    for m in range(1,8):
        for n in range(1,8):
            test_case(m,n)
    test_case(9,9)        
    test_case(9,10)        
    test_case(10,10)        
    test_case(99,99)        
    test_case(100,100)        
    test_case(99999,99999)        
    test_case(100000,100000)        
        
run_all_test_cases()

ta.goals.setdefault("decision_m2", True)
ta.goals.setdefault("decision_small", True)
ta.goals.setdefault("decision", True)
ta.goals.setdefault("decision_huge", True)
ta.goals.setdefault("construction_m2", True)
ta.goals.setdefault("construction_small", True)
ta.goals.setdefault("construction", True)

print(ta.goals)

