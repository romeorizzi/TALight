/*
Generatore di input per il problema Collage.

arg1 --> lunghezza della sequenza numerica da generare
arg2 --> lunghezza della sequenza numerica compressa
arg3 --> numero di colori disponibili (1 - 256), non il valore massimo (0 - 255)
arg4 --> modalita'
arg5 --> seed

VALORI ACCETTABILI PER MODALITA':
- 0 parentesi
- 1 chi2
- 2 completamente random

USI SPECIALI:
arg1 < 0: i casi di esempio
*/
#include<iostream>
#include<cassert>
#include<cstdlib>
#include<random>
#include<unordered_set>
#include<vector>
#include<ext/pb_ds/assoc_container.hpp>
#include<ext/pb_ds/tree_policy.hpp>

#define MAX_LEN 1000000
#define MAX_COMPRESSED_LEN 150
#define OFFSET 2000002
#define MAX_COLOR_PALETTE 256
#define N_MOD 3
#define LOG2(X) ((unsigned) (8*sizeof (unsigned long long) - __builtin_clzll((X)) - 1))

namespace std {
    /*un po' una schifezza, ma per il suo scopo limitato va bene.
    UniqueID serve per il padding.
    I nodi verranno inseriti in un order statistics tree per avere insertion piu' veloce rispetto ad un array, e access migliore rispetto ad una lista.*/
    uint64_t uniqueIDCounter = OFFSET;
    class NODO {
        public:
        NODO(int _colore, uint64_t id) : colore(_colore), uniqueID(id) {};
        NODO(int _colore) : colore(_colore) { uniqueID = uniqueIDCounter; uniqueIDCounter += OFFSET;};
        int colore;
        vector<NODO> figli;
        bool isDouble = false;
        uint64_t uniqueID;
    };
    template<> struct less<std::NODO> {
        bool operator() (const NODO& lhs, const NODO& rhs) const
        {
            return lhs.uniqueID < rhs.uniqueID;
        }
    };
}
using namespace std;
using namespace __gnu_pbds;
typedef tree<
            NODO,
            null_type,
            less<NODO>,
            rb_tree_tag,
            tree_order_statistics_node_update > STATISTIC_TREE;

STATISTIC_TREE generatedTree;


/* CODICE DI RIFERIMENTO ==> 1
Generazione con distribuzione Chi2
*/
void chiMode(int& len, int& numColors, int& seed){
    auto generator = default_random_engine(seed);
    int logC = LOG2(numColors) + 1;
    assert(logC > 0 && logC <= numColors);
    chi_squared_distribution<double> distribution(logC + 1);

    int count = 0;
    int oldColor = MAX_COLOR_PALETTE;
    int tmp;
    while(count < len) {
        tmp = distribution(generator);
        if(tmp >= 0 && tmp < numColors) {
            tmp = (tmp + (tmp == oldColor)) % numColors;
            oldColor = tmp;
            count++;
            generatedTree.insert(NODO(tmp));
        }
    }
}





/* CODICE DI RIFERIMENTO ==> 2
Generazione molto semplice: col classico rand() % colori disponibili.
*/
void randomMode(int& len, int& numColors, int& seed){
    int oldColor = MAX_COLOR_PALETTE;
    int tmp;
    for(int i = 0; i < len; i++) {
        tmp = rand() % numColors;
        tmp = (tmp + (tmp == oldColor)) % numColors;
        oldColor = tmp;
        generatedTree.insert(NODO(tmp));
    }
}





