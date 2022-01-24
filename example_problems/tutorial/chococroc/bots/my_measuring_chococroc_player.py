#!/usr/bin/env python3
from bot_lib import Bot
import chococroc_lib as cl

BOT = Bot(report_inputs=True,reprint_outputs=True)

while True:
    line = BOT.input()
    conf_string_choco='It is your turn to move from conf <chococroc(m='
    conf_string_nim = ' + nim(height='
    if conf_string_choco and conf_string_nim in line:
        index_end_choco=line.find(')', len(conf_string_choco)) #per avere tutti i valori tra le parentesi
        numbers_choco=(line[len(conf_string_choco):index_end_choco]).replace('n=', '')
        index_start_nim=line.find(conf_string_nim)
        index_end_nim=line.find(')', index_start_nim)
        numbers_nim=line[index_start_nim+len(conf_string_nim):index_end_nim]
        s,d = map(int, numbers_choco.split(',') ) #configurazione mappata su due variabili intere
        t =  int(numbers_nim)
        m,n,nim=cl.computer_decision_move(s,d,t)
        print(f"{m} {n} {nim}")
    if 'Since we played optimally' in line or 'The cases are two:' in line:
        exit(0)