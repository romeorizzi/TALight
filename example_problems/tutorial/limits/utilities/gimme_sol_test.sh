rtal connect model_lcs gimme_sol -ainstance_spec=random -am=5 -an=5 -aalphabet=dna -asol_style=subsequence
rtal connect model_lcs gimme_sol -ainstance_spec=random -am=5 -an=5 -aalphabet=dna -asol_style=annotated_subseq

rtal connect model_lcs gimme_sol -ainstance_spec=random -am=5 -an=5 -aalphabet=lowercase -asol_style=subsequence
rtal connect model_lcs gimme_sol -ainstance_spec=random -am=5 -an=5 -aalphabet=lowercase -asol_style=annotated_subseq

rtal connect model_lcs gimme_sol -ainstance_spec=random -am=5 -an=5 -aalphabet=lowercase_uppercase -asol_style=subsequence
rtal connect model_lcs gimme_sol -ainstance_spec=random -am=5 -an=5 -aalphabet=lowercase_uppercase -asol_style=annotated_subseq

rtal connect model_lcs gimme_sol -ainstance_spec=random -am=20 -an=25 -aalphabet=dna -asol_style=subsequence
rtal connect model_lcs gimme_sol -ainstance_spec=random -am=20 -an=25 -aalphabet=dna -asol_style=annotated_subseq

rtal connect model_lcs gimme_sol -ainstance_spec=random -am=20 -an=25 -aalphabet=lowercase -asol_style=subsequence
rtal connect model_lcs gimme_sol -ainstance_spec=random -am=20 -an=25 -aalphabet=lowercase -asol_style=annotated_subseq

rtal connect model_lcs gimme_sol -ainstance_spec=random -am=20 -an=25 -aalphabet=lowercase_uppercase -asol_style=subsequence
rtal connect model_lcs gimme_sol -ainstance_spec=random -am=20 -an=25 -aalphabet=lowercase_uppercase -asol_style=annotated_subseq

rtal connect model_lcs gimme_sol -ainstance_spec=TA_send_files_bot -am=5 -an=5 -aalphabet=dna -asol_style=subsequence -- bots/TA_send_files_bot.py instances/m_and_n_at_least_5_dna/instance2.only_strings.txt
rtal connect model_lcs gimme_sol -ainstance_spec=TA_send_files_bot -am=5 -an=5 -aalphabet=dna -asol_style=annotated_subseq -- bots/TA_send_files_bot.py instances/m_and_n_at_least_5_dna/instance2.only_strings.txt