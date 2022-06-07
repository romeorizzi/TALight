#!/usr/bin/env python3
from sys import stderr


Field = list[list[int]]


def parse_cell(cell: str) -> tuple[int, int]:
    # remove parenthesis
    cell = cell[1:-1]
    row, col = cell.split(",")
    row, col = ord(row.lower()) - ord("a"), int(col)
    return (row, col)


def free(field: Field, row: int, col: int) -> bool:
    """Checks whether a cell is free or forbidden."""
    return field[row][col] != -1


def check_instance_consistency(instance):
    #print(f"instance={instance}", file=stderr)
    instance_objects = ['field', 'diag', 'partialDP_to',
                        'partialDP_from', 'cell_from', 'cell_to', 'cell_through']

    field = instance['field']
    m, n = len(field), len(field[0])
    # TODO: ask whether this check is necessary for the type 'matrix_of_int'
    for row in field:
        if len(row) != n:
            print(f"Error: field must be a matrix")
            exit(0)

    for row in range(field):
        for col in range(row):
            if (c := field[row][col]) < -1:
                print(f"Error: value {c} in ({row},{col}) is not allowed")
                exit(0)

    if field[0][0] == -1 or field[-1][-1] == -1:
        print(f"Error")
        exit(0)

    # TODO: validate cells coordinates
    cell_from = parse_cell(instance['cell_from'])
    cell_to = parse_cell(instance['cell_to'])
    cell_through = parse_cell(instance['cell_through'])


def dptable_num_to_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for counting the number of paths.
    Construction starts from the cell in the top-left corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """

    # NOTE: cells default to zero, in some cases there is no need to assing values
    t = [[0 for _ in range(len(f[0]))] for _ in range(len(f))]
    t[0][0] = 1
    for i in range(1, len(t[0])):
        if free(f, 0, i):
            t[0][i] = t[0][i - 1]

    for i in range(1, len(t)):
        if free(f, i, 0):
            t[i][0] = t[i - 1][0]

    if diag:
        for i in range(1, len(t)):
            for j in range(1, len(t[i])):
                if free(f, i, j):
                    t[i][j] = t[i][j - 1] + t[i - 1][j] + t[i - 1][j - 1]

    else:
        for i in range(1, len(t)):
            for j in range(1, len(t[i])):
                if free(f, i, j):
                    t[i][j] = t[i][j - 1] + t[i - 1][j]

    return t


def dptable_num_from_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for counting the number of paths.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    pass


def dptable_opt_to_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """

    t = [[0 for _ in range(len(f[0]))] for _ in range(len(f))]
    t[0][0] = f[0][0]
    for i in range(1, len(t[0])):
        if free(f, 0, i):
            t[0][i] = f[0][i] + t[0][i - 1]

    for i in range(1, len(t)):
        if free(f, i, 0):
            t[i][0] = f[i][0] + t[i - 1][0]

    if diag:
        for i in range(1, len(t)):
            for j in range(1, len(t[i])):
                if free(f, i, j):
                    t[i][j] = f[i][j] + max([t[i][j - 1], t[i - 1][j], t[i - 1][j - 1]])

    else:
        for i in range(1, len(t)):
            for j in range(1, len(t[i])):
                if free(f, i, j):
                    t[i][j] = f[i][j] + max(t[i][j - 1], t[i - 1][j])

    return t


def dptable_opt_from_cell(f: Field, diag: bool = False) -> Field:
    pass


def dptable_num_opt_to_cell(f: Field, diag: bool = False) -> Field:
    pass


def dptable_num_opt_from_cell(f: Field, diag: bool = False) -> Field:
    pass


def solver(input_to_oracle):
    I = input_to_oracle["instance"]

    # extract and parse inputs
    field = I["field"]
    diag = I["diag"]
    cell_to = (0,0)
    cell_from = (0,0)
    cell_through = (0,0)

    # compute tables
    DPtable_num_to = dptable_num_to_cell(field, diag=diag)
    DPtable_num_from = dptable_num_from_cell(field, diag=diag)

    DPtable_opt_to = dptable_opt_to_cell(field, diag=diag)
    DPtable_opt_from = dptable_opt_from_cell(field, diag=diag)

    DPtable_num_opt_to = dptable_num_opt_to_cell(field, diag=diag)
    DPtable_num_opt_from = dptable_num_opt_from_cell(field, diag=diag)

    # retrieve and format outputs
    num_paths = 0
    num_opt_paths = 0
    opt_val = 0
    opt_path = []
    list_opt_path = []

    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers
