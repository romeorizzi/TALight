#!/usr/bin/env python3
import string
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
import limiti_lib as ll
import random
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('seed',int),
    ('cardinality',str),
    ('verbose',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'never')

## START CODING YOUR SERVICE:
cardinality=ENV["cardinality"]
random.seed(ENV['seed'])
TAc.print(LANG.render_feedback("seed", f'# puoi richiamare questa particolare istanza specificando -aseed={ENV["seed"]}'), "yellow")
def base_case():
    user_command=TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0]
    if user_command!='s1' and user_command!='sn':
        TAc.print(LANG.render_feedback("wrong", f'# questa scrittura non la capisco o e` errata... prova a rispondere con "sj" per un certo j tale che sj appartiene ad S:'), "red", ["bold"])
        return base_case()
    else:
        return TAc.print(LANG.render_feedback("correct", 'Giusto! Infatti: \n- s1 appartiene ad S? Si! \n- ogni elemento sj in S e` tale che sj<=s1? Si, infatti S={s1} e s1<=s1'), "green", ["bold"])
def check_command_subset(stringa,n,cardinality,max_values):
    start,end=ll.args_subset(stringa)
    def check_argument_value(stringa,n):
        try:
            eval_str=eval(stringa,{'n':n})
            if not int(eval_str)==eval_str:
                TAc.print(LANG.render_feedback("wrong", f'# No, \'max_in_sottoinsieme\' prende come argomenti solo numeri interi (o espressioni numeriche, al piu` e` consentito l\'utilizzo della variabile n che qui vale {n}).'), "red", ["bold"])
                return 'error'
            else:
                int_value=int(eval_str)
                return int_value
        except:
            TAc.print(LANG.render_feedback("wrong", f'# No, \'max_in_sottoinsieme\' prende come argomenti solo numeri interi (o espressioni numeriche, al piu` e` consentito l\'utilizzo della variabile n che qui vale {n}).'), "red", ["bold"])
            return 'error'
    def check_argument_value_open(stringa,n,max_values):
        try:
            eval_str=eval(stringa,{'n':max(max_values)})
            # print(f'{eval_str}, {max(max_values)}')
            valutato=True
        except:
            valutato=False
        if valutato:
            if not int(eval_str)==eval_str:
                TAc.print(LANG.render_feedback("wrong", f'# No, \'max_in_sottoinsieme\' prende come argomenti solo numeri interi (o espressioni numeriche, al piu` e` consentito l\'utilizzo della variabile n).'), "red", ["bold"])
                return 'error'
            elif int(eval_str)>max(max_values) and max(max_values)!=1:
                TAc.print(LANG.render_feedback("wrong", f'# No, se |S|={max(max_values)} staresti richiamando un elemento che non appartiene ad S.'), "red", ["bold"])
                return 'error'
            else:
                return stringa
        else:
            TAc.print(LANG.render_feedback("wrong", f'# No, \'max_in_sottoinsieme\' prende come argomenti numeri interi (o espressioni numeriche, al piu` e` consentito l\'utilizzo della variabile n).'), "red", ["bold"])
            return 'error'
    start_value=check_argument_value(start,n) if cardinality!='open' else check_argument_value_open(start,n,max_values)
    end_value=check_argument_value(end,n) if cardinality!='open' else check_argument_value_open(end,n,max_values)
    if start_value=='error' or end_value=='error':
        return 'error'
    if cardinality=='open' and int(eval(start_value,{'n':max(max_values)}))==1 and eval(end_value,{'n':max(max_values)})>=max(max_values):
        TAc.print(LANG.render_feedback("wrong", f'# No, il sottoinsieme di cui mi hai chiesto di trovare il massimo potrebbe essere un sottoinsieme improprio!'), "red", ["bold"])
        return 'error'
    elif cardinality=='open' and int(eval(start_value,{'n':max(max_values)}))>eval(end_value,{'n':max(max_values)}):
        TAc.print(LANG.render_feedback("wrong", f'# No, tu non conosci la cardinalita` di S e potresti star richiamando \'max_in_sottoinsieme(j,k)\' con j>k'), "red", ["bold"])
        return 'error'
    if cardinality=='open':
        start_value=int(eval(start_value,{'n':n}))
        end_value=int(eval(end_value,{'n':n}))
    if start_value>end_value:
        TAc.print(LANG.render_feedback("wrong", f'# No, \'max_in_sottoinsieme(j,k)\' deve essere tale che j<=k'), "red", ["bold"])
        return 'error'
    elif start_value==1 and end_value==n:
        TAc.print(LANG.render_feedback("wrong", f'# No, il sottoinsieme di cui mi hai chiesto di trovare il massimo e` un sottoinsieme improprio!'), "red", ["bold"])
        return 'error'
    elif end_value>n or start_value>n:
        TAc.print(LANG.render_feedback("wrong", f'# Vedi, |S|={n} e tu mi hai chiesto di trovare il massimo di un sottoinsieme che contiene un elemento che non sta in S.'), "red", ["bold"])
        return 'error'
    return 'all_fine'
