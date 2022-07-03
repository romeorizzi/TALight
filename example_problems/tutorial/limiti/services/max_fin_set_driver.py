#!/usr/bin/env python3
from sys import exit
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper
import limiti_lib as ll
from numpy import array

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('reference_set',str),
    ('instance_id',int),
    ('seed',int),
    ('set_cardinality',int),
    ('download',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

## START CODING YOUR SERVICE:
reference_set=ENV["reference_set"]
source=ENV["source"]
seed=ENV["seed"]
set_cardinality=ENV["set_cardinality"]

if reference_set=='generic':
    def step1():
        user_sol=TALinput(str, regex=f"^((\S)+)$", sep=None, TAc=TAc)[0]
        if user_sol!='s1':
            TAc.print(LANG.render_feedback("wrong", f'questa scrittura non la capisco o e` errata... prova con "sj" per una certa j'), "red", ["bold"])
            return step1()
        else:
            return TAc.print(LANG.render_feedback("correct", 'Giusto! Infatti: \n- s1 appartiene ad S \n- ogni elemento sj in S e` tale che sj<=s1 (infatti S={s1} e s1<=s1)'), "green", ["bold"])
    def check_command(stringa,n):
        if 'sottoinsieme' in stringa:
            posiz_start=stringa.find("sottoinsieme")+13
            if not stringa[posiz_start].isdigit():
                TAc.print(LANG.render_feedback("wrong", f'\'sottoinsieme\' prende come argomento solo numeri interi'), "red", ["bold"])
                exit(0)
            start=int(stringa[posiz_start])
            posiz_end=stringa[posiz_start+2]
            if not posiz_end.isdigit():
                TAc.print(LANG.render_feedback("wrong", f'\'sottoinsieme\' prende come argomento solo interi'), "red", ["bold"])
                exit(0)
            end=int(posiz_end)
            if start>=end:
                TAc.print(LANG.render_feedback("wrong", f'No, \'sottoinsieme(j,k)\' deve essere tale che j<k'), "red", ["bold"])
                exit(0)
            if start==1 and end==n:
                TAc.print(LANG.render_feedback("wrong", f'No, il sottoinsieme di cui mi hai chiesto di trovare il massimo e` un sottoinsieme improprio!'), "red", ["bold"])
                exit(0)
            if end>n or start>n:
                TAc.print(LANG.render_feedback("wrong", f'No, mi hai chiesto di trovare il massimo di un sottoinsieme che contiene un elemento maggiore di s{n}'), "red", ["bold"])
                exit(0)
        else:
            assert 'confronto' in stringa
            posiz_1=stringa.find("confronto")+10
            # comma_position=stringa.find(',')
    TAc.print(LANG.render_feedback("start", 'Ti va di dimostrare formalmente che un insieme finito di numeri ha sempre un massimo? Lo faremo insieme, sara` una dimostrazione per induzione. Dovrai astrarre la capacita` di trovare il massimo in modo da assicurarci che qualsiasi sia l\'insieme S={s1,s2,s3,...,sn} di n>0 elementi che ti viene proposto tu sappia trovare sempre il massimo.'), "white", ["bold"])
    TAc.print(LANG.render_feedback("set-explain", 'Consideriamo insiemi della forma S={s1,s2,s3,...,sn}.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("base-case", f'CASO BASE: se n=1, qual e` il massimo dell\'insieme S?'), "yellow", ["bold"])
    step1()
    TAc.print(LANG.render_feedback("inductive-step", f'PASSO INDUTTIVO: se n>1, qual e` il massimo dell\'insieme S? Per rispondere ora ti puoi servire di ben 2 oracoli: \n- confronto(sj,sk) : confronta due elementi nell\'insieme S, ovvero sj ed sk e restituisce il maggiore dei due \n- sottoinsieme(j,k) : considera il sottoinsieme proprio di S costituito dagli elementi che vanno da sj fino ad sk (quindi j<k) e restituisce il massimo tra questi. \nProva a combinare gli oracoli che ti offro (con i corrispettivi argomenti) in modo da costruire una sorta di algoritmo che trovi il massimo in base alla cardinalita` n che ti viene proposta; e` consentito inoltre l\'assegnamento delle variabili se necessario [ad esempio nome_variabile=confronto(sj,sk)]. Hai a disposizione massimo 8 righe per poter scrivere il tuo pseudo-codice; una volta terminato scrivi in una nuova riga "end" e capiro` che hai finito.'), "yellow", ["bold"])
    n=[2,3,4,5,6]
    for i in range(len(n)):
        TAc.print(LANG.render_feedback("n-proposal", f'n={n[i]}:'), "yellow", ["bold"])
        user_sol=''
        user_algo=[]
        algo_index=0
        while user_sol!='end' and algo_index<=8:
            user_sol=TALinput(str, regex=f"^[\w]*[=]?(confronto|sottoinsieme)+[(,)\w/\d +-]+$", sep='\n', TAc=TAc)[0]
            if user_sol!='end':
                if not ('sottoinsieme' in user_sol or 'confronto' in user_sol):
                    TAc.print(LANG.render_feedback("wrong", f'No, ogni riga deve contenere una chiamata ad un oracolo.'), "red", ["bold"])
                    exit(0)
                user_algo.append(user_sol.replace(" ",""))
            algo_index+=1
        # print(f'--> per debug, user_algo: {user_algo}')
        len_algo=len(user_algo)
        indices_set=[]
        variables_set={}
        for j in range(len_algo):
            check_command(user_algo[j],n[i])
            command_index=ll.indices(user_algo[j])
            if '=' in user_algo[j]:
                equal_pos=user_algo[j].find('=')
                variable_name=str(user_algo[j][:equal_pos])
                for indice in range(1,n[i]+1):
                    if variable_name=='s'+str(indice):
                        TAc.print(LANG.render_feedback("wrong", f'No, hai usato come variabile di assegnazione un elemento dell\'insieme S.'), "red", ["bold"])
                        exit(0)
                variables_set[variable_name]=command_index
            temporary_set=set()
            to_remove=[]
            for item in command_index:
                if type(item)==str:
                    if not item in variables_set:
                        TAc.print(LANG.render_feedback("wrong", f'Hai richiamato la variabile {item} che pero` non hai mai definito.'), "red", ["bold"])
                        exit(0)
                    if not variables_set[item] in indices_set:
                        TAc.print(LANG.render_feedback("wrong", f'Hai richiamato piu` volte {item}, pseudo-algoritmo non molto efficiente.'), "red", ["bold"])
                        exit(0)
                    indices_set.remove(variables_set[item])
                    temporary_set.update(variables_set[item])
                    to_remove.append(item)
                else:
                    temporary_set.add(item)
            if bool(to_remove):
                for elem in to_remove:
                    # print(elem)
                    command_index.remove(elem)
                command_index.update(temporary_set)
            indices_set.append(temporary_set)
            print(indices_set)
        if len(indices_set)!=1:
            TAc.print(LANG.render_feedback("wrong", f'No, il tuo pseudo-algoritmo non trova il massimo.'), "red", ["bold"])
            exit(0)
        else:
            for k in range(1,n[i]+1):
                if k not in indices_set[0]:
                    TAc.print(LANG.render_feedback("wrong", f'No, non hai considerato tutti gli elementi di S nel tuo pseudo-algoritmo (ad esempio s{k}).'), "red", ["bold"])
                    exit(0)
            check_array=list(indices_set[0])
            correct_array=[k for k in range(1,n[i]+1)]
            if check_array!=correct_array:
                TAc.print(LANG.render_feedback("wrong", f'No.'), "red", ["bold"])
                exit(0)
        TAc.print(LANG.render_feedback("correct", f'Ottimo! Hai costruito un pseudo-algoritmo per trovare il massimo in un insieme di {n[i]} elementi.'), "green", ["bold"])
    exit(0)

if source=='catalogue':
    set_values = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension='txt')
    TAc.print(LANG.render_feedback("instance", f'# instance_id: {ENV["instance_id"]} \n# Dati i seguenti numeri: \n{set_values}'),  "yellow", ["bold"])
    instance=ll.instance_to_array(set_values)
    output_filename = f"instance_catalogue_{ENV['instance_id']}_max_fin_set.txt"
