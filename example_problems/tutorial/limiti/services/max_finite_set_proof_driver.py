#!/usr/bin/env python3
from sys import exit

from sympy import maximum
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
import limiti_lib as ll
import random
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('cardinality',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')

## START CODING YOUR SERVICE:
cardinality=ENV["cardinality"]
def step1():
    user_sol=TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0]
    if user_sol!='s1' and user_sol!='sn':
        TAc.print(LANG.render_feedback("wrong", f'questa scrittura non la capisco o e` errata... prova a rispondere con "sj" per un certo j tale che sj appartiene ad S:'), "red", ["bold"])
        return step1()
    else:
        return TAc.print(LANG.render_feedback("correct", 'Giusto! Infatti: \n- s1 appartiene ad S? Si! \n- ogni elemento sj in S e` tale che sj<=s1? Si, infatti S={s1} e s1<=s1)'), "green", ["bold"])
def check_command_subset(stringa,n):
    posiz_start=stringa.find("max_in_sottoinsieme")+20
    comma_position=stringa.find(',')
    parenthesis_position=stringa.find(')')
    start=stringa[posiz_start:comma_position]
    def check_argument_value(stringa,n):
        try:
            eval_str=eval(stringa,{'n':n})
            if not int(eval_str)==eval_str:
                TAc.print(LANG.render_feedback("wrong", f'No, \'max_in_sottoinsieme\' prende come argomenti solo numeri interi'), "red", ["bold"])
                exit(0)
            else:
                int_value=int(eval_str)
                return int_value
        except:
            TAc.print(LANG.render_feedback("wrong", f'No, \'max_in_sottoinsieme\' prende come argomenti solo numeri interi (o espressioni numeriche, al piu` e` consentito l\'utilizzo della variabile n che qui vale {n}).'), "red", ["bold"])
            exit(0)
    start_value=check_argument_value(start,n)
    end=stringa[comma_position+1:parenthesis_position]
    end_value=check_argument_value(end,n)
    if start_value>end_value:
        TAc.print(LANG.render_feedback("wrong", f'No, \'max_in_sottoinsieme(j,k)\' deve essere tale che j<=k'), "red", ["bold"])
        exit(0)
    if start_value==1 and end_value==n:
        TAc.print(LANG.render_feedback("wrong", f'No, il sottoinsieme di cui mi hai chiesto di trovare il massimo e` un sottoinsieme improprio!'), "red", ["bold"])
        exit(0)
    if end_value>n or start_value>n:
        TAc.print(LANG.render_feedback("wrong", f'Vedi, |S|={n} e tu mi hai chiesto di trovare il massimo di un sottoinsieme che contiene un elemento che non sta in S.'), "red", ["bold"])
        exit(0)
def check_command_generic(stringa):
    posiz_start=stringa.find("max_in_sottoinsieme")+20
    comma_position=stringa.find(',')
    start=stringa[posiz_start:comma_position]
    posiz_end=comma_position+1
    end=stringa[comma_position:posiz_end]
    if not posiz_end.isdigit():
        exit(0)
    end=int(posiz_end)
    if start>end:
        TAc.print(LANG.render_feedback("wrong", f'No, \'max_in_sottoinsieme(j,k)\' deve essere tale che j<=k'), "red", ["bold"])
        exit(0)
    if start==1 and end==n:
        TAc.print(LANG.render_feedback("wrong", f'No, il sottoinsieme di cui mi hai chiesto di trovare il massimo e` un sottoinsieme improprio!'), "red", ["bold"])
        exit(0)
    if end>n or start>n:
        TAc.print(LANG.render_feedback("wrong", f'No, mi hai chiesto di trovare il massimo di un sottoinsieme che contiene un elemento maggiore di s{n}'), "red", ["bold"])
        exit(0)
def check_argument_confronto(user_sol,n):
    posiz_1=user_sol.find("confronto")+10
    comma_position=user_sol.find(',')
    arg_1=user_sol[posiz_1:comma_position]
    def check_argument(argument,n):
        if not argument[0]=='s' or not (argument[1:].isdigit() or argument[1:]=='n'):
            TAc.print(LANG.render_feedback("wrong-input", f'L\'oracolo "confronto" prende come argomenti due elementi dell\'insieme S della forma sj per un certo j<={n}'), "red", ["bold"])
            exit(0)
        elif argument[1:].isdigit() and int(argument[1:])>n:
            TAc.print(LANG.render_feedback("wrong-input", f'No, mi stai chiedendo di calcolare il massimo di un elemento che non sta in S.'), "red", ["bold"])
            exit(0)
    check_argument(arg_1,n)
    parenthesis_position=user_sol.find(')')
    arg_2=user_sol[comma_position+1:parenthesis_position]
    check_argument(arg_2,n)
def check_correctness_max(indices_set,user_sol,max_elem,n):
    if len(indices_set)>1:
        TAc.print(LANG.render_feedback("wrong", f'No, il tuo pseudo-algoritmo non trova il massimo, non hai confrontato tutti gli elementi di S tra di loro.'), "red", ["bold"])
        exit(0)
    if user_sol[7]=='s' and (user_sol[8:].isdigit() or user_sol[8:]=='n'):
        if int(eval(user_sol[8:],{'n':n}))==max_elem:
            TAc.print(LANG.render_feedback("correct", f'Ottimo! Il massimo dell\'insieme S e` s{max_elem}.'), "green", ["bold"])
            exit(0)
        else:
            TAc.print(LANG.render_feedback("error", f'No, il massimo dell\'insieme S non e` s{user_sol[8:]}, e` s{max_elem}.'), "red", ["bold"])
            exit(0)
    else:
        TAc.print(LANG.render_feedback("error", f'Non riesco a decifrare quello hai scritto, la sintassi e` "return sj" per una certa j<={n}.'), "red", ["bold"])
        exit(0)