/*
Divide il nodo in bucket in base alla sua lunghezza. Ogni bucket sara' un figlio e rappresentera' una "parentesi".
Ogni bucket viene ridiviso ricorsivamente.
I colori gia' usati hanno una maggior possibilita' di essere usati di nuovo per aumentare il grado di difficolta'.
*/
void recursiveCall(NODO& node, int len, unordered_set<int>& usedColors, int& numColors) {
#ifdef DEBUGME
    cout << "LEN:" << len << " ID:" << node.uniqueID << endl;
#endif
    assert(len > 0);
    //se mi e' rimasto da distribuire una lunghezza < 3 si trattera' o di un unico elemento, o di un paio di parentesi senza alcun elemento al loro interno.
    if(len == 1) {
        return;
    } else if(len == 2) {
        assert(len != 2 && "LEN 2 DOVREBBE ESSERE DISABILITATO");
        node.isDouble = true;
        return;
    } else {
        //sottraggo 2, ovvero le "parentesi esterne"
        len -= 2;
        int logC = LOG2(len + 1) + 1;
        
        //Bucket troppo grandi semplificano troppo la vita.
        //Per esempio con lunghezza mille la dimensione massima viene fissata a 500, cosi' da avere ALMENO due bucket.
        int maxBucketSize = max(1, len / ((rand() % logC) + 1));
        int newColor, bucketSize;
        
        //Colore da NON usare per il prossimo figlio
        auto forbiddenColor = node.colore;

        //Continuo a suddividere finche' ho ancora spazio a disposizione.
        while(len > 0) {
            bucketSize = min(len, 1 + (rand() % maxBucketSize));
            if(bucketSize == 2) {
                bucketSize = 1; //len 2 disabilitato (produrrebbe una sequenza non del tutto compressa)
            }
            do {
                newColor = rand() % (numColors * 3);
                if(newColor >= numColors) {
                    newColor = newColor % usedColors.size();
                    auto it = usedColors.begin();
                    advance(it, newColor);
                    newColor = *it;
                }
            } while(newColor == forbiddenColor || (newColor == node.colore && (bucketSize > 1 || len == 1)));
            usedColors.insert(newColor);
            forbiddenColor = newColor;
            
            //Aggiungo un nuovo figlio
            node.figli.push_back(NODO(newColor));
            
            //Suddivido anche il figlio
            recursiveCall(*node.figli.rbegin(), bucketSize, usedColors, numColors);
            len -= bucketSize;


            #ifdef DEBUGME 
            if(node.uniqueID == OFFSET) cout << "LEN:" << len << " ID:" << node.uniqueID << " B:" << bucketSize << " M:" << maxBucketSize << endl;
            #endif
        }
    }
}

/*
Solo il primo nodo verra' ignorato.
Vedi --> treeMode
*/
void visitPrint(NODO& node, bool ignoreMe = false) {
    if(!ignoreMe) {
        generatedTree.insert(NODO(node.colore));
    }
    if(!node.figli.empty()) {
        for(size_t i = 0; i < node.figli.size(); i++) {
            visitPrint(node.figli[i]);
        }
    }
    if(!ignoreMe && (node.isDouble || !node.figli.empty())) {
        generatedTree.insert(NODO(node.colore));
    }
}

/* CODICE DI RIFERIMENTO ==> 0
Generazione simil formula con parentesi.
Dopo una serie di chiamate ricorsive in cui si genera un albero, alla fine con una visita si ottiene una cosa molto simile ad una formula formata da parentesi.
La prima parentesi e' "invisibile", cosi' da ottenere una formula che non e' necessariamente fatta cosi':
((.........)(.......).....(......))
ma molto piu' probabilmente sara':
(.........)(.......).....(......)
*/
void treeMode(int& len, int& numColors, int& seed){
    if(numColors < 3) {
        randomMode(len, numColors, seed);
        return;
    }
    auto usedColors = unordered_set<int>();
    NODO radice (rand() % numColors);
    usedColors.insert(radice.colore);


    recursiveCall(radice, len + 2, usedColors, numColors);

    visitPrint(radice, true);
}