else:
    assert source=='randgen'
    instance=array(ll.instance_randgen(set_cardinality,reference_set,seed),dtype='str')
    set_values='\n'.join(instance)
    TAc.print(LANG.render_feedback("start", f'# seed: {ENV["seed"]} \n# Dati i seguenti numeri: \n{set_values}'), "yellow", ["bold"])
    output_filename = f"instance_{seed}_max_fin_set.txt"
if ENV["download"]:
    TALf.str2output_file(set_values,output_filename)
instance=ll.instance_to_number(instance)
max_value=max(instance)
# print(instance_str[max_value])
TAc.print(LANG.render_feedback("max", f'# determina il massimo:'), "yellow", ["bold"])
user_max=eval(TALinput(str, regex=f"^([+-]?[.\d]*)$", sep=None, TAc=TAc)[0])
# controllare soluzione studente
if user_max==max_value:
    TAc.print(LANG.render_feedback("correct", f'Ottimo! {max_value} e` nell\'insieme e non ci sono numeri maggiori di lui, quindi e` un massimo.'), "green", ["bold"])
    exit(0)
elif user_max not in instance:
    TAc.print(LANG.render_feedback("wrong", f'No, {user_max} non e` nell\'insieme quindi non puo` essere un massimo!'), "red", ["bold"])
    exit(0)
else:
    elem=instance[0]
    grater_numbers=[]
    for i in range(set_cardinality):
        if instance[i]>user_max:
            grater_numbers.append(instance[i])
    grater_numbers.sort()
    grater_number=grater_numbers[(len(grater_numbers)-1)//2]
    TAc.print(LANG.render_feedback("wrong", f'No, ad esempio {grater_number} e` piu` grande di {user_max} quindi non puo` essere un massimo!'), "red", ["bold"])
    exit(0)