#!/usr/bin/python3
import subprocess

tests=[
   ('cat solutions/goal1.txt | ./eval_submission.py 1 1', "perfect1-1-challenge"),
   ('cat solutions/goal1.txt | ./eval_submission.py 1 2', "perfect1-2-challenge"),
   ('cat solutions/goal1.txt | ./eval_submission.py 1 3', "perfect1-3-challenge"),
   ('cat tests/goal1_wrong_chars1.txt | ./eval_submission.py 1 1', "wrong-char-bool"),
   ('cat tests/goal1_wrong_chars1.txt | ./eval_submission.py 1 2', "wrong-char-bool"),
   ('cat tests/goal1_wrong_chars1.txt | ./eval_submission.py 1 3', "wrong-char-bool"),
   ('cat tests/goal1_wrong_chars2.txt | ./eval_submission.py 1 1', "perfect1-1-challenge"),
   ('cat tests/goal1_wrong_chars2.txt | ./eval_submission.py 1 2', "wrong-char-bool"),
   ('cat tests/goal1_wrong_chars2.txt | ./eval_submission.py 1 3', "wrong-char-bool"),
]

for run_test, expected_output_test in tests:
  try:
      output = str(subprocess.check_output([run_test], shell=True,))[2:]
  except EOFError:
      print(f'Test FAILED!!! If you lounch:\n   {run_test}\nyou get errors!\n')
      exit(1)

  if not output.startswith(f"({expected_output_test})"):
     rpos = output.find(")")
     print(f'Test FAILED!!! If you lounch:\n   {run_test}\nthe generated feedback code is not ({expected_output_test}) but {output[:rpos+1]}\n')
     exit(2)   

print("OK. All tests successfully passed!")
