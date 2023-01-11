#!/usr/bin/env python3

import logging
from dataclasses import dataclass
from typing import Dict, Final, List, Tuple, TypeVar

from RO_verify_submission_gen_prob_lib import verify_submission_gen

_LOGGER = logging.getLogger(__package__).getChild("robot")

instance_objects_spec = [
    ("grid", "matrix_of_int"),
    ("budget", int),
    ("diag", bool),
    ("cell_from", "list_of_str"),
    ("cell_to", "list_of_str"),
    ("cell_through", "list_of_str"),
]
additional_infos_spec = [
    ("partialDP_to", "matrix_of_int"),
    ("partialDP_from", "matrix_of_int"),
]
answer_objects_spec = {
    "num_paths": "int",                       # the number of feasible paths
    # the number of feasible paths that collect the maximum total prize
    "num_opt_paths": "int",
    # the maximum total prize a feasible path can collect
    "opt_val": "int",
    # a path collecting the maximum possible total prize
    "opt_path": "list_of_cell",
    "list_opt_paths": "list_of_list_of_cell",  # the list of all optimum paths
    # the DP table meant to tell the number of paths from top-left cell to the generic cell
    "DPtable_num_to": "matrix_of_int",
    # the DP table meant to tell the number of paths from the generic cell to the bottom-right cell"
    "DPtable_num_from": "matrix_of_int",
    # the DP table meant to tell the maximum value of a feasible path path moving from top-left cell to the generic cell
    "DPtable_opt_to": "matrix_of_int",
    # the DP table meant to tell the maximum value of a feasible path moving from the generic cell to the bottom-right cell
    "DPtable_opt_from": "matrix_of_int",
    # the DP table meant to tell the number of optimal paths from top-left cell to the generic cell"
    "DPtable_num_opt_to": "matrix_of_int",
    # the DP table meant to tell the number of optimal paths from the generic cell to the bottom-right cell.
    "DPtable_num_opt_from": "matrix_of_int",
}

answer_objects_implemented = [
    'num_paths',
    'num_opt_paths',
    'opt_val',
    'opt_path',
    'list_opt_paths',
    'DPtable_num_to',
    'DPtable_num_from',
    'DPtable_opt_to',
    'DPtable_opt_from',
    'DPtable_num_opt_to',
    'DPtable_num_opt_from'
]

limits = {
    'CAP_FOR_NUM_SOLS': 100,
    'CAP_FOR_NUM_OPT_SOLS': 100
}

_T = TypeVar("_T")

_Cell = Tuple[int, int]
_Mat = List[List[_T]]


def _xmap(x: int) -> int:
    """Map internal x coordinate of a cell to a human-readable format."""
    return x + 1


def _ymap(y: int) -> str:
    """Map internal y coordinate of a cell to a human-readable format."""
    return chr(ord('A') + y)


def _map(x, y):
    return f"({_xmap(x)},{_ymap(y)})"


def parse_cell(cell: str) -> _Cell:
    # Take row and col
    #cell = cell[1:-1]
    #row, col = cell.split(",")
    #row, col = ord(row.lower()) - ord("a"), int(col)
    row, col = cell
    row, col = int(row) - 1, ord(col.lower()) - ord("a")
    return (row, col)


def free(field: _Mat[int], row: int, col: int) -> bool:
    """Checks whether a cell is free or forbidden."""
    assert field is not None
    return field[row][col] != -1


def check_matrix_shape(f: _Grid) -> bool:
    print("\ncheck_matrix_shape")
    print(f)
    """Checks if matrix is empty."""
    if not f:
        return False


    """Checks if list is a matrix."""
    cols = len(f[0])
    if cols == 0:
        return False

    print("ciao 1")

    for row in f:
        print(row)
        if len(row) != cols:
            return False

    print("ciao 2")

    return True