/*
Duplica nodi finche' non raggiunge la giusta lunghezza.
Per ogni iterazione, viene scelto un nodo e ne viene aggiunto uno uguale accanto
*/
void pad(size_t newSize) {
    auto currentSize = generatedTree.size();
    while(currentSize < newSize) {
        size_t randomPos = rand() % currentSize++;
        /*
        auto elem = generatedTree.find_by_order(randomPos++);
        auto n = generatedTree.find_by_order(randomPos++);
        if(n!=generatedTree.end() && (n->colore == elem->colore)) {
            do {
                n = generatedTree.find_by_order(randomPos++);
            } while(n!=generatedTree.end() && (n->colore == elem->colore));
            n = generatedTree.find_by_order(randomPos - 2);
        } else {
            n = elem;
        }
        */
        auto elem = generatedTree.find_by_order(randomPos);
        auto n = elem;
        NODO fakeNODE = *elem;
        fakeNODE.uniqueID+= MAX_LEN + 1; //al piu' avro' duplicato quel nodo MAL_LEN volte
        auto sameGroupPos = generatedTree.order_of_key(fakeNODE) - 1; //Trovo la posizione dell'ultimo nodo di quel tipo duplicato chiedendo all'albero "Quanti nodi ci sono ID minore di...?" e sottranedo 1 perche' le posizioni iniziano da 0.
        if(randomPos != sameGroupPos && sameGroupPos != currentSize - 1) { //la seconda condizione non dovrebbe mai verificarsi. E' lì tanto per essere sicuri. Non cambia niente dal punto di vista della performance
            n = generatedTree.find_by_order(sameGroupPos);
        }

#ifdef DEBUGME
        cout << "elemColore: "<< elem->colore << " ID: " << elem->uniqueID << ". Aggiungo colore: " << n->colore << " ID: " << n->uniqueID + 1 << endl;
#endif
        generatedTree.insert(NODO(n->colore,n->uniqueID + 1));
    }
}

int main(int argc, char** argv) {
    assert(argc > 0);

    //CASI DI ESEMPIO
    if(argc == 2) {
        int exNumber = atoi(argv[1]);
        assert(exNumber < 0);
        switch(exNumber)
        {
            case -1:
                cout << "3" << endl << "1 2 1" << endl;
                break;
            case -2:
                cout << "7" << endl << "1 1 2 3 1 2 1" << endl;
                break;
            default:
                return - 1;
                break;
        }
        return 0;
    }
    assert(argc == 6);

    int len = atoi(argv[1]);
    assert(len <= MAX_LEN && len > 0);

    int compressedLen = atoi(argv[2]);
    assert(compressedLen <= len && compressedLen <= MAX_COMPRESSED_LEN && compressedLen > 0);

    int numColors = atoi(argv[3]);
    assert(numColors <= MAX_COLOR_PALETTE && numColors >= 1);

    assert(!(compressedLen > 1 && numColors == 1));

    int mod = atoi(argv[4]);
    assert(mod < N_MOD && mod >= 0);

    int seed = atoi(argv[5]);
    srand(seed);

    //Prima riga: lunghezza della sequenza
    cout << len << endl;

    //Generiamo una sequenza compressa di lunghezza compressedLen
    switch(mod) {
        case 0:
            treeMode(compressedLen, numColors, seed);
            break;
        case 1:
            chiMode(compressedLen, numColors, seed);
            break;
        case 2:
            randomMode(compressedLen, numColors, seed);
            break;
        default:
            return -1;
    }

#ifdef DEBUGME
    cout << "TREE PRIMA DI PADDING" << endl;
    for(auto it = generatedTree.begin(); it != generatedTree.end(); it++) {
        cout << it->colore << " ";
    }
    cout << endl << "Size: " << generatedTree.size() << endl << "TREE DOPO PADDING" << endl;
#endif

    //Padding della sequenza fino a raggiungere la lunghezza len
    pad(len);

    //Seconda ed ultima riga: la sequenza
    for(auto it = generatedTree.begin(); it != generatedTree.end(); it++) {
        cout << it->colore << " ";
    }
    cout << endl;

    return 0;
}
