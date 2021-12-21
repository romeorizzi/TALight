rtal connect model_lcs try_GMPL_model -asol_style=subsequence -ainstance_id=2 -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod
rtal connect model_lcs try_GMPL_model -asol_style=annotated_subseq -ainstance_id=2 -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod

rtal connect model_lcs try_GMPL_model -adisplay_output=1 -adisplay_error=1 -adisplay_solution=1 -acheck_solution=1 -asol_style=subsequence -ainstance_id=6 -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.modd

rtal connect model_lcs try_GMPL_model -adisplay_output=1 -adisplay_error=1 -adisplay_solution=1 -acheck_solution=1 -asol_style=annotated_subseq -ainstance_id=5 -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod

rtal connect model_lcs try_GMPL_model -adisplay_output=1 -adisplay_error=1 -adisplay_solution=1 -acheck_solution=1 -asol_style=subsequence -atxt_style=only_strings -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod dat=instances/m_and_n_at_least_20_lowercase/instance5.dat input=instances/m_and_n_at_least_20_lowercase/instance5.only_strings.txt
rtal connect model_lcs try_GMPL_model -adisplay_output=1 -adisplay_error=1 -adisplay_solution=1 -acheck_solution=1 -asol_style=subsequence -atxt_style=with_m_and_n -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod dat=instances/m_and_n_at_least_20_lowercase/instance5.dat input=instances/m_and_n_at_least_20_lowercase/instance5.with_m_and_n.txt

rtal connect model_lcs try_GMPL_model -ainstance_id=1 -adisplay_explicit_formulation=1 -aexplicit_formulation_format=mps -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod
rtal connect model_lcs try_GMPL_model -ainstance_id=1 -adisplay_explicit_formulation=1 -aexplicit_formulation_format=freemps -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod
rtal connect model_lcs try_GMPL_model -ainstance_id=1 -adisplay_explicit_formulation=1 -aexplicit_formulation_format=lp -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod
rtal connect model_lcs try_GMPL_model -ainstance_id=1 -adisplay_explicit_formulation=1 -aexplicit_formulation_format=glp -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod
