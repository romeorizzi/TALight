#!/usr/bin/env python3
from run_with_deadline import run_with_deadline
from time import sleep

if __name__ == '__main__':
    def slow_funct(a,b,snooze_secs):
        sleep(snooze_secs)
        return a*b

    for i in range(5):
        for j in range(5):
            print(run_with_deadline(f=slow_funct, args={'a':i, 'b':j, 'snooze_secs':i+j}, deadline=6))

