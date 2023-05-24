#!/usr/bin/env python3

from time import time
from sys import stdout, stderr
from os import environ
from os.path import join
import sqlite3
import traceback


class TC:
    def __init__(self, data, time_limit=1):
        self.data = data
        self.tl = time_limit
        self.exam = "TAL_META_EXP_TOKEN" in environ and "TAL_EXT_EXAM_DB" in environ

    def run(self, gen_tc, check_tc):
        output = open(
            join(environ["TAL_META_OUTPUT_FILES"], "result.txt"), "w")
        total_tc = sum(map(lambda x: x[0], self.data))
        print(total_tc, flush=True)
        tc_ok = 0
        tcn = 1
        for subtask in range(len(self.data)):
            for tc in range(self.data[subtask][0]):
                tc_data = gen_tc(*self.data[subtask][1])
                stdout.flush()
                start = time()
                try:
                    ret = check_tc(*tc_data)
                    msg = None
                    if isinstance(ret, tuple):
                        result = ret[0]
                        msg = ret[1]
                    else:
                        result = ret
                    if time() - start > self.tl:
                        print(f"Case #{tcn:03}: TLE", file=output)
                    elif result:
                        print(f"Case #{tcn:03}: AC", file=output)
                        tc_ok += 1
                    else:
                        print(f"Case #{tcn:03}: WA", file=output)
                    if msg is not None:
                        print(file=output)
                        print(msg, file=output)
                        print(file=output)
                except Exception as e:
                    print(f"Case #{tcn:03}: RE", file=output)
                    print(file=stderr)
                    print("".join(traceback.format_tb(
                        e.__traceback__)), e, file=stderr)
                tcn += 1
        print(file=output)
        print(f"Score: {tc_ok}/{total_tc}", file=output)
        output.close()
        if self.exam:
            db = sqlite3.connect(environ["TAL_EXT_EXAM_DB"])
            db.execute(
                "INSERT INTO submissions (user_id, problem, address, score, source) VALUES (?, ?, ?, ?, ?)",
                (
                    environ["TAL_META_EXP_TOKEN"],
                    environ["TAL_META_CODENAME"],
                    environ["TAL_META_EXP_ADDRESS"],
                    tc_ok,
                    open(join(environ["TAL_META_INPUT_FILES"],
                         "source"), "rb").read(),
                ),
            )
            db.commit()
            db.close()