def check_command_confronto(user_command,n,cardinality,max_values):
    arg_1,arg_2=ll.args_confronto(user_command)
    def check_argument(argument,n):
        try:
            eval(argument,{'n':n})
            valutato=True
        except:
            valutato=False
        if valutato:
            if (not argument.isdigit()) or eval(argument,{'n':n})>n:
                TAc.print(LANG.render_feedback("wrong-input", f'# L\'oracolo "confronto(j,k)" prende come argomenti indici di due elementi dell\'insieme S della forma j per un certo j<=n'), "red", ["bold"])
                return 'error'
            elif argument[1:].isdigit() and int(argument[1:])>n:
                TAc.print(LANG.render_feedback("wrong-input", f'# No, mi stai chiedendo di calcolare il massimo di un elemento che non sta in S.'), "red", ["bold"])
                return 'error'
        else:
            TAc.print(LANG.render_feedback("wrong", f'# No, "confronto" prende come argomenti  numeri interi o espressioni numeriche, e` consentito anche l\'utilizzo della variabile n).'), "red", ["bold"])
            return 'error'
    start=check_argument(arg_1,n)
    end=check_argument(arg_2,n)
    if start=='error' or end=='error':
        return 'error'
    def check_argument_open(argument,max_values):
        eval_arg=eval(argument,{'n':max(max_values)})
        if eval_arg>max(max_values):
            TAc.print(LANG.render_feedback("wrong-input", f'# No, se n fosse {max(max_values)} staresti richiamando un elemento che non appartiene ad S.'), "red", ["bold"])
            return 'error'
    if cardinality=='open':
        start=check_argument_open(arg_1,max_values)
        end=check_argument_open(arg_2,max_values)
    if start=='error' or end=='error':
        return 'error'
    return 'all_fine'

def check_first_command_confronto_open(user_command):
    arg_1,arg_2=ll.args_confronto(user_command)
    # print(f'#  arg 1: {arg_1}, arg 2: {arg_2}')
    def check_argument(argument):
        try:
            arg_value=eval(argument)
            riuscito=True
        except:
            riuscito=False
        if riuscito:
            if not int(arg_value)==arg_value:
                print('sono qui')
                TAc.print(LANG.render_feedback("wrong", f'# No, \'confronto\' prende come argomenti solo numeri interi o espressioni numeriche, e` consentito anche l\'utilizzo della variabile n.'), "red", ["bold"])
                return 'error'
            elif not arg_value in [1,2]:
                TAc.print(LANG.render_feedback("wrong-input", f'# No, se n fosse {random.randint(1,5)+int(argument)} staresti richiamando un elemento che non appartiene ad S.'), "red", ["bold"])
                return 'error'
            return int(argument)
        else:
            if not argument in ['n','n-1']:
                TAc.print(LANG.render_feedback("wrong-input", f'# No, \'confronto\' prende come argomenti solo numeri interi o espressioni numeriche, e` consentito anche l\'utilizzo della variabile n.'), "red", ["bold"])
                return 'error'
            return argument
    start=check_argument(arg_1)
    end=check_argument(arg_2)
    return start,end

