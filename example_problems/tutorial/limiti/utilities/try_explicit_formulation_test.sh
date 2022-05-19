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