if cardinality!='open':
    n=random.randint(2,10) if cardinality=='random' else int(cardinality)
    TAc.print(LANG.render_feedback("start", 'Ti va di dimostrare formalmente che un insieme finito di numeri ha sempre un massimo? Lo faremo insieme, sara` una dimostrazione per induzione. Dovrai astrarre la capacita` di trovare il massimo in modo da assicurarci che qualsiasi sia l\'insieme S={s1,s2,s3,...,sn} di n>0 elementi che ti viene proposto tu sappia trovare sempre il massimo.'), "white", ["bold"])
    TAc.print(LANG.render_feedback("set-explain", 'Consideriamo insiemi della forma S={s1,s2,s3,...,sn}.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("base-case", f'CASO BASE: se n=1, qual e` il massimo dell\'insieme S?'), "yellow", ["bold"])
    step1()
    if n==1:
        exit(0)
    TAc.print(LANG.render_feedback("inductive-step", f'PASSO INDUTTIVO: se n>1, qual e` il massimo dell\'insieme S? Per rispondere hai a disposizione ben 2 oracoli: \n- confronto(sj,sk) : confronta due elementi nell\'insieme S, ovvero sj ed sk e restituisce il maggiore dei due \n- max_in_sottoinsieme(j,k) : considera il sottoinsieme proprio di S costituito dagli elementi che vanno da sj fino ad sk (quindi j<=k) e restituisce il massimo tra questi. \nProva a combinare chiamate agli oracoli disponibili in modo da costruire il massimo sapendo che'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("n-proposal", f'n={n}'), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("inductive-step", f'Potrai disporre di massimo 8 righe per scrivere il tuo pseudo-codice; una volta terminato scrivi "return sj" (dove sj e` il massimo per un certo j) e capiro` che hai finito.'), "yellow", ["bold"])
    user_sol=TALinput(str, regex=f"^[\w]*[=]?[(,)\w/ \d +-]*$", sep='\n', TAc=TAc)[0]
    algo_index=0
    indices_set=set()
    indices_set.update(i for i in range(1,n+1))
    while (not 'return' in user_sol) and algo_index<=8 and len(indices_set)>1:
        algo_index+=1
        if 'max_in_sottoinsieme' in user_sol:
            check_command_subset(user_sol,n)
        elif 'confronto' in user_sol:
                check_argument_confronto(user_sol,n)
        if not ('max_in_sottoinsieme' in user_sol or 'confronto' in user_sol):
            TAc.print(LANG.render_feedback("wrong", f'Attenzione, ogni riga deve contenere una chiamata ad un oracolo.'), "red", ["bold"])
            exit(0)
        command_index=ll.indices(user_sol,n,cardinality)
        # print(f'command index {command_index}')
        temporary_set=set()
        for item in command_index:
            if not item in indices_set:
                TAc.print(LANG.render_feedback("error", f'attenzione, hai gia` fatto un controllo sull\'elemento s{item}...'), "red", ["bold"])
                exit(0)
            temporary_set.add(item)
        # print(temporary_set)
        max_elem=int(random.choice([i for i in temporary_set]))
        TAc.print(LANG.render_feedback("max-element", f'il massimo e` s{max_elem}'), "yellow", ["bold"])
        indices_set-=temporary_set
        indices_set.add(max_elem)
        # print(f'indices set {indices_set}')
        user_sol=TALinput(str, regex=f"^[\w]*[=]?[(,)\w/ \d +-]*$", sep='\n', TAc=TAc)[0]
    if 'return' in user_sol:
        check_correctness_max(indices_set,user_sol,max_elem,n)
    elif algo_index>=9:
        TAc.print(LANG.render_feedback("too-much-lines", f'Stai usando piu` righe del previsto.'), "red", ["bold"])
        exit(0)
    elif len(indices_set)==1:
        TAc.print(LANG.render_feedback("error", f'Hai gia` confrontato tutti gli elementi dell\'insieme, se controlli meglio ti accorgerai che il massimo e` s{max_elem}.'), "red", ["bold"])
        exit(0)
    exit(0)
else:
    TAc.print(LANG.render_feedback("start", 'Ti va di dimostrare formalmente che un insieme finito di numeri ha sempre un massimo? Cominciamo subito!'), "white", ["bold"])
    TAc.print(LANG.render_feedback("set-explain", 'Consideriamo l\'insieme S della forma S={s1,s2,s3,...,sn} con n>1. Qual e` il massimo dell\'insieme S? Per rispondere hai a disposizione ben 2 oracoli: \n- confronto(sj,sk) : confronta due elementi nell\'insieme S, ovvero sj ed sk e restituisce il maggiore dei due \n- max_in_sottoinsieme(j,k) : considera il sottoinsieme proprio di S costituito dagli elementi che vanno da sj fino ad sk (quindi j<=k) e restituisce il massimo tra questi. \nProva a combinare chiamate agli oracoli disponibili in modo da costruire il massimo. Potrai disporre di massimo 8 righe per scrivere il tuo pseudo-codice; una volta terminato scrivi "return sj" (dove sj e` il massimo per un certo j) e capiro` che hai finito.'), "yellow", ["bold"])
    n_tests=[2,3,4,10,20,30]
    
    TAc.print(LANG.render_feedback("correct", f'Ottimo! Hai costruito un pseudo-algoritmo per trovare il massimo in un insieme di n elementi.'), "green", ["bold"])
    exit(0)