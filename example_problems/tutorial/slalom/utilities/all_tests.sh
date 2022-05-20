## clean everything
make clean

## generate instances
make

## gimme_instance

rtal connect model_lcs gimme_instance -ainstance_spec=random -am=5 -an=5 -aalphabet=dna -aformat=only_strings.txt

rtal connect model_lcs gimme_instance -ainstance_spec=random -am=5 -an=5 -aalphabet=lowercase -aformat=with_m_and_n.txt

rtal connect model_lcs gimme_instance -ainstance_spec=random -am=5 -an=5 -aalphabet=lowercase_uppercase -aformat=dat

rtal connect model_lcs gimme_instance -ainstance_spec=random -am=20 -an=25 -aalphabet=dna -aformat=only_strings.txt

rtal connect model_lcs gimme_instance -ainstance_spec=random -am=20 -an=25 -aalphabet=lowercase -aformat=with_m_and_n.txt

rtal connect model_lcs gimme_instance -ainstance_spec=random -am=20 -an=25 -aalphabet=lowercase_uppercase -aformat=dat

rtal connect model_lcs gimme_instance -asource=catalogue -ainstance_id=2 -am=5 -an=5 -aalphabet=dna -aformat=only_strings.txt
rtal connect model_lcs gimme_instance -asource=catalogue -ainstance_id=2 -am=5 -an=5 -aalphabet=dna -aformat=with_m_and_n.txt
rtal connect model_lcs gimme_instance -asource=catalogue -ainstance_id=2 -am=5 -an=5 -aalphabet=dna -aformat=dat

## gimme_sol

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

### check_sol

rtal connect model_lcs check_sol -ainstance_spec=random -am=5 -an=5 -aalphabet=dna -asol_style=subsequence
rtal connect model_lcs check_sol -ainstance_spec=random -am=5 -an=5 -aalphabet=dna -asol_style=annotated_subseq

rtal connect model_lcs check_sol -ainstance_spec=TA_send_files_bot -am=7 -an=7 -aalphabet=dna -asol_style=subsequence -- bots/TA_send_files_bot.py examples/instance_with_solution_subsequence.txt
rtal connect model_lcs check_sol -ainstance_spec=TA_send_files_bot -am=7 -an=7 -aalphabet=dna -asol_style=annotated_subseq -- bots/TA_send_files_bot.py examples/instance_with_solution_annotated_subseq.txt

## try_GMPL_model

rtal connect model_lcs try_GMPL_model -asol_style=subsequence -ainstance_id=2 -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod
rtal connect model_lcs try_GMPL_model -asol_style=annotated_subseq -ainstance_id=2 -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod

rtal connect model_lcs try_GMPL_model -adisplay_output=1 -adisplay_error=1 -adisplay_solution=1 -acheck_solution=1 -asol_style=subsequence -ainstance_id=6 -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.modd

rtal connect model_lcs try_GMPL_model -adisplay_output=1 -adisplay_error=1 -adisplay_solution=1 -acheck_solution=1 -asol_style=annotated_subseq -ainstance_id=5 -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod

rtal connect model_lcs try_GMPL_model -adisplay_output=1 -adisplay_error=1 -adisplay_solution=1 -acheck_solution=1 -asol_style=subsequence -atxt_style=only_strings -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod dat=instances/m_and_n_at_least_20_lowercase/instance5.dat input=instances/m_and_n_at_least_20_lowercase/instance5.only_strings.txt
rtal connect model_lcs try_GMPL_model -adisplay_output=1 -adisplay_error=1 -adisplay_solution=1 -acheck_solution=1 -asol_style=subsequence -atxt_style=with_m_and_n -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod dat=instances/m_and_n_at_least_20_lowercase/instance5.dat input=instances/m_and_n_at_least_20_lowercase/instance5.with_m_and_n.txt

rtal connect model_lcs try_GMPL_model -ainstance_id=1 -adisplay_explicit_formulation=1 -aexplicit_formulation_format=wmps -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod
rtal connect model_lcs try_GMPL_model -ainstance_id=1 -adisplay_explicit_formulation=1 -aexplicit_formulation_format=wfreemps -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod
rtal connect model_lcs try_GMPL_model -ainstance_id=1 -adisplay_explicit_formulation=1 -aexplicit_formulation_format=wlp -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod
rtal connect model_lcs try_GMPL_model -ainstance_id=1 -adisplay_explicit_formulation=1 -aexplicit_formulation_format=wglp -- bots/TA_send_files_bot.py mod=models/lcs_ILP-model-gmpl.mod

# eval_GMPL_model

rtal connect model_lcs eval_GMPL_model -agoal=m_and_n_at_least_5_dna -- bots/TA_send_files_bot.py models/lcs_ILP-model-gmpl.mod

# try_explicit_formulation

rtal connect model_lcs try_explicit_formulation -aformat=freemps -- bots/TA_send_files_bot.py ef=examples/formulations_over_instance1/freemps_formulation.txt
rtal connect model_lcs try_explicit_formulation -aformat=glp -- bots/TA_send_files_bot.py ef=examples/formulations_over_instance1/glp_formulation.txt
rtal connect model_lcs try_explicit_formulation -aformat=lp -- bots/TA_send_files_bot.py ef=examples/formulations_over_instance1/lp_formulation.txt
rtal connect model_lcs try_explicit_formulation -aformat=mps -- bots/TA_send_files_bot.py ef=examples/formulations_over_instance1/mps_formulation.txt
rtal connect model_lcs try_explicit_formulation -aformat=math -- bots/TA_send_files_bot.py ef=models/lcs_ILP-model-gmpl.mod dat=instances/out/instance1.dat

rtal connect model_lcs try_explicit_formulation -adisplay_error=1 -adisplay_output=1 -aformat=freemps -- bots/TA_send_files_bot.py ef=examples/formulations_over_instance1/freemps_formulation.txt
rtal connect model_lcs try_explicit_formulation -adisplay_error=1 -adisplay_output=1 -aformat=glp -- bots/TA_send_files_bot.py ef=examples/formulations_over_instance1/glp_formulation.txt
rtal connect model_lcs try_explicit_formulation -adisplay_error=1 -adisplay_output=1 -aformat=lp -- bots/TA_send_files_bot.py ef=examples/formulations_over_instance1/lp_formulation.txt
rtal connect model_lcs try_explicit_formulation -adisplay_error=1 -adisplay_output=1 -aformat=mps -- bots/TA_send_files_bot.py ef=examples/formulations_over_instance1/mps_formulation.txt
rtal connect model_lcs try_explicit_formulation -adisplay_error=1 -adisplay_output=1 -aformat=math -- bots/TA_send_files_bot.py ef=models/lcs_ILP-model-gmpl.mod dat=instances/public_examples/instance1.dat