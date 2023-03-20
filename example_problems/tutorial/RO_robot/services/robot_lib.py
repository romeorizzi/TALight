#!/usr/bin/env python3

import logging
from dataclasses import dataclass
from typing import Dict, Final, List, Tuple, TypeVar

from RO_verify_submission_gen_prob_lib import verify_submission_gen
from RO_std_eval_lib import std_eval_feedback

_UNWALKABLE = -1
"""Magic value of a cell that cannot be traversed."""

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
    # the number of feasible paths
    "num_paths": "int",

    # the number of feasible paths that collect the maximum total prize
    "num_opt_paths": "int",

    # the maximum total prize a feasible path can collect
    "opt_val": "int",

    # a path collecting the maximum possible total prize
    "opt_path": "list_of_cell",

    # the list of all optimum paths
    "list_opt_paths": "list_of_list_of_cell",

    # the DP table meant to tell the number of paths from top-left cell to the generic cell
    "DPtable_num_to": "matrix_of_matrix_of_int",

    # the DP table meant to tell the number of paths from the generic cell to the bottom-right cell"
    "DPtable_num_from": "matrix_of_matrix_of_int",

    # the DP table meant to tell the maximum value of a feasible path path moving from top-left cell to the generic cell
    "DPtable_opt_to": "matrix_of_matrix_of_int",

    # the DP table meant to tell the maximum value of a feasible path moving from the generic cell to the bottom-right cell
    "DPtable_opt_from": "matrix_of_matrix_of_int",

    # the DP table meant to tell the number of optimal paths from top-left cell to the generic cell"
    "DPtable_num_opt_to": "matrix_of_matrix_of_int",

    # the DP table meant to tell the number of optimal paths from the generic cell to the bottom-right cell.
    "DPtable_num_opt_from": "matrix_of_matrix_of_int",
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
    # cell = cell[1:-1]
    # row, col = cell.split(",")
    # row, col = ord(row.lower()) - ord("a"), int(col)
    row, col = cell
    row, col = int(row) - 1, ord(col.lower()) - ord("a")
    return (row, col)


def walkable(grid: _Mat[int], cell: _Cell) -> bool:
    """Checks whether a cell is free or forbidden."""
    assert grid is not None
    assert cell is not None
    x, y = cell
    return grid[x][y] != _UNWALKABLE


def check_matrix_shape(f: _Mat) -> bool:
    """Checks if matrix is empty."""
    if not f:
        return False

    """Checks if list is a matrix."""
    cols = len(f[0])
    if cols == 0:
        return False

    for row in f:
        if len(row) != cols:
            return False

    return True


def check_budget_bounds(budget: int) -> bool:
    """Check if the allocated budget is within the bounds specified by the problem."""
    # TODO: finalize the value of the upper bound in yaml file
    return 0 < budget < 100


def check_contains_cell(grid: _Mat, cell: _Cell) -> bool:
    """Check if the coordinates map to a valid cell."""
    assert grid is not None
    assert cell is not None
    rows, cols = shape(grid)
    return 0 <= cell[0] < rows and 0 <= cell[1] < cols


def shape(grid: _Mat) -> Tuple[int, int]:
    """
    Return:
        (number of rows, number of columns) of matrix
    """
    return len(grid), len(grid[0])


def check_cell_contiguity(c0: _Cell, c1: _Cell, diag: bool) -> bool:
    """
    Check if a cell can be reached from another one with a valid single move.

    c0:   source cell
    c1:   target cell
    diag: allow diagonal moves
    """
    assert c0 is not None
    assert c1 is not None

    # try horizontal move from c0 to c1
    if c1[0] == (c0[0] + 1) and c1[1] == c0[1]:
        return True

    # try vertical move from c0 to c1
    if c1[0] == c0[0] and c1[1] == (c0[1] + 1):
        return True

    # try diagonal move from c0 to c1
    if diag and c1[0] == (c0[0] + 1) and c1[1] == (c0[1] + 1):
        return True

    return False


def check_path_feasible(path: List[_Cell], diag: bool) -> bool:
    """
    Check if a path can be traversed from cell to cell with valid moves.

    path: sequence of cells
    diag: allow diagonal moves
    """
    assert path is not None

    for i in range(len(path) - 1):
        if not check_cell_contiguity(path[i], path[i + 1], diag=diag):
            return False

    return True


def check_instance_consistency(instance):
    _LOGGER.debug("instance = %s", instance)
    grid = instance['grid']
    rows, cols = shape(grid)
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
        if cell[0] > rows or cell[1] > cols:
            print(f"Invalid {argname} {cell}")
            exit(0)


def value(content_inside_cell: int) -> int:
    """The solution value of a cell."""
    # only cells with positive content have a value
    return max(content_inside_cell, 0)


def cost(content_inside_cell: int) -> int:
    """The solution cost on the budget of a cell."""
    # only cells with negative content have a cost
    return max(-content_inside_cell, 0)


def build_cost_table(grid: _Mat) -> _Mat:
    """Build the cost table associated with a grid."""
    assert grid is not None
    assert check_matrix_shape(grid)

    rows, cols = shape(grid)
    costs = [[cost(grid[row][col]) for col in range(cols)]
             for row in range(rows)]

    assert shape(costs) == shape(grid)
    return costs


def dptable_num_to_with_budget(grid: _Mat[int], budget: int, diag: bool = False) -> _Mat:
    assert check_matrix_shape(grid)
    assert check_budget_bounds(budget)

    rows, cols = shape(grid)
    dptable = [[[0 for _ in range(cols)] for _ in range(rows)]
               for _ in range(budget)]

    for b in range(budget):
        assert shape(dptable[b]) == shape(grid)

    costs = build_cost_table(grid)
    dptable[0][0][0] = 1
    # iterate on each cell of the grid, except the last row and column
    for row in range(rows - 1):
        for col in range(cols - 1):

            # iterate on all budget values that we may have when reaching the cell
            for b in range(budget):
                # try moving vertically by checking the cost of the move
                c = costs[row + 1][col] + b
                assert c >= 0
                if c < budget:
                    dptable[c][row + 1][col] += dptable[b][row][col]

                # try moving horizontally by checking the cost of the move
                c = costs[row][col + 1] + b
                assert c >= 0
                if c < budget:
                    dptable[c][row][col + 1] += dptable[b][row][col]

                if diag:
                    # try moving diagonally by checking the cost of the move
                    c = costs[row + 1][col + 1] + b
                    assert c >= 0
                    if c < budget:
                        dptable[c][row + 1][col + 1] += dptable[b][row][col]

    # iterate on the last column, we can only move vertically
    for row in range(rows - 1):
        for b in range(budget):
            c = costs[row][-1] + b
            if c < budget:
                dptable[c][row + 1][-1] += dptable[b][row][-1]

    # iterate on the last row, we can only move horizontally
    for col in range(cols - 1):
        for b in range(budget):
            c = costs[-1][col] + b
            assert c >= 0
            if c < budget:
                dptable[c][-1][col + 1] += dptable[b][-1][col]

    print("Calcolo path")
    print(dptable)

    return dptable


def dptable_num_to(grid: _Mat[int], budget: int , diag: bool, through) -> _Mat:
    """
    Construct a table that calculates the optimal path for each path 
    from the top left cell to the throw cell.

    Args:
        grid: game table
        budget: initial budget 
        diag: allow diagonal moves
        through: arrive cell

    Returns:
        Table containing the optimal path for each road from the top left cell to the throw cell.
    """
    assert check_matrix_shape(grid)

    rows, cols = shape(grid)

    mat = [[[0 for _ in range(budget+1)] for _ in range(cols)] for _ in range(rows)]  #NOTE: Matrix [x][y][b]

    for x in range(0, rows):
        for y in range(0, cols):
            for b in range(0, budget+1): #NOTE: I fill as many matrices as my budget
                if (walkable(grid, (x, y))):
                    if x == 0 and y == 0:
                        mat[x][y][b] = 1 #NOTE: The first cell is always one
                    elif diag:
                        if x-1 < 0 or y-1 < 0:
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]
                        else:
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] + mat[x - 1][y - 1][b]
                    else:
                        mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]
                elif b != 0: #NOTE: I fill the cells only if I'm not in the zero matrix
                    if diag:
                        if x-1 < 0 or y-1 < 0:
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]
                        else:
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] + mat[x - 1][y - 1][b]
                    else:
                        mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]


    # NOTE: Change Values in a specific row
    for y in range(through[1]+1, cols):
        for b in range(0, budget+1):
            mat[through[0]][y][b] = 0

    # NOTE: Change Values after through
    for x in range(through[0]+1, rows):
        for y in range(0, cols):
            for b in range(0, budget+1):
                mat[x][y][b] = 0

    return mat


