#!/usr/bin/env python3
from sys import stderr
from typing import Optional, List, Dict, Callable
import termcolor 
from ansi2html import Ansi2HTMLConverter
ansi2html = Ansi2HTMLConverter(inline = True)

class std_eval_feedback:
    def __init__(self, ENV, oracle_dict = None):
        self.color_implementation = ENV["color_implementation"]
        self.new_line = '\n' if ENV["color_implementation"] == "ANSI" else '\\n'
        self.with_positive_enforcement = ENV["with_positive_enforcement"]
        self.with_notes = ENV["with_notes"]
        self.task_number = ENV["task"]
        self.pt_tot = ENV["pt_tot"]
        self.pt_formato_OK = ENV["pt_formato_OK"]
        self.pt_feasibility_OK = ENV["pt_feasibility_OK"]
        self.pt_consistency_OK = ENV["pt_consistency_OK"]
        self.non_spoilering_feedback_so_far = ""
        self.all_feedback_so_far = ""
        self.oracle_dict = oracle_dict

    def feedback_append(self, last_feedback_msg:str, spoilering = False):
        self.all_feedback_so_far += last_feedback_msg
        if not spoilering:
            self.non_spoilering_feedback_so_far += last_feedback_msg
        #print(f"current feedback={self.all_feedback_so_far}",file=stderr)
    
    def colored(self, msg_text, *msg_rendering):
        if self.color_implementation == None:
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
        if self.color_implementation == 'ANSI':
            colored_msg = ANSI_msg
        elif self.color_implementation == 'html':
            colored_msg = ansi2html.convert(ANSI_msg.replace(">", "&gt;").replace("<", "&lt;"), full=False).replace(self.new_line, "\n<br/>")
        else:
            assert self.color_implementation == None
        return colored_msg

    def evaluation_format(self, explanation, pt_safe:Optional[int] = None,pt_out:Optional[int] = None):
        pt_maybe = self.pt_tot-(pt_safe if pt_safe != None else 0)-(pt_out if pt_out != None else 0)