def check_max_after_return(indices_list,user_command,max_elem,n):
    one_correct_sol=[]
    for i in range(len(indices_list)):
        for k in range(1,n+1):
            if k not in indices_list[i]:
                one_correct_sol.append(False)
                break
        else:
            one_correct_sol.append(True)
    if not True in one_correct_sol:
        TAc.print(LANG.render_feedback("wrong", f'# Attenzione, non hai confrontato tutti gli elementi di S tra di loro.'), "red", ["bold"])
        exit(0)
    non_valutato=True
    try:
        user_max=eval(user_command[7:],{'n':n})
        non_valutato=False
        if int(user_max)==max_elem:
            TAc.print(LANG.render_feedback("correct", f'Ottimo! Il massimo dell\'insieme S e` s{max_elem}.'), "green", ["bold"])
            exit(0)
        elif user_max>n:
            TAc.print(LANG.render_feedback("error", f'# No, l\'elemento s{user_max}, non appartiene all\'insieme S.'), "red", ["bold"])
            exit(0)
        else:
            TAc.print(LANG.render_feedback("error", f'# No, il massimo dell\'insieme S non e` s{user_max}, e` s{max_elem}.'), "red", ["bold"])
            exit(0)
    except:
        if non_valutato:
            TAc.print(LANG.render_feedback("error", f'# Non riesco a decifrare quello hai scritto, la sintassi giusta e` "return j" per una certa j<={n}, prova a riscrivere:'), "red", ["bold"])
            exit(0)
def check_argument_value_subset_open(stringa):
    try:
        eval_str=eval(stringa, {'n':2})
        riuscito=True
    except:
        riuscito=False
    if riuscito:
        if not int(eval_str)==eval_str:
            TAc.print(LANG.render_feedback("wrong", f'# No, \'max_in_sottoinsieme\' prende come argomenti solo numeri interi o espressioni numeriche, e` consentito anche l\'utilizzo della variabile n.'), "red", ["bold"])
            return 'error'
        elif not int(eval_str) in [1,2]:
            TAc.print(LANG.render_feedback("wrong", f'# No, questa chiamata all\'oracolo non sarebbe valida per n=2.'), "red", ["bold"])
            return 'error'
        else:
            try:
                eval_str=eval(stringa)
                int_value=int(eval_str)
                return int_value
            except:
                return stringa
    else:
        TAc.print(LANG.render_feedback("wrong", f'# No, \'max_in_sottoinsieme\' prende come argomenti solo numeri interi o espressioni numeriche, e` consentito anche l\'utilizzo della variabile n.'), "red", ["bold"])
        return 'error'
def check_first_command_subset_open(stringa):
    start,end=ll.args_subset(stringa)
    start_value=check_argument_value_subset_open(start)
    end_value=check_argument_value_subset_open(end)
    if start_value=='error' or end_value=='error':
        return 'error','error'
    cond_1=type(start_value)==int and type(end_value)==int and start_value>end_value
    cond_2=start_value=='n' and not end_value=='n'
    cond_3=start_value==2 and end_value=='n-1'
    cond_4=start_value=='n-1' and not end_value=='n'
    cond_5= start_value=='n-1' and end_value=='n'
    if cond_1:
        TAc.print(LANG.render_feedback("wrong", f'# No, \'max_in_sottoinsieme(j,k)\' deve essere tale che j<=k'), "red", ["bold"])
        return 'error','error'
    if cond_2:
        TAc.print(LANG.render_feedback("wrong", f'# No, la tua chiamata all\'oracolo non sarebbe valida per nessun valore di n.'), "red", ["bold"])
        return 'error','error'
    elif cond_3:
        TAc.print(LANG.render_feedback("wrong", f'# No, se n=2 allora n-1=1 e 2>1 (deve invece essere max_in_sottoinsieme(j,k) con j<k)'), "red", ["bold"])
        return 'error','error'
    elif cond_4:
        if type(end_value)==int:
            TAc.print(LANG.render_feedback("wrong", f'# No, se n={end_value+random.randint(3,6)} allora n-1>{end_value} (deve invece essere max_in_sottoinsieme(j,k) con j<k)'), "red", ["bold"])
            return 'error','error'
    elif start_value==1 and end_value=='n':
        TAc.print(LANG.render_feedback("wrong", f'# No, il sottoinsieme di cui mi hai chiesto di trovare il massimo e` un sottoinsieme improprio!'), "red", ["bold"])
        return 'error','error'
    elif cond_5:
        TAc.print(LANG.render_feedback("wrong", f'# No, se n=2 mi staresti chiedendo di trovare il massimo di un sottoinsieme improprio!'), "red", ["bold"])
        return 'error','error'
    return start_value,end_value