def dptable_num_from(grid: _Mat[int], budget: int , diag: bool, through) -> _Mat:
    """
    Construct a table that calculates the optimal path for each path 
    from the throw cell to the bottom right cell.

    Args:
        grid: game table
        budget: initial budget 
        diag: allow diagonal moves
        through: arrive cell

    Returns:
        Table containing the optimal path for each road from the throw cell to the bottom right cell.
    """
    assert check_matrix_shape(grid)

    rows, cols = shape(grid)

    mat = [[[0 for _ in range(budget+1)] for _ in range(cols)] for _ in range(rows)]  #NOTE: Matrix [x][y][b]

    for x in range(0, rows):
        for y in range(0, cols):
            for b in range(0, budget+1): #NOTE: I fill as many matrices as my budget              
                if (walkable(grid, (x, y))):
                    if x == 0 and y == 0:
                        mat[x][y][b] = 1 #NOTE: The first cell is always one
                    elif diag:
                        if x-1 < 0 or y-1 < 0:
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]
                        else:
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] + mat[x - 1][y - 1][b]
                    else:
                        mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]
                elif b != 0: #NOTE: I fill the cells only if I'm not in the zero matrix
                    if diag:
                        if x-1 < 0 or y-1 < 0:
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]
                        else:
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] + mat[x - 1][y - 1][b]
                    else:
                        mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]

    # NOTE: Change Values before through
    for x in range(0, through[0]):
        for y in range(0, cols):
            for b in range(0, budget+1):
                mat[x][y][b] = 0

    # NOTE: Change Values in a specific row
    for y in range(0, through[1]):
        for b in range(0, budget+1):
            mat[through[0]][y][b] = 0

    return mat


def dptable_opt_to(grid: _Mat[int], budget: int , diag: bool, through) -> _Mat:
    """
    Build a table that calculates the maximum gain for each path 
    from the top left cell to the launch cell.

    Args:
        grid: game table
        budget: initial budget 
        diag: allow diagonal moves
        through: arrive cell

    Returns:
        Table containing the maximum gain for each street from the top left cell to the launch cell.
    """
    assert check_matrix_shape(grid)

    rows, cols = shape(grid)

    mat = [[[0 for _ in range(budget+1)] for _ in range(cols)] for _ in range(rows)]  #NOTE: Matrix [x][y][b]

    for x in range(0, rows):
        for y in range(0, cols):
            for b in range(0, budget+1): #NOTE: I fill as many matrices as my budget
                if (walkable(grid, (x, y))):
                    if x == 0 and y == 0:
                        mat[x][y][b] = grid[x][y] #NOTE: The first cell always has the gain value it possesses
                    elif diag:
                        if x-1 < 0 or y-1 < 0:
                            opt = max(mat[x][y - 1][b], mat[x - 1][y][b])
                            mat[x][y][b] = opt + grid[x][y] #NOTE: opt

                        else:
                            opt = max(mat[x][y - 1][b], mat[x - 1][y][b], mat[x - 1][y - 1][b])
                            mat[x][y][b] = opt + grid[x][y] #NOTE: opt

                    else:
                        opt = max(mat[x][y - 1][b], mat[x - 1][y][b])
                        mat[x][y][b] = opt + grid[x][y] #NOTE: opt

                elif b != 0: #NOTE: I fill the cells only if I'm not in the zero matrix
                    if diag:
                        if x-1 < 0 or y-1 < 0:
                            opt = max(mat[x][y - 1][b], mat[x - 1][y][b])
                            mat[x][y][b] = opt #NOTE: opt

                        else:
                            opt = max(mat[x][y - 1][b], mat[x - 1][y][b], mat[x - 1][y - 1][b])
                            mat[x][y][b] = opt #NOTE: opt

                    else:
                        opt = max(mat[x][y - 1][b], mat[x - 1][y][b])
                        mat[x][y][b] = opt #NOTE: opt


    # NOTE: Change Values in a specific row
    for y in range(through[1]+1, cols):
        for b in range(0, budget+1):
            mat[through[0]][y][b] = 0

    # NOTE: Change Values after through
    for x in range(through[0]+1, rows):
        for y in range(0, cols):
            for b in range(0, budget+1):
                mat[x][y][b] = 0

    return mat


