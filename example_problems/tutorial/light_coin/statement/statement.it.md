# Individuare la Moneta Leggera (light_coin)

## Descrizione del problema

Vuoi individuare l'unica moneta falsa in un set di $7$ monete numerate da $1$ ad $7$. Puoi avvalerti in questo di una bilancia a braccia uguali.
Questo puzzle classico assume che la moneta falsa ha un peso diverso delle altre (e in una sua variante più semplice assume che il penso della moneta falsa sia sempre inferiore a quello delle altre).
Organizzare una pesata significa specificare i due sottoinsiemi disgiunti di $\{1,2,3,4,5,6\}$ delle monete da collocare sui due piatti della bilancia. Ad esempio, Se giochi a riga di comando, con:

[1, 5, 6], [2, 4]

richiederesti una pesata con le monete $1$, $5$, e $6$ sul piatto sinistro e $2, 4$ su quello destro. 

La misura potrà avere uno dei seguenti 3 esiti:

- **NONE:** se i due piatti della bilancia sono in perfetto equilibrio (nessuno dei due scende in basso);

- **LEFT:** se il carico è maggiore sul piatto sinistro;

- **RIGHT:** se il carico è maggiore sul piatto destro.

## Estensibilità ever green del problema

Attorno a questo puzzle potrai condurre delle tue esplorazioni, al momento possiamo proporre i seguenti percorsi:

1. distinzione tra strategie statiche (dove l'insieme delle misure da compiere viene fissato a priori) e dinamiche (dove ogni atto di misura viene stabilit potendo prendere in considerazione gli esiti delle pesate precdenti)

2. ricerca della natura ricorsiva del problema chiedendosi come possa essere stabilita una buna strategia di gioco per un numero di monete $n$ generico.

Se ti sovvengono altre di queste curiosità puoi porti la sfida di realizzare tu dei servizi che stimolino e supportino il problem solver e scoprirti nel ruolo di problem maker ([brake on through to the other side](https://www.youtube.com/watch?v=-r679Hhs9Zs)). 

## Supporti alla programmazione, interfacce grafiche, o avanguardia

Oltre che giocare tu stesso prescrivendo le tue pesate da riga di comando con:

```bash
rtal connect light_coin check_dynamic_strategy
```

puoi divertirti ad istruire un bot affinchè giochi in tua vece con:

```bash
rtal connect light_coin check_dynamic_strategy -- python mybot.py
```

Il bot può essere scritto in un qualsiasi altro linguaggio, e, se è un compilato, non ti sarà necesario richiamare l'interprete:

```bash
rtal connect light_coin check_dynamic_strategy -- mybot
```

Ovviamente il file `mybot` sarà il file col codice binario prodotto con la compilazione, coi necessari diritti di esecuzione settati.  

Se vuoi concentrarti sugli aspetti alti del probema e trascurare i dettagli della programmazione, puoi prendere un bot contenitore per il tuo linguaggio e limitarti a specificare l'implmentazine delle funzioni che gstisocono la logica del gioco. Ad esempio in python potrai limitarti ad implementare la funzione `individua()` nel modulo `logic.py` e da `individua()` potrai chiamare il comando/funzione: 

```
risp = piatto_con_peso_maggiore(left=[1, 5, 6], right=[2, 4])
```

Quando poi sei sicuro su quale sia la moneta falsa dovrai consegnarla alla zecca invocando:
```
denuncia(monetaFalsa)
```
per concludere con successo la partita.

E'altresì possibile giocare entro un applet grafico (adatto per le medie) oppure in un ambiente ibrido dove ti sono consentiti varie possibilità per collocare ogni tua intrazione e, ad esempio, se compi una tua mossacol mouse puoi ottenerne visualizzazione/traduzione a vari livelli diversi del protocollo di gioco.

## Servizi di tipo eval (per ottenere un feedback anche sul piano dei metodi e delle tcniche di problem solving)


### Possibili goals per la strategia dinamica

- Il programma termina dopo la prima chiamata alla funzione denuncia oppure allo scadere del tempo limite.

- $1 <= n <= 1,000,000$

## Obbiettivi

1. Trovare la moneta falsa.

2. Trovare la moneta falsa tra 7 monete ($n = 7$) con al massimo 6 pesate.

3. Trovare la moneta falsa tra 7 monete ($n = 7$) con al massimo 4 pesate.

4. Trovare la moneta falsa tra 7 monete ($n = 7$) con al massimo 3 pesate.

5. Trovare la moneta falsa tra 8 monete ($n = 8$) con al massimo 3 pesate.

6. Trovare la moneta falsa con al più $n - 1$ pesate.

7. Trovare la moneta falsa con al più $\lfloor n/2 \rfloor$ pesate.

8. Trovare la moneta falsa con al più $\lfloor log_2 n \rfloor$ pesate.

9. Viene permesso solo quel minimo numero di pesate che, se impiegato, sapientemente, consenta sempre di individuare la moneta falsa.
