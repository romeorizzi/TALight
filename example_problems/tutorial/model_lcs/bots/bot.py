#!/usr/bin/python
from sys import stderr, exit, argv
import argparse
from bot_lib import Bot

parser = argparse.ArgumentParser(description="I am a bot for the TALight problem `lcs` (longest common subsequence of two strings s and t). In a never ending loop (until I get the '# WE HAVE FINISHED' line), I read an input instances from stdin and I write my answer for it on stdout. The default instance format is 'only_strings', but you can call me with the optional argument --with_m_and_n to switch it to 'with_m_and_n'. The default answer format is 'only_val', but you can call me with the optional argument --subseq to switch it to 'subseq'. The other optional arguments are --subopt and --supopt. They are meant to impose me to make mistakes, and are useful for testing the 'eval_your_bot' service of the problem. These optional arguments will tell me on which side I should err (in particular, by joining the optional arguments --subseq and --supopt, you are asking me to return unfeasible solutions)")
parser.add_argument('--with_m_and_n', action='store_true', help="by default, the bot gets the two strings s and t comprising each instance of the `lcs` problem by reading the two first uncommented lines from stdin (lines starting with the '#' character or empty are considered comments and ignored by the protocol between the problem solver bot and the service server). Use this optional argument when, for each input instance, the first line read from stdin containts the two integers m and n, which specify the lengths of the two input strings s and t (to be read on the next two uncommented lines)")
parser.add_argument('--subseq', action='store_true', help="when, for each instance, the bot should print on stdout a longest common subsequence (of the two strings s and t read from stdin) rather than just its length")
group = parser.add_mutually_exclusive_group()
group.add_argument('--subopt', action='store_true', help="the bot will err on the pessimistic side, as it could see only sub-optimal solutions")
group.add_argument('--supopt', action='store_true', help="the bot will err on the optimistic side (in particular, when asked for an optimal solution using also the --subseq flag, then it will return just an unfeasible solution)")
args = parser.parse_args()

print(f"""# I am a bot for the TALight problem `lcs` (longest common subsequence of two strings s and t). Call me like this:
#     {argv[0]} -h
#if you want to know more about me (how to call me, my arguments and what I am supposed to do for you).
# My parameters for the current call are set as follows:
#   {args.with_m_and_n=}
#   {args.subseq=}
#   {args.subopt=}
#   {args.supopt=}""")


# BOT = Bot(report_inputs=True,reprint_outputs=True)
BOT = Bot(report_inputs=False,reprint_outputs=False)
while True:
    m = None
    n = None
    if args.with_m_and_n:
        m,n = map(int, BOT.input().split())
    s = BOT.input()
    t = BOT.input()
    if m == None:
        m = len(s)
    else:
        assert m == len(s)
    if n == None:
        n = len(t)
    else:
        assert n == len(t)
    pref_of_len = [ [ 0 ] * (1+len(t)) for i in range(1+len(s)) ]
    for i in range(1,1+len(s)):
      for j in range(1,1+len(t)):
          if s[i-1] == t[j-1]:
              pref_of_len[i][j] = 1 + pref_of_len[i-1][j-1]
          else:
              pref_of_len[i][j] = max(pref_of_len[i-1][j],pref_of_len[i][j-1])
    def reconstruct_opt_lcs_pref_of_len(len_s,len_t, lcs : list):
        if pref_of_len[len_s][len_t] == 0:
            pass
        elif s[len_s-1] == t[len_t-1]:
            lcs.append(s[len_s-1])
            reconstruct_opt_lcs_pref_of_len(len_s-1,len_t-1, lcs)
        elif len_s==1:
            reconstruct_opt_lcs_pref_of_len(len_s,len_t-1, lcs)
        elif pref_of_len[len_s-1][len_t]==pref_of_len[len_s][len_t]:
            reconstruct_opt_lcs_pref_of_len(len_s-1,len_t, lcs)
        else:
            reconstruct_opt_lcs_pref_of_len(len_s,len_t-1, lcs)
            
    if args.subseq:
        lcs = []
        reconstruct_opt_lcs_pref_of_len(len(s),len(t), lcs)
        opt_sol = "".join(reversed(lcs))
        if args.subopt:
            BOT.print(opt_sol[:-1])
        elif args.supopt:
            BOT.print(opt_sol+t[-1])
        else:
            BOT.print(opt_sol)
    else:
        if args.subopt:
            BOT.print(pref_of_len[len(s)][len(t)]-1)
        elif args.supopt:
            BOT.print(pref_of_len[len(s)][len(t)]+1)
        else:
            BOT.print(pref_of_len[len(s)][len(t)])

    
        