def dptable_opt_from(grid: _Mat[int], budget: int , diag: bool, through) -> _Mat:
    """
    Build a table that calculates the maximum gain for each path 
    from the throw cell to the bottom right cell.

    Args:
        grid: game table
        budget: initial budget 
        diag: allow diagonal moves
        through: arrive cell

    Returns:
        Table containing the maximum gain for each street from the throw cell to the bottom right cell.
    """
    assert check_matrix_shape(grid)

    rows, cols = shape(grid)

    mat = [[[0 for _ in range(budget+1)] for _ in range(cols)] for _ in range(rows)]  #NOTE: Matrix [x][y][b]

    for x in range(0, rows):
        for y in range(0, cols):
            for b in range(0, budget+1): #NOTE: I fill as many matrices as my budget
                if (walkable(grid, (x, y))):
                    if x == 0 and y == 0:
                        mat[x][y][b] = grid[x][y] #NOTE: The first cell always has the gain value it possesses
                    elif diag:
                        if x-1 < 0 or y-1 < 0:
                            opt = max(mat[x][y - 1][b], mat[x - 1][y][b])
                            mat[x][y][b] = opt + grid[x][y] #NOTE: opt

                        else:
                            opt = max(mat[x][y - 1][b], mat[x - 1][y][b], mat[x - 1][y - 1][b])
                            mat[x][y][b] = opt + grid[x][y] #NOTE: opt

                    else:
                        opt = max(mat[x][y - 1][b], mat[x - 1][y][b])
                        mat[x][y][b] = opt + grid[x][y] #NOTE: opt

                elif b != 0: #NOTE: I fill the cells only if I'm not in the zero matrix
                    if diag:
                        if x-1 < 0 or y-1 < 0:
                            opt = max(mat[x][y - 1][b], mat[x - 1][y][b])
                            mat[x][y][b] = opt #NOTE: opt

                        else:
                            opt = max(mat[x][y - 1][b], mat[x - 1][y][b], mat[x - 1][y - 1][b])
                            mat[x][y][b] = opt #NOTE: opt

                    else:
                        opt = max(mat[x][y - 1][b], mat[x - 1][y][b])
                        mat[x][y][b] = opt #NOTE: opt


    # NOTE: Change Values before through
    for x in range(0, through[0]):
        for y in range(0, cols):
            for b in range(0, budget+1):
                mat[x][y][b] = 0

    # NOTE: Change Values in a specific row
    for y in range(0, through[1]):
        for b in range(0, budget+1):
            mat[through[0]][y][b] = 0

    return mat


@dataclass
class NumOptCell:
    count: int  # the count of optimal paths ending at this cell
    value: int  # the optimal value of a path ending at this cell


def dptable_num_opt_to(grid: _Mat[int], budget: int , diag: bool, through) -> _Mat:
    """
    Builds a table that calculates the optimal path based on the gain obtained along the road 
    and the path of the road, starting from the top left cell to the throw cell.

    Args:
        grid: game table
        budget: initial budget 
        diag: allow diagonal moves
        through: arrive cell

    Returns:
        Table containing the optimal path for each road from the top left cell to the throw cell.
    """
    
    assert check_matrix_shape(grid)

    rows, cols = shape(grid)

    mat = [[[0 for _ in range((budget+1)*2)] for _ in range(cols)] for _ in range(rows)]  #NOTE: Matrix [x][y][b]

    for x in range(0, rows):
        for y in range(0, cols):
            for b in range(0, (budget+1)*2, 2): #NOTE: Fill two values for each cycle one for gain and one for path
                if (walkable(grid, (x, y))):
                    #NOTE: Calculate the first cell
                    if x == 0 and y == 0:
                        if b % 2 == 0:
                            mat[x][y][b] = 1 #NOTE: The first cell is always one
                        else:
                            mat[x][y][b] = grid[x][y] #NOTE: the first cell always has the gain value it possesses

                    elif diag:
                        if x-1 < 0 or y-1 < 0:
                            opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1])

                            if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                            mat[x][y][b+1] = opt + grid[x][y] #NOTE: opt

                        else:
                            opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1], mat[x - 1][y - 1][b+1])

                            if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] + mat[x - 1][y - 1][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y - 1][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]#NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y - 1][b]#NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] + mat[x - 1][y - 1][b]#NOTE: num

                            mat[x][y][b+1] = opt + grid[x][y] #NOTE: opt

                    else:
                        opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1])

                        if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] #NOTE: num

                        elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x][y - 1][b] #NOTE: num

                        elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                        mat[x][y][b+1] = opt + grid[x][y] #NOTE: opt

                #NOTE: I fill the cells only if I'm not in the zero matrix
                elif b > 1:

                    if diag:
                        if x-1 < 0 or y-1 < 0:
                            opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1])

                            if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                            mat[x][y][b+1] = opt #NOTE: optt

                        else:
                            opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1], mat[x - 1][y - 1][b+1])

                            if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] + mat[x - 1][y - 1][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y - 1][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]#NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y - 1][b]#NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] + mat[x - 1][y - 1][b]#NOTE: num

                            mat[x][y][b+1] = opt #NOTE: opt

                    else:
                        opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1])

                        if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] #NOTE: num

                        elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x][y - 1][b] #NOTE: num
                            
                        elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                        mat[x][y][b+1] = opt #NOTE: opt

    # NOTE: Change Values in a specific row
    for y in range(through[1]+1, cols):
        for b in range(0, (budget+1)*2, 2):
            mat[through[0]][y][b] = 0
            mat[through[0]][y][b+1] = 0

    # NOTE: Change Values after through
    for x in range(through[0]+1, rows):
        for y in range(0, cols):
            for b in range(0, (budget+1)*2, 2):
                mat[x][y][b] = 0
                mat[x][y][b+1] = 0

    return mat