# Note: for web renditions in the `esami-RO-private` project use:
#        index_pt=self.task_number-1
#        arr_point[index_pt]=pt_safe
#        file = open("points.txt", "w")
#        file.write(str(arr_point))
#        file.close()
        self.summary_of_scores = self.colored(f"{self.new_line}Totalizzi ", ["bold"]) + \
                               self.colored(f"[punti sicuri: {pt_safe}]", "green", ["bold"]) + ", " + \
                               self.colored(f"[punti aggiuntivi possibili: {pt_maybe}]", "blue", ["bold"]) + ", " + \
                               self.colored(f"[punti fuori portata: {pt_out}]", "red", ["bold"])
        self.last_explanation = self.colored(f"{self.new_line}Spiegazione: ", "cyan", ["bold"]) + explanation + self.colored(f"{self.new_line}")
        self.feedback_append(self.summary_of_scores)
        self.feedback_append(self.last_explanation)
        if pt_safe is None:
            pt_safe = 0
        if pt_out is None:
            pt_out = 0
        self.non_spoilering_feedback = {'pt_safe':pt_safe,'pt_maybe':pt_maybe,'pt_out':pt_out,'pt_available':self.pt_tot,'feedback_string':self.non_spoilering_feedback_so_far,'summary-of-scores':self.summary_of_scores,'last_explanation':self.last_explanation}

   
    class goal:
        def __init__(self, goal_std_name, ad_hoc_name, answer_object):
            self.std_name = goal_std_name
            self.alias = ad_hoc_name
            self.answ = answer_object
        def __repr__(self):
            return f'Object goal(self.std_name={self.std_name}, self.alias={self.alias}, self.answ={self.answ})'
        
    def load(self, long_answer_dict:Dict):
        goals = {}
        for std_name,obj_with_alias in long_answer_dict.items():
            goals[std_name] = self.goal(std_name, ad_hoc_name=obj_with_alias[1], answer_object=obj_with_alias[0])
        return goals

    
    def voice_NO(self, voice:str, explanation:str, spoilering = False):
        self.feedback_append(f"• {voice}: "+self.colored(f"NO.", "red", ["bold"])+self.colored(f".", "red")+self.colored(f".", "magenta") + self.colored(f".(motivo: ", "magenta", ["bold"]) + explanation + self.colored(")", "magenta", ["bold"]) + self.colored(self.new_line), spoilering = spoilering)

    def voice_OK(self, voice:str, positive_enforcement:str, note:str, spoilering = False):
        self.feedback_append(f"• {voice}: "+self.colored(f"OK", "green", ["bold"]), spoilering = spoilering)
        if self.with_positive_enforcement and len(positive_enforcement) > 0:
            self.feedback_append(self.colored(".", "green", ["bold"])+self.colored(f"..(infatti: ", "green") + positive_enforcement + self.colored(")", "green"), spoilering = spoilering)
        if self.with_notes and len(note) > 0:
            self.feedback_append(self.colored(".", "green", ["bold"])+self.colored(f".", "green")+self.colored(f".", "cyan") + self.colored(f".(nota: ", "cyan", ["bold"]) + note + self.colored(")", "cyan", ["bold"]), spoilering = spoilering)
        self.feedback_append(self.colored(self.new_line), spoilering = spoilering)
        
    def format_NO(self, goal, explanation):
        self.voice_NO(f"Formato di `{goal.alias}`", explanation)
        self.evaluation_format(explanation, pt_safe=None,pt_out=self.pt_tot)
        return False
        
    def format_OK(self, goal, positive_enforcement, note):
        self.voice_OK(f"Formato di `{goal.alias}`", positive_enforcement, note)
        
    def feasibility_NO(self, goal, explanation):
        self.voice_NO(f"Ammissibilità di `{goal.alias}`", explanation)
        self.evaluation_format(explanation, pt_safe=self.pt_formato_OK,pt_out=self.pt_tot-self.pt_formato_OK)
        return False
        
    def feasibility_OK(self, goal, positive_enforcement, note):
        self.voice_OK(f"Ammissibilità di `{goal.alias}`", positive_enforcement, note)
        
    def consistency_NO(self, goals, explanation):
        self.voice_NO(f"Consistenza tra `{'` e `'.join([goal_std_name for goal_std_name in goals])}`", explanation)
        pt_safe = self.pt_formato_OK + self.pt_feasibility_OK
        self.evaluation_format(explanation, pt_safe=pt_safe,pt_out=self.pt_tot-pt_safe)
        return False
        
    def consistency_OK(self, goals, positive_enforcement, note):
        self.voice_OK(f"Consistenza tra `{'` e `'.join([goal_std_name for goal_std_name in goals])}`", positive_enforcement, note)

    def optimality_NO(self, goal, explanation):
        # as for now, comment/decomment:
        self.voice_NO(f"Ottimalità di `{goal.alias}`", explanation, spoilering = True)
        #self.voice_NO(f"Ottimalità di `{goal.alias}`", explanation, spoilering = False)
        pt_safe = self.pt_formato_OK + self.pt_feasibility_OK + self.pt_consistency_OK
        #self.evaluation_format(explanation,pt_safe=pt_safe,pt_out=self.pt_tot-pt_safe)
        return False
        
    def optimality_OK(self, goal, positive_enforcement, note):
        # as for now, comment/decomment:
        self.voice_OK(f"Ottimalità di `{goal.alias}`", positive_enforcement, note, spoilering = True)
        #self.voice_OK(f"Ottimalità di `{goal.alias}`", positive_enforcement, note, spoilering = False)
        
            
    def feedback_when_all_non_spoilering_checks_passed(self):
        self.evaluation_format(f"Quanto sottomesso{'' if self.task_number < 0 else ' per la Richiesta '+str(self.task_number)} ha superato tutti i miei controlli. Ovviamente in sede di esame non posso esprimermi sull'ottimalità di valori e di soluzioni immesse. Il mio controllo e supporto si è limitato alla compatibilità di formato, all'ammissibilità, e alla consistenza dei dati immessi.", pt_safe=self.pt_formato_OK + self.pt_feasibility_OK + self.pt_consistency_OK,pt_out=0)
        return self.non_spoilering_feedback

