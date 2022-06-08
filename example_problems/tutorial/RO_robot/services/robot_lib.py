#!/usr/bin/env python3
from dataclasses import dataclass
from sys import stderr


Field = list[list[int]]
Cell = tuple[int, int]


def parse_cell(cell: str) -> Cell:
    # remove parenthesis
    cell = cell[1:-1]
    row, col = cell.split(",")
    row, col = ord(row.lower()) - ord("a"), int(col)
    return (row, col)


def free(field: Field, row: int, col: int) -> bool:
    """Checks whether a cell is free or forbidden."""
    return field[row][col] != -1


def check_matrix_shape(f: Field) -> bool:
    cols = len(f[0])
    for row in f:
        if len(row) != cols:
            return False
    return True


def check_instance_consistency(instance):
    #print(f"instance={instance}", file=stderr)
    instance_objects = ['field', 'diag', 'partialDP_to',
                        'partialDP_from', 'cell_from', 'cell_to', 'cell_through']

    field = instance['field']
    rows, cols = len(field), len(field[0])
    # TODO: ask whether this check is necessary for the type 'matrix_of_int'
    if not check_matrix_shape(field):
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
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    t = [[0 for _ in range(cols)] for _ in range(rows)]
    # NOTE: cells default to zero, in some cases there is no need to assing values
    t[0][0] = 1
    for i in range(1, cols):
        if free(f, 0, i):
            t[0][i] = t[0][i - 1]

    for i in range(1, rows):
        if free(f, i, 0):
            t[i][0] = t[i - 1][0]

    if diag:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    t[i][j] = t[i][j - 1] + t[i - 1][j] + t[i - 1][j - 1]

    else:
        for i in range(1, rows):
            for j in range(1, cols):
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
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    t = [[0 for _ in range(cols)] for _ in range(rows)]

    # NOTE: cells default to zero, in some cases there is no need to assing values
    t[-1][-1] = 1
    for i in reversed(range(cols - 1)):
        if free(f, -1, i):
            t[-1][i] = t[-1][i + 1]

    for i in reversed(range(rows - 1)):
        if free(f, i, -1):
            t[i][-1] = t[i + 1][-1]

    if diag:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    t[i][j] = t[i][j + 1] + t[i + 1][j] + t[i + 1][j + 1]

    else:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    t[i][j] = t[i][j + 1] + t[i + 1][j]

    return t


def dptable_opt_to_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    t = [[0 for _ in range(cols)] for _ in range(rows)]

    t[0][0] = f[0][0]
    for i in range(1, cols):
        if free(f, 0, i):
            t[0][i] = f[0][i] + t[0][i - 1]

    for i in range(1, rows):
        if free(f, i, 0):
            t[i][0] = f[i][0] + t[i - 1][0]

    if diag:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    t[i][j] = f[i][j] + \
                        max([t[i][j - 1], t[i - 1][j], t[i - 1][j - 1]])

    else:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    t[i][j] = f[i][j] + max(t[i][j - 1], t[i - 1][j])

    return t


def dptable_opt_from_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    t = [[0 for _ in range(cols)] for _ in range(rows)]

    t[-1][-1] = f[-1][-1]
    for i in reversed(range(cols - 1)):
        if free(f, -1, i):
            t[-1][i] = f[-1][i] + t[-1][i + 1]

    for i in reversed(range(rows - 1)):
        if free(f, i, -1):
            t[i][-1] = f[i][-1] + t[i + 1][-1]

    if diag:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    t[i][j] = f[i][j] + \
                        max([t[i][j + 1], t[i + 1][j], t[i + 1][j + 1]])

    else:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    t[i][j] = f[i][j] + max(t[i][j + 1], t[i + 1][j])

    return t


@dataclass
class NumOptCell:
    count: int  # the count of optimal paths ending at this cell
    value: int  # the optimal value of a path ending at this cell


def dptable_num_opt_to_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    # NOTE: store (num_of_paths, opt_value) for each cell
    t = [[NumOptCell(count=0, value=0) for _ in range(cols)]
         for _ in range(rows)]

    t[0][0].count = 1
    t[0][0].value = f[0][0]
    for i in range(1, cols):  # fill first row
        if free(f, 0, i):
            t[0][i].count = t[0][i - 1].count
            t[0][i].value = f[0][i] + t[0][i - 1].value

    for i in range(1, rows):  # fill first column
        if free(f, i, 0):
            t[i][0].count = t[i - 1][0].count
            t[i][0].value = f[i][0] + t[i - 1][0].value

    if diag:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    neighbors = [t[i][j - 1], t[i - 1][j], t[i - 1][j - 1]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    else:
        for i in range(1, rows):
            for j in range(1, cols):
                if free(f, i, j):
                    neighbors = [t[i][j - 1], t[i - 1][j]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    return as_tuple_matrix(t)


def dptable_num_opt_from_cell(f: Field, diag: bool = False) -> Field:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    rows, cols = len(f), len(f[0])
    # NOTE: store (num_of_paths, opt_value) for each cell
    t = [[NumOptCell(count=0, value=0) for _ in range(cols)]
         for _ in range(rows)]

    t[-1][-1].count = 1
    t[-1][-1].value = f[-1][-1]
    for i in reversed(range(cols - 1)):  # fill last row
        if free(f, -1, i):
            t[-1][i].count = t[-1][i + 1].count
            t[-1][i].value = f[-1][i] + t[-1][i + 1].value

    for i in reversed(range(rows - 1)):  # fill last column
        if free(f, i, -1):
            t[i][-1].count = t[i + 1][-1].count
            t[i][-1].value = f[i][-1] + t[i + 1][-1].value

    if diag:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    neighbors = [t[i][j + 1], t[i + 1][j], t[i + 1][j + 1]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    else:
        for i in reversed(range(rows - 1)):
            for j in reversed(range(cols - 1)):
                if free(f, i, j):
                    neighbors = [t[i][j + 1], t[i + 1][j]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    return as_tuple_matrix(t)


def as_tuple_matrix(table: list[list[NumOptCell]]) -> list[list[Cell]]:
    return [[(x.count, x.value) for x in row] for row in table]


def build_opt_path(dptable: Field, diag: bool = False) -> list[Cell]:
    rows, cols = len(dptable), len(dptable[0])
    row, col = 0, 0
    path = []
    if diag:
        while ():
            pass

    else:
        while ():
            pass

    return path


def build_all_opt_path(dptable: Field, diag: bool = False) -> list[list[Cell]]:
    pass


def solver(input_to_oracle):
    I = input_to_oracle["instance"]

    # extract and parse inputs
    field = I["field"]
    diag = I["diag"]
    cell_to = (0, 0)
    cell_from = (0, 0)
    cell_through = (0, 0)

    # compute tables
    DPtable_num_to = dptable_num_to_cell(field, diag=diag)
    DPtable_num_from = dptable_num_from_cell(field, diag=diag)

    DPtable_opt_to = dptable_opt_to_cell(field, diag=diag)
    DPtable_opt_from = dptable_opt_from_cell(field, diag=diag)

    DPtable_num_opt_to = dptable_num_opt_to_cell(field, diag=diag)
    DPtable_num_opt_from = dptable_num_opt_from_cell(field, diag=diag)

    # retrieve and format outputs
    # TODO: adapt solutions to different 'from' and 'to' cells
    num_paths = DPtable_num_to[-1][-1]
    num_opt_paths = DPtable_num_opt_to[-1][-1]
    opt_val = DPtable_opt_to[-1][-1]
    list_opt_path = [[]]
    opt_path = list_opt_path[0]

    # TODO: random obfuscation of dptables as last step

    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers
