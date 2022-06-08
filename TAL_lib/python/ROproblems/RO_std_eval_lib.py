#!/usr/bin/env python3
from sys import stderr
from typing import Optional, List, Dict, Callable
import termcolor 
from ansi2html import Ansi2HTMLConverter
ansi2html = Ansi2HTMLConverter(inline = True)

class std_eval_feedback:
    def __init__(self, task_number:int, pt_tot:int,pt_formato_OK:int,pt_feasibility_OK:int,pt_consistency_OK:int, COLOR_IMPLEMENTATION ="ANSI", new_line='\n'):
        self.COLOR_IMPLEMENTATION = COLOR_IMPLEMENTATION
        self.new_line = new_line
        self.task_number = task_number
        self.pt_tot = pt_tot
        self.pt_formato_OK = pt_formato_OK
        self.pt_feasibility_OK = pt_feasibility_OK
        self.pt_consistency_OK = pt_consistency_OK
        self.feedback_so_far = ""
        self.completed_feedback = False
    
    def colored(self, msg_text, *msg_rendering):
        if self.COLOR_IMPLEMENTATION == None:
            return msg_text
        if len(msg_rendering) == 0:
            ANSI_msg = msg_text
        else:
            if type(msg_rendering[-1]) == list:
                msg_style = msg_rendering[-1]
                msg_colors = msg_rendering[:-1]
            else:
                msg_style = []
                msg_colors = msg_rendering
            ANSI_msg = termcolor.colored(msg_text, *msg_colors, attrs=msg_style)
        if self.COLOR_IMPLEMENTATION == 'ANSI':
            colored_msg = ANSI_msg
        elif self.COLOR_IMPLEMENTATION == 'html':
            colored_msg = ansi2html.convert(ANSI_msg.replace(">", "&gt;").replace("<", "&lt;"), full=False).replace(self.new_line, "\n<br/>")
        else:
            assert self.COLOR_IMPLEMENTATION == None
        return colored_msg

    def evaluation_format(self, explanation, pt_safe:Optional[int] = None,pt_out:Optional[int] = None):
        pt_maybe = self.pt_tot-(pt_safe if pt_safe != None else 0)-(pt_out if pt_out != None else 0)
        index_pt=self.task_number-1
        self.feedback_so_far += "Totalizzi "
        self.feedback_so_far += self.colored(f"[punti sicuri: {pt_safe}]", "green", ["bold"]) + ", "
        self.feedback_so_far += self.colored(f"[punti aggiuntivi possibili: {pt_maybe}]", "blue", ["bold"]) + ", " 
        self.feedback_so_far += self.colored(f"[punti fuori portata: {pt_out}]", "red", ["bold"]) + self.colored(f"{self.new_line}Spiegazione: ", "cyan", ["bold"]) + explanation + self.colored(f"{self.new_line}")
        if pt_safe == None:
            pt_safe = 0
        if pt_out == None:
            pt_out = 0
        self.completed_feedback = {'pt_safe':pt_safe,'pt_maybe':pt_maybe,'pt_out':pt_out,'pt_available':self.pt_tot,'feedback_string':self.feedback_so_far}

   
    class goal:
        def __init__(self, goal_std_name, ad_hoc_name, answer_object):
            self.std_name = goal_std_name
            self.alias = ad_hoc_name
            self.answ = answer_object
        def __repr__(self):
            return f'Object goal({self.std_name=}, goal("{self.alias=}, goal("{self.answ=}'
        
    def load(self, long_answer_dict:Dict):
        goals = {}
        for std_name,obj_with_alias in long_answer_dict.items():
            goals[std_name] = self.goal(std_name, ad_hoc_name=obj_with_alias[1], answer_object=obj_with_alias[0])
        return goals

    def format_NO(self, goal, explanation):
        self.feedback_so_far += f"formato di `{goal.std_name}`: "+self.colored(f"NO{self.new_line}", "red", ["bold"])
        self.evaluation_format(explanation, pt_safe=None,pt_out=self.pt_tot)
        return False
        
    def format_OK(self, goal, positive_enforcement, note=None):
        self.feedback_so_far += f"formato di `{goal.std_name}`: "+self.colored(f"OK{self.new_line}", "green", ["bold"])
        if note != None:
            self.feedback_so_far += self.colored(f"    {self.new_line}-nota: ", "cyan", ["bold"]) + note
        
    def feasibility_NO(self, goal, explanation):
        self.feedback_so_far += f"ammissibilità di `{goal.std_name}`: "+self.colored(f"NO{self.new_line}", "red", ["bold"])
        self.evaluation_format(explanation, pt_safe=self.pt_formato_OK,pt_out=self.pt_tot-self.pt_formato_OK)
        return False
        
    def feasibility_OK(self, goal, positive_enforcement, note=None):
        self.feedback_so_far += f"ammissibilità di `{goal.std_name}`: "+self.colored(f"OK{self.new_line}", "green", ["bold"])
        if note != None:
            self.feedback_so_far += self.colored(f"    {self.new_line}-nota: ", "cyan", ["bold"]) + note
        
    def consistency_NO(self, goals, explanation):
        self.feedback_so_far += f"consistenza tra `{'` e `'.join([goal_std_name for goal_std_name in goals])}`: "+self.colored(f"NO{self.new_line}", "red", ["bold"])
        self.evaluation_format(explanation, pt_safe=self.pt_formato_OK+self.pt_feasibility_OK,pt_out=self.pt_tot-self.pt_formato_OK-self.pt_feasibility_OK)
        return False
        
    def consistency_OK(self, goal, positive_enforcement, note=None):
        self.feedback_so_far += f"ammissibilità di `{goal.std_name}`: "+self.colored(f"OK{self.new_line}", "green", ["bold"])
        if note != None:
            self.feedback_so_far += self.colored(f"    {self.new_line}-nota: ", "cyan", ["bold"]) + note


    def feedback_when_all_checks_passed(self):
        self.completed_feedback = self.evaluation_format(self.feedback_so_far, f"Quanto sottomesso{'' if self.task_number < 0 else ' per la Richiesta '+str(self.task_number)} ha superato tutti i miei controlli. Ovviamente in sede di esame non posso esprimermi sull'ottimalità di valori e di soluzioni immesse. Il mio controllo e supporto si è limitato alla compatibilità di formato, all'ammissibilità, e alla consistenza dei dati immessi.", pt_safe=self.pt_formato_OK + self.pt_feasibility_OK + self.pt_consistency_OK,pt_out=0)
        return self.completed_feedback

            