def check_same_shape(g1: _Mat, g2: _Mat) -> bool:
    """Check if two matrices have the same shape"""
    return len(g1) == len(g2) and len(g1[0]) == len(g2[0])


def check_instance_consistency(instance):
    _LOGGER.debug("instance = %s", instance)
    grid = instance['grid']
    ROWS, COLS = len(grid), len(grid[0])
    # TODO: ask whether this check is necessary for the type 'matrix_of_int'
    if not check_matrix_shape(grid):
        print(f"Error: {grid} must be a matrix")
        exit(0)

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if (c := grid[row][col]) < -1:
                print(f"Error: value {c} in {_map(row, col)} is not allowed")
                exit(0)

    if grid[0][0] == -1 or grid[-1][-1] == -1:
        print(f"Error")
        exit(0)

    # TODO: validate cells coordinates
    for argname in ["cell_from", "cell_to", "cell_through"]:
        cell = parse_cell(instance[argname])
        if cell[0] > ROWS or cell[1] > COLS:
            print(f"Invalid {argname} {cell}")
            exit(0)


def dptable_num_to(grid: _Mat[int], diag: bool = False) -> _Mat:
    """
    Build an acceleration table suitable for counting the number of paths.
    Construction starts from the cell in the top-left corner.

    Args:
        f:    game field table
        diag: allow diagonal moves

    Returns:
        A table where each cell contains the maximum utility value of any path starting from it.
    """
    assert check_matrix_shape(grid)
    assert free(grid, 0, 0) and free(grid, -1, -1)

    ROWS, COLS = len(grid), len(grid[0])
    t = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    # NOTE: cells default to zero, in some cases there is no need to assing values
    t[0][0] = 1
    for i in range(1, COLS):
        if free(grid, 0, i):
            t[0][i] = t[0][i - 1]

    for i in range(1, ROWS):
        if free(grid, i, 0):
            t[i][0] = t[i - 1][0]

    if diag:
        for i in range(1, ROWS):
            for j in range(1, COLS):
                if free(grid, i, j):
                    t[i][j] = t[i][j - 1] + t[i - 1][j] + t[i - 1][j - 1]

    else:
        for i in range(1, ROWS):
            for j in range(1, COLS):
                if free(grid, i, j):
                    t[i][j] = t[i][j - 1] + t[i - 1][j]

    assert check_same_shape(grid, t)
    return t


