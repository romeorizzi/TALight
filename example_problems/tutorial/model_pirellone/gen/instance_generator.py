#!/usr/bin/env python3
from sys import argv, stderr, exit

import model_pirellone_lib as pl

m = int(argv[1])
n = int(argv[2])
solvable = bool(argv[3])
seed = int(argv[4])
format_primary = argv[5]
format_secondary = argv[6]

pirellone = pl.gen_pirellone(m,n,seed)
if format_primary == "dat": 
    print(pl.pirellone_to_dat(pirellone))
elif format_primary == "txt":
    if format_secondary == "only_matrix": 
       print(pl.pirellone_to_str(pirellone, "only_matrix"))
    elif format_primary == "with_m_and_n":
       print(pl.pirellone_to_str(pirellone, "with_m_and_n"))
    else:
        assert False, f"Value {format_secondary} unsupported for the argument format_secondary when format_primary={ format_primary}."

    print(pl.pirellone_to_dat(pirellone))
else:
    assert False, f"Value {format_primary} unsupported for the argument format_primary."

exit(0)