def dptable_num_opt_from(grid: _Mat[int], budget: int , diag: bool, through) -> _Mat:
    """
    Builds a table that calculates the optimal path based on the gain obtained along the road 
    and the path of the road, starting from the throw cell to the bottom right cell.

    Args:
        grid: game table
        budget: initial budget 
        diag: allow diagonal moves
        through: arrive cell

    Returns:
        Table containing the optimal path for each street from the throw cell to the bottom right cell.
    """
    
    assert check_matrix_shape(grid)

    rows, cols = shape(grid)

    mat = [[[0 for _ in range((budget+1)*2)] for _ in range(cols)] for _ in range(rows)]  #NOTE: Matrix [x][y][b]

    for x in range(0, rows):
        for y in range(0, cols):
            for b in range(0, (budget+1)*2, 2): #NOTE: Fill two values for each cycle one for gain and one for path
                if (walkable(grid, (x, y))):
                    #NOTE: Calculate the first cell
                    if x == 0 and y == 0:
                        if b % 2 == 0:
                            mat[x][y][b] = 1 #NOTE: The first cell is always one
                        else:
                            mat[x][y][b] = grid[x][y] #NOTE: the first cell always has the gain value it possesses 

                    elif diag:
                        if x-1 < 0 or y-1 < 0:
                            opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1])

                            if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                            mat[x][y][b+1] = opt + grid[x][y] #NOTE: opt

                        else:
                            opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1], mat[x - 1][y - 1][b+1])

                            if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] + mat[x - 1][y - 1][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y - 1][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]#NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y - 1][b]#NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] + mat[x - 1][y - 1][b]#NOTE: num

                            mat[x][y][b+1] = opt + grid[x][y] #NOTE: opt

                    else:
                        opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1])

                        if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] #NOTE: num

                        elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x][y - 1][b] #NOTE: num

                        elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                        mat[x][y][b+1] = opt + grid[x][y] #NOTE: opt

                #NOTE: I fill the cells only if I'm not in the zero matrix
                elif b > 1:

                    if diag:
                        if x-1 < 0 or y-1 < 0:
                            opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1])

                            if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                            mat[x][y][b+1] = opt #NOTE: optt

                        else:
                            opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1], mat[x - 1][y - 1][b+1])

                            if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] + mat[x - 1][y - 1][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y - 1][b] #NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt != mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b]#NOTE: num

                            elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y - 1][b]#NOTE: num

                            elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1] and opt == mat[x - 1][y - 1][b+1]):
                                mat[x][y][b] = mat[x - 1][y][b] + mat[x - 1][y - 1][b]#NOTE: num

                            mat[x][y][b+1] = opt #NOTE: opt

                    else:
                        opt = max(mat[x][y - 1][b+1], mat[x - 1][y][b+1])

                        if(opt == mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x][y - 1][b] + mat[x - 1][y][b] #NOTE: num

                        elif(opt == mat[x][y - 1][b+1] and opt != mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x][y - 1][b] #NOTE: num
                            
                        elif(opt != mat[x][y - 1][b+1] and opt == mat[x - 1][y][b+1]):
                            mat[x][y][b] = mat[x - 1][y][b] #NOTE: num

                        mat[x][y][b+1] = opt #NOTE: opt

    # NOTE: Change Values before through
    for x in range(0, through[0]):
        for y in range(0, cols):
            for b in range(0, (budget+1)*2, 2):
                mat[x][y][b] = 0
                mat[x][y][b+1] = 0

    # NOTE: Change Values in a specific row
    for y in range(0, through[1]):
        for b in range(0, (budget+1)*2, 2):
            mat[through[0]][y][b] = 0
            mat[through[0]][y][b+1] = 0

    return mat


