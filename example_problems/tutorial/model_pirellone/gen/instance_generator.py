#!/usr/bin/env python3
from sys import argv, stderr, exit

import model_pirellone_lib as pl


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


def main(n, m, solvable, gen_seed, format):
    # Automatic cast:
    n = int(n)
    m = int(m)
    solvable = str2bool(solvable)
    gen_seed = int(gen_seed)
    format_list = format.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = ''
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]

    # Generate pirellone instance
    instance_seed = pl.gen_pirellone_seed(solvable, gen_seed)
    pirellone = pl.gen_pirellone(m, n, instance_seed)

    # Generate selected output
    # CASE1: dat
    if format_primary == 'dat': 
        if format_secondary == '': #for_now_we_have_only_one
            print(pl.pirellone_to_dat(pirellone))
        else:
            assert False, f'Value {format_secondary} unsupported for the argument format_secondary when format_primary={format_primary}.'

    # CASE2: txt
    elif format_primary == 'txt':
        if format_secondary == 'only_matrix':
            print(pl.pirellone_to_str(pirellone, 'only_matrix'))
        elif format_secondary == 'with_m_and_n':
            print(pl.pirellone_to_str(pirellone, 'with_m_and_n'))
        else:
            assert False, f'Value {format_secondary} unsupported for the argument format_secondary when format_primary={format_primary}.'

    # CASEN: error
    else:
        assert False, f'Value {format_primary} unsupported for the argument format_primary.'

    exit(0)


if __name__ == "__main__":
    from sys import argv
    assert len(argv) == 6, 'Miss arguments'
    main(argv[1], argv[2], argv[3], argv[4], argv[5])