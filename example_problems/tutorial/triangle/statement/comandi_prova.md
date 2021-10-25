Lista dei comandi per richiedere i servizi. Presenti solo gli argomenti obbligatori.

**AVVIARE IL SERVER**

```
rtald -d ~/TALight/example_problems/tutorial
```

**gimme_instance** 

```
rtal connect triangle gimme_instance
```

**check_one_sol** 

Inserimento del triangolo tramite seed e del path come argomento.
```
rtal connect -ahow_to_input_the_triangle=123456 -apath=LRRL triangle check_one_sol
```

**check_sol_value** 
1. Inserimento del triangolo tramite seed e del path come argomento.
```
rtal connect -ahow_to_input_the_triangle=123456 -asol_value=LRRL triangle check_sol_value
```
2. Inserimento del triangolo tramite seed e del valore della soluzione come argomento.
```
rtal connect -ahow_to_input_the_triangle=123456 -asol_value=300 triangle check_sol_value
```


**check_path_value** 
Inserimento del triangolo tramite seed e del path come argomento.
```
rtal connect -ahow_to_input_the_triangle=123456 -apathvalue=300 -apath=LRRLtriangle check_path_value
```