def as_tuple_matrix(table: _Mat[NumOptCell]) -> _Mat[Tuple[int, int]]:
    return [[(x.count, x.value) for x in row] for row in table]


def build_opt_path(dptable: _Mat, diag: bool = False) -> List[_Cell]:
    # TODO: is it actually required if we also need to compute all optimal paths?
    assert dptable is not None

    ROWS, COLS = len(dptable), len(dptable[0])
    FULL_PATH_LEN = ROWS + COLS - 1
    path = []
    row, col = 0, 0

    # TODO: simplify edge cases by adding unwalkable border at edges?
    # if diag:
    #     while len(path) < FULL_PATH_LEN:
    #         pass

    # else:
    #     while len(path) < FULL_PATH_LEN:
    #         pass

    return path


def build_all_opt_path(f: _Mat[int], dptable: _Mat, diag: bool = False) -> _Mat[_Cell]:
    assert f is not None
    assert dptable is not None
    assert shape(f) == shape(dptable)

    rows, cols = shape(f)
    paths = []

    def _build_exclude_diag(path: List[_Cell]):
        if (cell := path[-1]) != (rows - 1, cols - 1):  # not last cell
            row, col = cell
            value_on_opt_path = dptable[row][col] - f[row][col]
            if row < (rows - 1):  # check the cell in the next row
                if dptable[row + 1][col] == value_on_opt_path:
                    _build_exclude_diag(path + [(row + 1, col)])

            if col < (cols - 1):  # check the cell in the next column
                if dptable[row][col + 1] == value_on_opt_path:
                    _build_exclude_diag(path + [(row, col + 1)])
        else:
            paths.append(path)

    def _build_include_diag(path: List[_Cell]):
        if (cell := path[-1]) != (rows - 1, cols - 1):  # not last cell
            row, col = cell
            value_on_opt_path = dptable[row][col] - f[row][col]
            if row < (rows - 1):  # check the cell in the next row
                if dptable[row + 1][col] == value_on_opt_path:
                    _build_include_diag(path + [(row + 1, col)])

            if col < (cols - 1):  # check the cell in the next column
                if dptable[row][col + 1] == value_on_opt_path:
                    _build_include_diag(path + [(row, col + 1)])

            if row < (rows - 1) and col < (cols - 1):
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
    # _LOGGER.debug("input = %s", input_to_oracle)
    instance: Final[dict] = input_to_oracle["input_data_assigned"]
    print(input_to_oracle)

    # extract and parse inputs
    grid: Final = instance["grid"]
    diag: Final = instance["diag"]
    budget: Final = instance["budget"]
    source: Final = parse_cell(instance["cell_from"])
    target: Final = parse_cell(instance["cell_to"])
    through: Final = parse_cell(instance["cell_through"])

    print("\nFrom:", source, "Through:", through, "To:", target)
    print("Diagonal movement:", diag)

    # top-left subgrid, bottom-right subgrid
    # subtables = [[f(g, diag=diag) for g in splitgrids(grid)] for f in [
    #     dptable_num_to,
    #     dptable_num_from,
    #     dptable_opt_to,
    #     dptable_opt_from,
    #     dptable_num_opt_to,
    #     dptable_num_opt_from]]

    # (DPtable_num_to, DPtable_num_from,
    #  DPtable_opt_to, DPtable_opt_from,
    #  DPtable_num_opt_to, DPtable_num_opt_from) = [fusegrids(*t) for t in subtables]

    print("\nProblem", *grid, sep="\n")

    ##
    # NOTE: DPtable_num
    ##
    DPtable_num_to = dptable_num_to(grid, budget, diag, through)
    print("\nDPtable_num_to", *DPtable_num_to, sep="\n")
    DPtable_num_from = dptable_num_from(grid, budget, diag, through)
    print("\nDPtable_num_from", *DPtable_num_from, sep="\n")
    
    ##
    # NOTE: DPtable_opt
    ##
    DPtable_opt_to = dptable_opt_to(grid, budget, diag, through)
    print("\nDPtable_opt_to", *DPtable_opt_to, sep="\n")
    DPtable_opt_from = dptable_opt_from(grid, budget, diag, through)
    print("\nDPtable_opt_from", *DPtable_opt_from, sep="\n")

    ##
    # NOTE: DPtable_num_opt
    ##
    DPtable_num_opt_to = dptable_num_opt_to(grid, budget, diag, through)
    print("\nDPtable_num_opt_to", *DPtable_num_opt_to, sep="\n")
    DPtable_num_opt_from = dptable_num_opt_from(grid, budget, diag, through)
    print("\nDPtable_num_opt_from", *DPtable_num_opt_from, sep="\n")

    # first move from <source> cell to <through> cell
    # then move from <through> cell to <target> cell
    # TODO: adapt solutions to different 'from' and 'to' cells
    x, y = through
    num_paths = sum([DPtable_num_to[x][y][b] * DPtable_num_from[x][y][b]
                    for b in range(budget + 1)])
    opt_val = sum([DPtable_opt_to[x][y][b] * DPtable_opt_from[x][y][b]
                    for b in range(budget + 1)])
    num_opt_paths = sum([DPtable_num_opt_to[x][y][b] * DPtable_num_opt_from[x][y][b]
                         for b in range(budget + 1)])

    list_opt_paths = build_all_opt_path(grid, DPtable_opt_from, diag)
    opt_path = list_opt_paths[0] if len(list_opt_paths) > 0 else []

    oracle_answers = {}
    for std_name, ad_hoc_name in input_to_oracle["request"].items():
        oracle_answers[ad_hoc_name] = locals()[std_name]
    return oracle_answers