def dptable_num_from(g: _Mat[int], diag: bool = False) -> _Mat:
    """
    Build an accelerator table suitable for counting the number of paths.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(g)
    assert free(g, 0, 0) and free(g, -1, -1)

    ROWS, COLS = len(g), len(g[0])
    t = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    # NOTE: cells default to zero, in some cases there is no need to assing values
    t[-1][-1] = 1
    for i in reversed(range(COLS - 1)):
        if free(g, -1, i):
            t[-1][i] = t[-1][i + 1]

    for i in reversed(range(ROWS - 1)):
        if free(g, i, -1):
            t[i][-1] = t[i + 1][-1]

    if diag:
        for i in reversed(range(ROWS - 1)):
            for j in reversed(range(COLS - 1)):
                if free(g, i, j):
                    t[i][j] = t[i][j + 1] + t[i + 1][j] + t[i + 1][j + 1]

    else:
        for i in reversed(range(ROWS - 1)):
            for j in reversed(range(COLS - 1)):
                if free(g, i, j):
                    t[i][j] = t[i][j + 1] + t[i + 1][j]

    assert check_same_shape(g, t)
    return t


def dptable_opt_to(g: _Mat, diag: bool = False) -> _Mat:
    """
    Build an accelerator table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves

    Returns:
        A table where each cell contains the maximum utility value
        of any path that starts from that cell.
    """
    assert g is not None
    assert check_matrix_shape(g)
    assert free(g, 0, 0) and free(g, -1, -1)

    ROWS, COLS = len(g), len(g[0])
    t = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    t[0][0] = g[0][0]
    for i in range(1, COLS):
        if free(g, 0, i):
            t[0][i] = g[0][i] + t[0][i - 1]

    for i in range(1, ROWS):
        if free(g, i, 0):
            t[i][0] = g[i][0] + t[i - 1][0]

    if diag:
        for i in range(1, ROWS):
            for j in range(1, COLS):
                if free(g, i, j):
                    t[i][j] = g[i][j] + \
                        max([t[i][j - 1], t[i - 1][j], t[i - 1][j - 1]])

    else:
        for i in range(1, ROWS):
            for j in range(1, COLS):
                if free(g, i, j):
                    t[i][j] = g[i][j] + max(t[i][j - 1], t[i - 1][j])

    return t


def dptable_opt_from(g: _Mat, diag: bool = False) -> _Mat:
    """
    Build an accelerator table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves

    Returns:
        A table where each cell contains the maximum utility value
        of any path that ends at that cell.
    """
    assert check_matrix_shape(g)
    assert free(g, 0, 0) and free(g, -1, -1)

    ROWS, COLS = len(g), len(g[0])
    t = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    t[-1][-1] = g[-1][-1]
    for i in reversed(range(COLS - 1)):
        if free(g, -1, i):
            t[-1][i] = g[-1][i] + t[-1][i + 1]

    for i in reversed(range(ROWS - 1)):
        if free(g, i, -1):
            t[i][-1] = g[i][-1] + t[i + 1][-1]

    if diag:
        for i in reversed(range(ROWS - 1)):
            for j in reversed(range(COLS - 1)):
                if free(g, i, j):
                    t[i][j] = g[i][j] + \
                        max([t[i][j + 1], t[i + 1][j], t[i + 1][j + 1]])

    else:
        for i in reversed(range(ROWS - 1)):
            for j in reversed(range(COLS - 1)):
                if free(g, i, j):
                    t[i][j] = g[i][j] + max(t[i][j + 1], t[i + 1][j])

    return t


@dataclass
class NumOptCell:
    count: int  # the count of optimal paths ending at this cell
    value: int  # the optimal value of a path ending at this cell


def dptable_num_opt_to(f: _Mat, diag: bool = False) -> _Mat:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    ROWS, COLS = len(f), len(f[0])
    # NOTE: store (num_of_paths, opt_value) for each cell
    t = [[NumOptCell(count=0, value=0) for _ in range(COLS)]
         for _ in range(ROWS)]

    t[0][0].count = 1
    t[0][0].value = f[0][0]
    for i in range(1, COLS):  # fill first row
        if free(f, 0, i):
            t[0][i].count = t[0][i - 1].count
            t[0][i].value = f[0][i] + t[0][i - 1].value

    for i in range(1, ROWS):  # fill first column
        if free(f, i, 0):
            t[i][0].count = t[i - 1][0].count
            t[i][0].value = f[i][0] + t[i - 1][0].value

    if diag:
        for i in range(1, ROWS):
            for j in range(1, COLS):
                if free(f, i, j):
                    neighbors = [t[i][j - 1], t[i - 1][j], t[i - 1][j - 1]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    else:
        for i in range(1, ROWS):
            for j in range(1, COLS):
                if free(f, i, j):
                    neighbors = [t[i][j - 1], t[i - 1][j]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    return as_tuple_matrix(t)


def dptable_num_opt_from(f: _Mat, diag: bool = False) -> _Mat:
    """
    Build a DP table suitable for finding the maximum value.
    Construction starts from the cell in the bottom-right corner.

    Args:
        f:    game field table
        diag: allow diagonal moves
    """
    assert check_matrix_shape(f)
    assert free(f, 0, 0) and free(f, -1, -1)

    ROWS, COLS = len(f), len(f[0])
    # NOTE: store (num_of_paths, opt_value) for each cell
    t = [[NumOptCell(count=0, value=0) for _ in range(COLS)]
         for _ in range(ROWS)]

    t[-1][-1].count = 1
    t[-1][-1].value = f[-1][-1]
    for i in reversed(range(COLS - 1)):  # fill last row
        if free(f, -1, i):
            t[-1][i].count = t[-1][i + 1].count
            t[-1][i].value = f[-1][i] + t[-1][i + 1].value

    for i in reversed(range(ROWS - 1)):  # fill last column
        if free(f, i, -1):
            t[i][-1].count = t[i + 1][-1].count
            t[i][-1].value = f[i][-1] + t[i + 1][-1].value

    if diag:
        for i in reversed(range(ROWS - 1)):
            for j in reversed(range(COLS - 1)):
                if free(f, i, j):
                    neighbors = [t[i][j + 1], t[i + 1][j], t[i + 1][j + 1]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    else:
        for i in reversed(range(ROWS - 1)):
            for j in reversed(range(COLS - 1)):
                if free(f, i, j):
                    neighbors = [t[i][j + 1], t[i + 1][j]]
                    maxvalue = max(neighbors, key=lambda x: x.value).value
                    t[i][j].count = sum(map(lambda x: x.count,
                                            filter(lambda x: x.value == maxvalue, neighbors)))
                    t[i][j].value = f[i][j] + maxvalue

    return as_tuple_matrix(t)


def as_tuple_matrix(table: _Mat[NumOptCell]) -> _Mat[Tuple[int, int]]:
    return [[(x.count, x.value) for x in row] for row in table]

# TODO: is it actually required if we also need to compute all optimal paths?
def build_opt_path(dptable: _Mat, diag: bool = False) -> List[_Cell]:
    assert dptable is not None

    ROWS, COLS = len(dptable), len(dptable[0])
    FULL_PATH_LEN = ROWS + COLS - 1
    path = []
    row, col = 0, 0

    # TODO: simplify edge cases by adding unwalkable border at edges?
    if diag:
        while len(path) < FULL_PATH_LEN:
            pass

    else:
        while len(path) < FULL_PATH_LEN:
            pass

    return path


def build_all_opt_path(f: _Mat[int], dptable: _Mat, diag: bool = False) -> _Mat[_Cell]:
    assert f is not None
    assert dptable is not None
    assert len(f) == len(dptable) and len(f[0]) == len(dptable[0])

    ROWS, COLS = len(f), len(f[0])
    paths = []

    def _build_exclude_diag(path: List[_Cell]):
        if (cell := path[-1]) != (ROWS - 1, COLS - 1):  # not last cell
            row, col = cell
            value_on_opt_path = dptable[row][col] - f[row][col]
            if row < (ROWS - 1):  # check the cell in the next row
                if dptable[row + 1][col] == value_on_opt_path:
                    _build_exclude_diag(path + [(row + 1, col)])

            if col < (COLS - 1):  # check the cell in the next column
                if dptable[row][col + 1] == value_on_opt_path:
                    _build_exclude_diag(path + [(row, col + 1)])
        else:
            paths.append(path)

    def _build_include_diag(path: List[_Cell]):
        if (cell := path[-1]) != (ROWS - 1, COLS - 1):  # not last cell
            row, col = cell
            value_on_opt_path = dptable[row][col] - f[row][col]
            if row < (ROWS - 1):  # check the cell in the next row
                if dptable[row + 1][col] == value_on_opt_path:
                    _build_include_diag(path + [(row + 1, col)])

            if col < (COLS - 1):  # check the cell in the next column
                if dptable[row][col + 1] == value_on_opt_path:
                    _build_include_diag(path + [(row, col + 1)])

            if row < (ROWS - 1) and col < (COLS - 1):
                if dptable[row + 1][col + 1] == value_on_opt_path:
                    _build_include_diag(path + [(row + 1, col + 1)])
        else:  # last cell, path is complete
            paths.append(path)

    if diag:
        _build_include_diag([(0, 0)])
    else:
        _build_exclude_diag([(0, 0)])
    return paths


def conceal(dptable: _Mat):
    """
    Conceals some cells of the table
    """
    # TODO: discuss how to select the cells to obfuscate
    cells = []
    for row, col in cells:
        dptable[row][col] = -1


def solver(input_to_oracle):
    assert input_to_oracle is not None
    _LOGGER.debug("input = %s", input_to_oracle)
    instance: Final[dict] = input_to_oracle["input_data_assigned"]

    # extract and parse inputs
    grid: Final = instance["grid"]
    diag: Final = instance["diag"]
    budget: Final = instance["budget"]
    source: Final = parse_cell(instance["cell_to"])
    target: Final = parse_cell(instance["cell_from"])
    through: Final = parse_cell(instance["cell_through"])

    def splitgrids(g: _Mat) -> Tuple[_Mat, _Mat]:
        """
        Simplify the task as a pair of grid problems:
            1. subgrid from 'cell_from' to 'cell_through'
            2. subgrid from 'cell_through' to 'cell_to'

        Returns:
            the top-left and the bottom-right subgrids
        """

        # source and target cells restrict the admissible area
        # of the original grid to a rectangle subset
        
        print(grid)
        print(source) 
        print(through)
        print(target)
        #for x in range(source[0], through[0] + 1):
        #    print(x)
        #    for y in range(source[1], through[1] + 1):
        #        print(y)
        top_left_slice = [g[x][y] for x in range(source[0], through[0] + 1)
                          for y in range(source[1], through[1] + 1)]
        
        # through cell creates a chokepoint in the grid
        bottom_right_slice = [g[x][y] for x in range(through[0], target[0] + 1)
                              for y in range(through[1], target[1] + 1)]

        print(top_left_slice)
        print(bottom_right_slice)
        return top_left_slice, bottom_right_slice

    def fusegrids(tl_slice: _Mat, br_slice: _Mat) -> _Mat:
        """
        Fills a full size grid

        Args:
            tl_slice: top-left subgrid, from 'cell_from' to 'cell_through
            br_slice: bottom-right subgrig, from 'cell_through' to 'cell_to'
        """
        assert check_matrix_shape(tl_slice)
        assert check_matrix_shape(br_slice)

        ROWS, COLS = len(grid), len(grid[0])
        table = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        # place each subgrid in appropriate spot
        MARGINS = [(source, through), (through, target)]
        for subgrid, cellmin, cellmax in zip([tl_slice, br_slice], MARGINS):
            rows, cols = len(subgrid), len(subgrid[0])
            assert rows == cellmax[0] - cellmin[0]
            assert cols == cellmax[1] - cellmin[1]

            # copy over dptable
            for x in range(rows):
                for y in range(cols):
                    table[cellmin[0] + x][cellmin[1] + y] = subgrid[x][y]

        return table

    # top-left subgrid, bottom-right subgrid
    subtables = [[f(g, diag=diag) for g in splitgrids(grid)] for f in [
        dptable_num_to,
        dptable_num_from,
        dptable_opt_to,
        dptable_opt_from,
        dptable_num_opt_to,
        dptable_num_opt_from]]

    (DPtable_num_to, DPtable_num_from,
     DPtable_opt_to, DPtable_opt_from,
     DPtable_num_opt_to, DPtable_num_opt_from) = [fusegrids(*t) for t in subtables]

    # retrieve and format outputs
    # TODO: adapt solutions to different 'from' and 'to' cells
    num_paths = DPtable_num_to[-1][-1]
    num_opt_paths = DPtable_num_opt_to[-1][-1]
    opt_val = DPtable_opt_to[-1][-1]
    list_opt_path = build_all_opt_path(grid, DPtable_opt_from, diag=diag)
    opt_path = list_opt_path[0]

    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers


class verify_submission_problem_specific(verify_submission_gen):
    # , request_setups: str):
    def __init__(self, SEF, input_data_assigned: Dict, long_answer_dict: Dict):
        super().__init__(SEF, input_data_assigned, long_answer_dict)  # , request_setups)

    def verify_format(self, SEF):
        if not super().verify_format(SEF):
            return False
        if 'opt_val' in self.goals:
            g = self.goals['opt_val']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto",
                          f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")
        if 'num_opt_sols' in self.goals:
            g = self.goals['num_opt_sols']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un intero come richiesto",
                          f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            if type(g.answ) != list:
                return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una lista di oggetti (esempio ['{self.I.labels[0]}','{self.I.labels[2]}']). Hai invece immesso `{g.answ}`.")
            for ele in g.answ:
                if ele not in self.I.labels:
                    return SEF.format_NO(g, f"Ogni oggetto che collochi nella lista `{g.alias}` deve essere uno degli elementi disponibili. L'elemento `{ele}` da tè inserito non è tra questi. Gli oggetti disponibili sono {self.I.labels}.")
            SEF.format_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale",
                          f"resta da stabilire l'ammissibilità di `{g.alias}`")
        return True

    def set_up_and_cash_handy_data(self):
        if 'opt_sol' in self.goals:
            self.sum_vals = sum([val for ele, cost, val in zip(
                self.I.labels, self.I.costs, self.I.vals) if ele in self.goals['opt_sol'].answ])
            self.sum_costs = sum([cost for ele, cost, val in zip(
                self.I.labels, self.I.costs, self.I.vals) if ele in self.goals['opt_sol'].answ])

    def verify_feasibility(self, SEF):
        if not super().verify_feasibility(SEF):
            return False
        if 'opt_sol' in self.goals:
            g = self.goals['opt_sol']
            for ele in g.answ:
                if ele in self.I.forced_out:
                    return SEF.feasibility_NO(g, f"L'oggetto `{ele}` da tè inserito nella lista `{g.alias}` è tra quelli proibiti. Gli oggetti proibiti per la Richiesta {str(SEF.task_number)}, sono {self.I.forced_out}.")
            for ele in self.I.forced_in:
                if ele not in g.answ:
                    return SEF.feasibility_NO(g, f"Nella lista `{g.alias}` hai dimenticato di inserire l'oggetto `{ele}` che invece è forzato. Gli oggetti forzati per la Richiesta {str(SEF.task_number)} sono {self.I.forced_in}.")
            if self.sum_costs > self.I.Knapsack_Capacity:
                return SEF.feasibility_NO(g, f"La tua soluzione in `{g.alias}` ha costo {self.sum_costs} > Knapsack_Capacity e quindi NON è ammissibile in quanto fora il budget per la Richiesta {str(SEF.task_number)}. La soluzione da tè inserita ricomprende il sottoinsieme di oggetti `{g.alias}`= {g.answ}.")
            SEF.feasibility_OK(g, f"come `{g.alias}` hai immesso un sottoinsieme degli oggetti dell'istanza originale",
                               f"resta da stabilire l'ottimalità di `{g.alias}`")
        return True

    def verify_consistency(self, SEF):
        if not super().verify_consistency(SEF):
            return False
        if 'opt_val' in self.goals and 'opt_sol' in self.goals:
            g_val = self.goals['opt_val']
            g_sol = self.goals['opt_sol']
            if self.sum_vals != g_val.answ:
                return SEF.consistency_NO(['opt_val', 'opt_sol'], f"Il valore totale della soluzione immessa in `{g_sol.alias}` è {self.sum_vals}, non {g_val.answ} come hai invece immesso in `{g_val.alias}`. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}.")
            SEF.consistency_OK(
                ['opt_val', 'opt_sol'], f"{g_val.alias}={g_val.answ} = somma dei valori sugli oggetti in `{g_sol.alias}`.", "")
        return True
