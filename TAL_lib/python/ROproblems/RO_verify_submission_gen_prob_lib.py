#!/usr/bin/env python3
from sys import stderr
from typing import Optional, List, Dict, Callable
from types import SimpleNamespace
from copy import deepcopy

class verify_submission_gen:
    def __init__(self, SEF,input_data_assigned:Dict, long_answer_dict:Dict, oracle_response:Dict = None):
        self.I = SimpleNamespace(**input_data_assigned)
        self.goals = SEF.load(long_answer_dict)
        self.long_answer_dict = long_answer_dict
        self.oracle_response = oracle_response

    def verify_format(self, SEF):
        """In realtà questo tipo di controllo è attualmente demandato alla funzione check_and_standardization_of_request_answer_consistency  del modulo RO_std_io_lib.py
           Preferisco tuttavia richiamarlo quì perchè:
              1. non è del tutto chiaro (anche in relazione all'esperienza d'uso che avviene dentro i fogli Jupyther, il messaggio prodotto dalla funzione check_and_standardization_of_request_answer_consistenc  al momento è troppo severo, e d'altronde sono messaggi del modulo multilanguage che in questo momento non intedo toccare, ma posso duplicare il codice di quella parte e forse quella è la soluzione migliore, ma a quel punto la domanda è perchè non portare quì il controllo di tipo  togliendolo da  check_and_standardization_of_request_answer_consisten) quale possa essere il suo miglior collocamento
              2. come promemoria che vogliamo inventarci modi per portare a fattor comune controlli da problemi diversi.
           Tuttavia, per quanto riguarda 2, la via importante è che in questo modulo si definiscano delle funzioni general purpose per fare controlli sufficientemente generali (per definizione di un qualche linguaggio minimale e/oppure passando ad esse funzioni che fanno il controllo). Ma certo trovare delle buone soluzioni (con intelligenti compromessi) avrebbe il doppio vantaggio di sgravare il lavoro del problem maker e di offrire un'esperienza d'uso più standardizzata allo studente/problem solver.
        """
        for g in self.goals:
            if self.long_answer_dict[g] == 'int':
                if type(g.answ) != int:
                    return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
                SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto", f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")            
        return True
                
    def verify_feasibility(self, SEF):
        return True
                
    def verify_consistency(self, SEF):
        return True
                
    def verify_optimality(self, SEF):
        return True
                
    def set_up_and_cash_handy_data(self):
        pass       

    def verify_submission(self, SEF):
        if not self.verify_format(SEF):
            return whole_feedback_dict(SEF.non_spoilering_feedback)
        self.set_up_and_cash_handy_data()
        if not self.verify_feasibility(SEF):
            return whole_feedback_dict(SEF.non_spoilering_feedback)
        if not self.verify_consistency(SEF):
            return whole_feedback_dict(SEF.non_spoilering_feedback)
        also_optimal = self.verify_optimality(SEF)
        feedback_dict = whole_feedback_dict(SEF.feedback_when_all_non_spoilering_checks_passed())
        if also_optimal:
            feedback_dict['spoilering']['feedback_string'] += "(also optimality was checked for the positive, all points are safe)"
            feedback_dict['spoilering']['pt_safe'] += feedback_dict['spoilering']['pt_maybe']
        else:
            feedback_dict['spoilering']['feedback_string'] = SEF.all_feedback_so_far
            feedback_dict['spoilering']['pt_out'] += feedback_dict['spoilering']['pt_maybe']
        feedback_dict['spoilering']['pt_maybe'] = 0
        return feedback_dict

def whole_feedback_dict(non_spoilering_feedback):
    feedback_dict = {}
    feedback_dict['non_spoilering'] = non_spoilering_feedback
    feedback_dict['spoilering'] = deepcopy(non_spoilering_feedback)
    return feedback_dict