def insert_command(n,cardinality,max_values):
    user_command=TALinput(str, regex=f"^[(,)\w/ =\d +-]*$", sep='\n', TAc=TAc)[0]
    if user_command=='end':
        exit(0)
    if 'max_in_sottoinsieme' in user_command:
        check=check_command_subset(user_command,n,cardinality,max_values)
        if check=='error':
            TAc.print(LANG.render_feedback("wrong", f'{error_message}'), "grey", ["bold"])
            return insert_command(n,cardinality,max_values)
        else: 
            return user_command
    elif 'confronto' in user_command:
        check=check_command_confronto(user_command,n,cardinality,max_values)
        if check=='error':
            TAc.print(LANG.render_feedback("wrong", f'{error_message}'), "grey", ["bold"])
            return insert_command(n,cardinality,max_values) 
        else: 
            return user_command
    elif 'return' in user_command:
        return user_command
    else:
        TAc.print(LANG.render_feedback("wrong", f'# Attenzione, ogni riga deve contenere una chiamata ad un oracolo.'), "red", ["bold"])
        TAc.print(LANG.render_feedback("wrong", f'{error_message}'), "grey", ["bold"])
        return insert_command(n,cardinality,max_values)
error_message='# non considerero` questa risposta, puoi continuare al tua ricerca del massimo (altrimenti, se vuoi uscire, scrivi \'end\'):'
if cardinality!='open':
    n=random.randint(2,10) if cardinality=='you_choose' else int(cardinality)
    TAc.print(LANG.render_feedback("start", '# Ti va di dimostrare formalmente che un insieme finito di numeri ammette sempre massimo? Lo faremo insieme, sara` una dimostrazione per induzione. Dovrai astrarre la capacita` di trovare il massimo in modo da assicurarci che qualsiasi sia l\'insieme S={s1,s2,s3,...,sn} di n>0 elementi che ti viene proposto tu sappia trovare sempre il massimo.'), "white", ["bold"])
    TAc.print(LANG.render_feedback("set-explain", '# Consideriamo insiemi della forma S={s1,s2,s3,...,sn}.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("base-case", f'# CASO BASE: se n=1, qual e` il massimo dell\'insieme S?'), "yellow", ["bold"])
    base_case()
    if n==1:
        exit(0)
    TAc.print(LANG.render_feedback("inductive-step", f'# PASSO INDUTTIVO: se n>1, qual e` il massimo dell\'insieme S? Per rispondere hai a disposizione ben 2 oracoli: \n#     - confronto(j,k) : confronta due elementi nell\'insieme S, ovvero sj ed sk e restituisce il maggiore dei due \n#     - max_in_sottoinsieme(j,k) : considera il sottoinsieme proprio di S costituito dagli elementi che vanno da sj fino ad sk (quindi j<=k) e restituisce il massimo tra questi. \n# Prova a combinare chiamate agli oracoli disponibili in modo da costruire il massimo sapendo che'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("n-proposal", f'n={n}'), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("inductive-step", f'# Una volta terminato scrivi "return j" (per indicarmi che il massimo dell\'insieme S e` sj) e capiro` che hai finito.'), "yellow", ["bold"])
    all_elem_in_set=[i for i in range(1,n+1)]
    checked_set=random.sample(all_elem_in_set,k=n)
    # print(f'elementi ordinati: {checked_set}')
    user_command=insert_command(n,cardinality,None)
    indices_list=[]
    while not 'return' in user_command:
        indices_list,max_elem=ll.core_function_max_finite_set_proof(indices_list,user_command,checked_set,n,cardinality)
        # print(f'indices list {indices_list}')
        TAc.print(LANG.render_feedback("max-element", f'# il massimo e` s{max_elem}'), "yellow", ["bold"])
        user_command=insert_command(n,cardinality,None)
    if 'return' in user_command:
        max_elem=checked_set[0]
        check=check_max_after_return(indices_list,user_command,max_elem,n)
    if ENV["verbose"]:
        list_to_print=''
        for i in range(n-1):
            list_to_print+=(' s'+str(checked_set[i])+' <')
        TAc.print(LANG.render_feedback("proof", f'Infatti: {list_to_print} s{checked_set[n-1]}'), "grey", ["bold"])
        exit(0)
    else:
        exit(0)
else:
    TAc.print(LANG.render_feedback("start", 'Ti va di dimostrare formalmente che un insieme finito di numeri ha sempre un massimo? Cominciamo subito!'), "white", ["bold"])
    TAc.print(LANG.render_feedback("set-explain", 'Consideriamo l\'insieme S della forma S={s1,s2,s3,...,sn} con n>1. Qual e` il massimo dell\'insieme S? Per rispondere hai a disposizione ben 2 oracoli: \n- confronto(j,k) : confronta due elementi nell\'insieme S, ovvero sj ed sk e restituisce il maggiore dei due \n- max_in_sottoinsieme(j,k) : considera il sottoinsieme proprio di S costituito dagli elementi che vanno da sj fino ad sk (quindi j<=k) e restituisce il massimo tra questi. \nProva a richiamare gli oracoli disponibili combinandoli in modo da costruire il massimo. Una volta terminato scrivi "return j" (per indicarmi che il massimo dell\'insieme S e` sj) e capiro` che hai finito.'), "yellow", ["bold"])
    def first_input_open():
        user_command=TALinput(str, regex=f"^[(,)\w/ =\d +-]*$", sep='\n', TAc=TAc)[0]
        if 'max_in_sottoinsieme' in user_command:
            start,end=check_first_command_subset_open(user_command)
            if start=='error':
                TAc.print(LANG.render_feedback("wrong", f'{error_message}'), "grey", ["bold"])
                return first_input_open()
            else: 
                return user_command,start,end
        elif 'confronto' in user_command:
            start,end=check_first_command_confronto_open(user_command)
            if start=='error' or end=='error':
                TAc.print(LANG.render_feedback("wrong", f'{error_message}'), "grey", ["bold"])
                return first_input_open()
            else: 
                return user_command,start,end
        else:
            TAc.print(LANG.render_feedback("wrong", f'# Attenzione, ogni riga deve contenere una chiamata ad un oracolo.'), "red", ["bold"])
            TAc.print(LANG.render_feedback("wrong", f'{error_message}'), "grey", ["bold"])
            return first_input_open()
    user_command,start,end=first_input_open()
    n=random.randint(2,10)
    TAc.print(LANG.render_feedback("n-proposal", f'n={n}'), "yellow", ["reverse"])
    all_elem_in_set=[i for i in range(1,n+1)]
    checked_set=random.sample(all_elem_in_set,k=n)
    print(f'elementi ordinati: {checked_set}')
    indices_list=[]
    indices_list.append({i for i in range(eval(str(start),{'n':n}),eval(str(end),{'n':n})+1)})
    # print(indices_list)
    max_values=set()
    first_indices=[i for i in range(eval(str(start),{'n':n}),eval(str(end),{'n':n})+1)]
    position_first_max=[checked_set.index(item) for item in first_indices]
    max_elem=checked_set[min(position_first_max)]
    if eval(str(end),{'n':n})<n and end!=2:
        max_values.add(max_elem+1)
    elif eval(str(end),{'n':n})==n and end!=2:
        max_values.add(max_elem)
    elif max_elem==1:
        max_values.add(2)
    else:
        max_values.add(2)
    TAc.print(LANG.render_feedback("max-element", f'# il massimo e` s{max_elem}'), "yellow", ["bold"])
    user_command=insert_command(n,cardinality,max_values)
    while not 'return' in user_command:
        indices_list,max_elem=ll.core_function_max_finite_set_proof(indices_list,user_command,checked_set,n,cardinality)
        max_values.add(max_elem)
        # print(f'indices list {indices_list}')
        TAc.print(LANG.render_feedback("max-element", f'# il massimo e` s{max_elem}'), "yellow", ["bold"])
        user_command=insert_command(n,cardinality,max_values)
    if 'return' in user_command:
        max_elem=checked_set[0]
        check_max_after_return(indices_list,user_command,max_elem,n)
    exit(0)