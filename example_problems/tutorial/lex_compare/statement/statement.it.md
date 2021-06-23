# Confronto lessicografico tra stringhe

Con questo problema e percorso didattico intendiamo familiarizzare col concetto di ordine lessicografico.

Cominciamo con l'ordine lessicografico tra strighe, ossia quello utilizzato nella compilazione dei dizionari.

Quando recitiamo l'alfabeto scandiamo le lettere nel seguente ordine:

```
A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, X, Y, Z
```

L'ordine lessicografico tra stringhe è una naturale estensione di tale ordine tra le lettere (dette anche caratteri).

**stringa:** Una stringa è una sequenza finita di lettere da un dato alfabeto, nel nostro caso utilizzeremo l'_alfabeto inglese maiuscolo_ sopra elencato.

**ordinamento lessicografico:** Dall'ordinamento dell'alfabeto consegue un ordinamento dell'insieme delle stringhe costruibili da esso, secondo le regole:

 1. se $s_1$ ed $s_2$ sono entrambe la stringa vuota allora esse sono uguali;
 2. la stringa vuota è minore di qualsiasi altra stringa;
 3. se il primo carattere di $s_i$ è minore del primo carattere di $s_j$ allora $s_i < s_j$;
 4. se $s_1$ ed $s_2$ iniziano con uno stesso carattere $C$, cioè $s_1 = Cs'_1$ e $s_s = Cs'_2$, allora il confronto tra $s_1$ ed $s_2$ si riduce al confronto tra $s'_1$ e $s'_2$.

Si noti che l'ordinamento lessicografico fà dell'insieme infinito delle stringhe un insieme totalmente ordinato.

Se ti restano dei dubbi su quale sia l'esito corretto del confronto tra due date stringhe, puoi sottoporle al servizio `compare_two_strings` per risolverli. Tramite l'argomento `feedback`, potrai anche richiedere al servizio di fornire maggiori spiegazioni sul perchè quello sia l'esito corretto. Ma ecco un esempio di interazione semplice col servizio:

```
> rtal connect lex_compare compare_two_strings -a s=MARIA t=MARIANNA
s < t
```

Quando reputi che la nozione di ordine lessicografico ti sia chiara, prova a scrivere tu un bot che effettui il confronto e chiedine validazione al servizio `eval_compare_two_strings`. L'argomento `goal` di tale servizio ti consente di modulare i tuoi obiettivi come da tabella:

`char_vs_char`: entrambe le stringhe sono di un solo carattere.
`char_vs_string`: la prima stringa è di un solo carattere.
`string_vs_string`: stringhe qualsiasi, nessuna restrizione.

## Esempi di input/output per il tuo bot:
```
MARIA
MARIANNA
-1
```
```
PESCECANE
PESCE
1
```
```
BELLO
BELLO
0
```
```
BUONO
BELLO
1
```

## Linguaggi di programmazione

Il tuo bot gira in locale e dialoga col servizio (che potrà essere anche esso in locale oppure nel cloud). Ti è pertanto consentito di utilizzare il linguaggio che preferisci. Se poi vorrai consegnare il tuo sorgente ad un tuo docente di riferimento, ad esempio per ottenere un feedback sullo stile di programmazione, segui le sue indicazioni in merito al linguaggio e a quant'altro.

Nel caso di alcuni linguaggi potrai trovare dei template già pronti che si occupano di cose come l'input/output e dove, per ottenere un bot funzionante, puoi limitarti ad inserire la logica sottostante la competenza in questione.

Ad esempio, nel file `lex_compare_template_bot.py` contenuto nella cartella `templates` dovrai solo risistemare l'implementazione della funzione `lex_compare`. Essa riceve in input due stringhe $s$ e $t$ e vorrebbe restituire l'esito del loro confronto, ma al momento ci vede poco tanto che per lei le stringhe sono tutte uguali:

```python
def lex_compare(s,t):
    return UGUALE
```

Metti gli occhiali alla `lex_compare`. Essa deve ritornare MINORE quando $s<t$ e MAGGIORE quando $t<s$. In tutti gli altri casi dovrà continuare a ritornare UGUALE, ovviamente. (Nota Bene: le costanti simboliche UGUALE, MINORE e MAGGIORE sono definite da noi nel template, ti basta utilizzarle, sono un nostro pensierino per voi per meglio accompagnarvi nei vostri primi passi con la buona programmazione).

## Come mettere alla prova il tuo bot

Dalla cartella dove si trova il tuo bot lancia il comando:

```
> rtal connect -e lex_compare eval_compare_two_strings -- python lex_compare_template_bot.py
```

Puoi lanciarlo anche da altra cartella, specificando però tramite il path dove si trovi il tuo bot.

# Confronto lessicografico tra due vettori

La mia idea quì sarebbe di riproporre qualcosa in tutto analogo (come schema e servizi) a quanto sopra per le stringhe.


# Confronto lessicografico tra due sequenze, in generale

La mia idea quì sarebbe di offrire un servizio di valutazione di un bot che, su un certo numero di testcases, per ciascuno dei quali ha luogo il seguente dialogo:

```
   il server scrive le lunghezze delle sequenze S e T per l'istanza che ha in mente
   il bot può fare delle query del tipo:
   ? i j
   con le quali chiede l'esito del confronto tra S[i] e T[j]
   il bot restituisce infine l'esito del confronto tra S e T.
```

In questo caso tra i goal del servizio di valutazione potremmo mettere vari possibili bound sul numero delle query.
`any_number_of_queries`
`never_repeat_a_query`
`at_most_m_times_n_queries`
`at_most_m_plus_n_queries`
`minimum_number_of_queries`