class verify_submission_problem_specific(verify_submission_gen):
    def __init__(self, SEF, input_data_assigned: Dict, long_answer_dict: Dict):
        super().__init__(SEF, input_data_assigned, long_answer_dict)

    def verify_format(self, SEF: std_eval_feedback):
        if not super().verify_format(SEF):
            return False

        # TODO: format checks

        return True

    def set_up_and_cash_handy_data(self):
        if 'opt_sol' in self.goals:
            self.sum_vals = sum([val for ele, cost, val in zip(
                self.I.labels, self.I.costs, self.I.vals) if ele in self.goals['opt_sol'].answ])
            self.sum_costs = sum([cost for ele, cost, val in zip(
                self.I.labels, self.I.costs, self.I.vals) if ele in self.goals['opt_sol'].answ])

        self.beg = parse_cell(self.I.cell_from)
        self.mid = parse_cell(self.I.cell_through)
        self.end = parse_cell(self.I.cell_to)

        rows, cols = shape(self.I.grid)
        self.dptable_shape = (rows, cols, self.I.budget)

    def verify_feasibility(self, SEF: std_eval_feedback):
        if not super().verify_feasibility(SEF):
            return False

        if 'opt_path' == self.goals:
            path = self.goals['opt_path'].answ
            print(path)
            if not check_path_feasible(path, diag=self.I.diag):
                return SEF.feasibility_NO('opt_path', f"Path {path} cannot be followed by valid moves")

        if 'list_opt_path' == self.goals:
            g = self.goals['list_opt_path']
            for path in g.answ:
                if not check_path_feasible(path, diag=self.I.diag):
                    return SEF.feasibility_NO('list_opt_path', f"Path {path} cannot be followed by valid moves")

        dptables = [
            'DPtable_num_to', 'DPtable_num_from',
            'DPtable_opt_to', 'DPtable_opt_from',
            'DPtable_num_opt_to', 'DPtable_num_opt_from'
        ]
        for dptable in dptables:
            if dptable in self.goals:
                if shape(self.goals[dptable]) != self.dptable_shape:
                    return SEF.feasibility_NO(dptable, f"")

        return True

    def verify_consistency(self, SEF: std_eval_feedback):
        if not super().verify_consistency(SEF):
            return False

        # TODO: consistency checks

        return True
