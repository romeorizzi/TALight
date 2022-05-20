rtal connect model_lcs check_sol -ainstance_spec=random -am=5 -an=5 -aalphabet=dna -asol_style=subsequence
rtal connect model_lcs check_sol -ainstance_spec=random -am=5 -an=5 -aalphabet=dna -asol_style=annotated_subseq

rtal connect model_lcs check_sol -ainstance_spec=TA_send_files_bot -am=7 -an=7 -aalphabet=dna -asol_style=subsequence -- bots/TA_send_files_bot.py examples/instance_with_solution_subsequence.txt
rtal connect model_lcs check_sol -ainstance_spec=TA_send_files_bot -am=7 -an=7 -aalphabet=dna -asol_style=annotated_subseq -- bots/TA_send_files_bot.py examples/instance_with_solution_annotated_subseq.txt