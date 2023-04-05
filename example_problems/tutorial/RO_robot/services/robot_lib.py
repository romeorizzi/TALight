#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Final, List, Tuple, TypeVar
import itertools

import numpy as np

from RO_verify_submission_gen_prob_lib import verify_submission_gen
from RO_std_eval_lib import std_eval_feedback


instance_objects_spec = [
    ('grid','matrix_of_int'),
    ('budget',int),
    ('diag',bool),
    ('cell_from','list_of_str'),
    ('cell_to','list_of_str'),
    ('cell_through','list_of_str'),
    ('CAP_FOR_NUM_SOLS',int),
    ('CAP_FOR_NUM_OPT_SOLS',int),
]
additional_infos_spec = [
    ('partialDP_to', 'matrix_of_int'),
    ('partialDP_from', 'matrix_of_int'),
]
answer_objects_spec = {
    'num_paths':'int', # the number of feasible paths
    'num_opt_paths':'int', # the number of feasible paths that collect the maximum total prize
    'opt_val':'int', # the maximum total prize a feasible path can collect
    'opt_path':'list_of_cell', # a path collecting the maximum possible total prize
    'list_opt_paths':'list_of_list_of_cell', # the list of all optimum paths
    'DPtable_num_to':'matrix_of_matrix_of_int', # the DP table meant to tell the number of paths from top-left cell to the generic cell
    'DPtable_num_from':'matrix_of_matrix_of_int', # the DP table meant to tell the number of paths from the generic cell to the bottom-right cell
    'DPtable_opt_to':'matrix_of_matrix_of_int',# the DP table meant to tell the maximum value of a feasible path path moving from top-left cell to the generic cell
    'DPtable_opt_from':'matrix_of_matrix_of_int', # the DP table meant to tell the maximum value of a feasible path moving from the generic cell to the bottom-right cell
    'DPtable_num_opt_to':'matrix_of_matrix_of_int', # the DP table meant to tell the number of optimal paths from top-left cell to the generic cell
    'DPtable_num_opt_from':'matrix_of_matrix_of_int', # the DP table meant to tell the number of optimal paths from the generic cell to the bottom-right cell
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
    'CAP_FOR_NUM_SOLS': 10,
    'CAP_FOR_NUM_OPT_SOLS': 10
}

_T = TypeVar("_T")

_Cell = Tuple[int, int]
_Path = list[_Cell]
_Mat = List[List[_T]]


@dataclass
class Instance:
    grid: np.ndarray
    cost: int
    diag: bool
    beg: _Cell
    mid: _Cell
    end: _Cell


def _map(x, y):
    return f"({str(x + 1)},{chr(ord('A') + y)})"


def parse_cell(coords: list[str]) -> _Cell:
    # the format specification is [row, col]
    row, col = coords
    row, col = int(row) - 1, ord(col.lower()) - ord("a")
    return (row, col)


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
    return 0 <= budget < 100


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


def cellgain(content_inside_cell: int) -> int:
    """The solution gain of a cell."""
    # only cells with positive content have a value
    return max(content_inside_cell, 0)


def cellcost(content_inside_cell: int) -> int:
    """The solution cost on the budget of a cell."""
    # only cells with negative content have a cost
    return max(-content_inside_cell, 0)


def build_cost_table(grid: _Mat) -> _Mat:
    """Build the cost table associated with a grid."""
    assert grid is not None
    assert check_matrix_shape(grid)

    rows, cols = shape(grid)
    costs = [[cellcost(grid[row][col]) for col in range(cols)]
             for row in range(rows)]

    assert shape(costs) == shape(grid)
    return costs


def dp_num_to(grid: np.ndarray, cell: _Cell, budget: int, diag: bool) -> np.ndarray:
    """
    Construct a table that calculates the number of paths
    from a specific cell to any cell.

    Args:
        grid:   game table
        cell:   reference cell
        budget: max budget for a path 
        diag:   allow diagonal moves

    Returns:
        DP table
    """
    row0, col0 = cell
    rows, cols = grid.shape
    # NOTE: matrix format [budget][rows][cols]
    mat = np.zeros((budget + 1, rows, cols), dtype=np.intc)
    for b in range(budget + 1):
        if cellcost(grid[row0][col0]) <= b:
            mat[b][row0][col0] = 1

    # NOTE: start iteration from the reference cell
    for b in range(budget + 1):  # iterate on all possible values of budget
        for x in range(row0, rows):
            for y in range(col0, cols):
                cost_at_prev_cell = b - cellcost(grid[x][y])
                if cost_at_prev_cell >= 0:
                    # move from the top cell if there is a previous row
                    if x > 0:
                        mat[b][x][y] += mat[cost_at_prev_cell][x - 1][y]

                    # move from the left cell if there is a previous col
                    if y > 0:
                        mat[b][x][y] += mat[cost_at_prev_cell][x][y - 1]

                    # move diagonally from the top-left cell
                    if diag and x > 0 and y > 0:
                        mat[b][x][y] += mat[cost_at_prev_cell][x - 1][y - 1]

    return mat


def dp_num_from(grid: np.ndarray, cell: _Cell, budget: int, diag: bool) -> np.ndarray:
    """
    Construct a table that calculates the number of paths
    from any cell to a specific cell.

    Args:
        grid:   game table
        cell:   reference cell
        budget: max budget for a valid path 
        diag:   allow diagonal moves

    Returns:
        DP table
    """
    # flip both the field and the reference cell
    grid = np.flip(grid)
    # cells are zero-indexed, so we need to offset the coordinates
    cell = (grid.shape[0] - cell[0] - 1, grid.shape[1] - cell[1] - 1)
    result = dp_num_to(grid, cell, budget, diag)
    # also flip the result back, but only on the grid axis
    assert result.shape == (budget + 1, *grid.shape),\
        "The expected dptable format is [budget][row][col]"
    return np.flip(result, (1, 2))


def dp_opt_to(grid: np.ndarray, cell: _Cell, budget: int, diag: bool) -> np.ndarray:
    """
    Build a table that calculates the maximum gain for each path 
    from a specific cell to any cell.

    Args:
        grid:   game table
        cell:   reference cell
        budget: max budget for a valid path
        diag:   allow diagonal moves

    Returns:
        DP table
    """
    row0, col0 = cell
    rows, cols = grid.shape
    # NOTE: matrix format [budget][rows][cols]
    mat = np.full((budget + 1, rows, cols), fill_value=-1, dtype=np.intc)
    for b in range(budget + 1):
        if cellcost(grid[row0][col0]) <= b:
            mat[b][row0][col0] = cellgain(grid[row0][col0])

    # NOTE: start iteration from the reference cell
    for b in range(budget + 1):  # iterate on all possible values of budget
        for x in range(row0, rows):
            for y in range(col0, cols):
                prev_cost = b - cellcost(grid[x][y])
                if prev_cost >= 0:
                    v = cellgain(grid[x][y])
                    # move from the top cell if there is a previous row
                    if x > 0 and mat[prev_cost][x - 1][y] != -1:
                        mat[b][x][y] = max(mat[b][x][y],
                                           mat[prev_cost][x - 1][y] + v)

                    # move from the left cell if there is a previous col
                    if y > 0 and mat[prev_cost][x][y - 1] != -1:
                        mat[b][x][y] = max(mat[b][x][y],
                                           mat[prev_cost][x][y - 1] + v)

                    # move diagonally from the top-left cell
                    if diag and x > 0 and y > 0 and mat[prev_cost][x - 1][y - 1] != -1:
                        mat[b][x][y] = max(mat[b][x][y],
                                           mat[prev_cost][x - 1][y - 1] + v)

    return mat


def dp_opt_from(grid: np.ndarray, cell: _Cell, budget: int, diag: bool) -> np.ndarray:
    """
    Build a table that calculates the maximum gain for each path 
    from any cell to a specific cell.

    Args:
        grid:   game table
        cell:   reference cell
        budget: max budget for a valid path
        diag:   allow diagonal moves

    Returns:
        DP table
    """
    # flip both the field and the reference cell
    grid = np.flip(grid)
    # cells are zero-indexed, so we need to offset the coordinates
    cell = (grid.shape[0] - cell[0] - 1, grid.shape[1] - cell[1] - 1)
    result = dp_opt_to(grid, cell, budget, diag)
    # also flip the result back, but only on the grid axis
    assert result.shape == (budget + 1, *grid.shape),\
        "The expected dptable format is [budget][row][col]"
    return np.flip(result, (1, 2))


def dp_num_opt_to(
        grid: np.ndarray, cell: _Cell, dptable: np.ndarray, budget: int, diag: bool
) -> np.ndarray:
    """
    Build a table that calculates the number of optimal paths
    from any cell to a specific cell.

    Args:
        grid:   game table
        cell:   reference cell
        budget: max budget for a valid path
        diag:   allow diagonal moves
        dptable:

    Returns:
        DP table
    """
    row0, col0 = cell
    rows, cols = grid.shape
    # NOTE: matrix format [budget][rows][cols]
    mat = np.zeros((budget + 1, rows, cols), dtype=np.intc)
    for b in range(budget + 1):
        if cellcost(grid[row0][col0]) <= b:
            mat[b][row0][col0] = 1

    # NOTE: start iteration from the reference cell
    for x in range(cell[0], rows):
        for y in range(cell[1], cols):
            for b in range(budget + 1):
                # the budget left at a previous cell required to move in the current cell
                # with the current total budget
                bud = b - cellcost(grid[x][y])

                # the optimal value of a path that gets at the current
                opt = dptable[bud][x][y] - cellgain(grid[x][y])

                if x > 0:  # can move by row
                    if dptable[bud][x - 1][y] == opt:  # and the path is optimal
                        mat[b][x][y] += mat[bud][x - 1][y]

                if y > 0:  # can move by column
                    if dptable[bud][x][y - 1] == opt:  # and the path is optimal
                        mat[b][x][y] += mat[bud][x][y - 1]

                if diag and x > 0 and y > 0:  # can move diagonally
                    if dptable[bud][x - 1][y - 1] == opt:  # and the path is optimal
                        mat[b][x][y] += mat[bud][x - 1][y - 1]

    return mat


def dp_num_opt_from(
        grid: np.ndarray, cell: _Cell, dptable: np.ndarray, budget: int, diag: bool
) -> np.ndarray:
    # flip both the field and the reference cell
    grid = np.flip(grid)
    assert dptable.shape == (budget + 1, *grid.shape),\
        "The expected dptable format is [budget][row][col]"
    dptable = np.flip(dptable, (1, 2))
    # cells are zero-indexed, so we need to offset the coordinates
    cell = (grid.shape[0] - cell[0] - 1, grid.shape[1] - cell[1] - 1)
    result = dp_num_opt_to(grid, cell, dptable, budget, diag)
    # also flip the result back, but only on the grid axis
    assert result.shape == (budget + 1, *grid.shape),\
        "The expected dptable format is [budget][row][col]"
    return np.flip(result, (1, 2))


def opt_paths_beg_to_mid(
        p: Instance, opt_beg2any: np.ndarray, cost: int
) -> list[_Path]:
    assert cost >= 0
    paths = []

    def build(path: list[_Cell], c: int):
        x, y = path[-1]

        # check if we have reached the end
        if (x, y) == p.beg:
            # NOTE: the build process is reversed, so flip the path order
            path.reverse()
            paths.append(path)
            return

        # remove the cost of the current cell
        opt = opt_beg2any[c][x][y]
        c1 = c - cellcost(p.grid[x][y])
        assert c1 >= 0, "Underflowed minimum cost"

        # if the result path is optimal, keep building from the cell in the previuos row
        if x > p.beg[0]:
            if opt_beg2any[c1][x - 1][y] + cellgain(p.grid[x - 1][y]) == opt:
                build(path + [(x - 1, y)], c1)

        # if the result path is optimal, keep building from the cell in the previuos column
        if y > p.beg[1]:
            if opt_beg2any[c1][x][y - 1] + cellgain(p.grid[x][y - 1]) == opt:
                build(path + [(x, y - 1)], c1)

        # if the result path is optimal, keep building from the cell in the previuos diagonal
        if p.diag and x > p.beg[0] and y > p.beg[1]:
            if opt_beg2any[c1][x - 1][y - 1] + cellgain(p.grid[x - 1][y - 1]) == opt:
                build(path + [(x - 1, y - 1)], c1)

    # NOTE: for this case the build process is reversed,
    # starting from the <mid> cell and moving towards the <beg> cell
    build([p.mid], cost)
    return paths


def opt_paths_mid_to_end(
        p: Instance, opt_any2end: np.ndarray, cost: int
) -> list[_Path]:
    assert cost >= 0
    paths = []

    def build(path: list[_Cell], c: int):
        x, y = path[-1]

        # check if we have reached the end
        if (x, y) == p.end:
            # NOTE: the build process is reversed, so flip the path order
            paths.append(path)
            return

        # remove the cost of the current cell
        opt = opt_any2end[c][x][y]
        c1 = c + cellcost(p.grid[x][y])
        assert c1 <= cost, "Overflowed maximum cost"

        # if the result path is optimal, keep building from the cell in the previuos row
        if x < p.end[0]:
            if opt_any2end[c1][x + 1][y] + cellgain(p.grid[x + 1][y]) == opt:
                build(path + [(x + 1, y)], c1)

        # if the result path is optimal, keep building from the cell in the previuos column
        if y < p.end[1]:
            if opt_any2end[c1][x][y + 1] + cellgain(p.grid[x][y + 1]) == opt:
                build(path + [(x, y + 1)], c1)

        # if the result path is optimal, keep building from the cell in the previuos diagonal
        if p.diag and x < p.end[0] and y < p.end[1]:
            if opt_any2end[c1][x + 1][y + 1] + cellgain(p.grid[x + 1][y + 1]) == opt:
                build(path + [(x + 1, y + 1)], c1)

    build([p.mid], cost)
    return paths


def yield_opt_paths(p: Instance, opt_beg2any: np.ndarray, opt_any2end: np.ndarray):
    assert opt_beg2any.shape == opt_any2end.shape

    # list all cost combinations for the subpaths with associated complete path value
    midx, midy = p.mid
    solutions = list[tuple[int, int, int]]()
    for c0, c1 in zip(range(p.cost + 1), reversed(range(p.cost + 1))):
        value = opt_beg2any[c0][midx][midy] + opt_any2end[c1][midx][midy]
        solutions.append((c0, c1, value))

    assert len(solutions) > 0

    # find all cost combinations for the subpaths that provide a path with the optimal value
    opt = max(map(lambda x: x[-1], solutions))
    solutions = [(c0, c1) for c0, c1, value in solutions if value == opt]
    assert len(solutions) > 0

    # find all paths that produce the optimal value as sum
    for c0, c1 in solutions:
        paths_beg_to_mid = opt_paths_beg_to_mid(
            p, opt_beg2any=opt_beg2any, cost=c0)
        paths_mid_to_end = opt_paths_mid_to_end(
            p, opt_any2end=opt_any2end, cost=c1)
        # merge all possible subpaths combinations
        for p0 in paths_beg_to_mid:
            for p1 in paths_mid_to_end:
                # the checkpoint cell <mid> appears in both paths,
                # so we remove it from the end of the beg->mid path
                yield p0[:-1] + p1


def conceal(dptable: _Mat):
    """
    Conceals some cells of the table
    """
    # TODO: discuss how to select the cells to obfuscate
    cells = []
    for row, col in cells:
        dptable[row][col] = -1


def query_num(num_beg2any: np.ndarray, num_any2end: np.ndarray, through: _Cell):
    """
    Compute metric <num> from paths.

    Args:
        num_beg2any: dptable from the top-left cell to a generic cell
        num_any2end: dptable from a generic cell to the bottom-right cell
        through: checkpoint cell

    Return:
        num of paths that start from A, go through B and end at C
    """
    assert num_beg2any.shape == num_any2end.shape
    x, y = through
    budget = num_beg2any.shape[0]  # dptable matrix is [budget][row][col]

    solutions = list[int]()
    for b0, b1 in zip(range(budget), reversed(range(budget))):
        num_A_to_B = num_beg2any[b0][x][y]
        num_B_to_C = num_any2end[b1][x][y]
        solutions.append(num_A_to_B * num_B_to_C)

    # pick all the solutions
    return sum(solutions)


def query_opt(opt_beg2any: np.ndarray, opt_any2end: np.ndarray, through: _Cell):
    assert opt_beg2any.shape == opt_any2end.shape
    x, y = through
    budget = opt_beg2any.shape[0]  # dptable matrix is [budget][row][col]

    solutions = list[int]()
    for b0, b1 in zip(range(budget), reversed(range(budget))):
        opt_A_to_B = opt_beg2any[b0][x][y]
        opt_B_to_C = opt_any2end[b1][x][y]
        solutions.append(opt_A_to_B + opt_B_to_C)

    # pick the best solution
    return max(solutions)


def query_num_opt(
        opt_beg2any: np.ndarray,
        opt_any2end: np.ndarray,
        num_opt_beg2any: np.ndarray,
        num_opt_any2end: np.ndarray,
        through: _Cell):

    assert opt_beg2any.shape == opt_any2end.shape
    assert num_opt_beg2any.shape == num_opt_any2end.shape
    x, y = through
    budget = num_opt_beg2any.shape[0]  # dptable matrix is [budget][row][col]

    solutions = list[tuple[int, int]]()
    for b0, b1 in zip(range(budget), reversed(range(budget))):
        opt_A_to_B = opt_beg2any[b0][x][y]
        num_opt_A_to_B = num_opt_beg2any[b0][x][y]

        opt_B_to_C = opt_any2end[b1][x][y]
        num_opt_B_to_C = num_opt_any2end[b1][x][y]

        num = num_opt_A_to_B * num_opt_B_to_C
        opt = opt_A_to_B + opt_B_to_C
        solutions.append((num, opt))

    # pick all solutions that provide the optimal total path value
    opt_total_val = max(map(lambda x: x[1], solutions))
    opt_solutions = [x[0] for x in solutions if x[1] == opt_total_val]
    return sum(opt_solutions)


def solver(input_to_oracle):
    assert input_to_oracle is not None

    instance: Final[dict] = input_to_oracle["input_data_assigned"]

    # extract and parse inputs
    grid: Final = np.array(instance["grid"])
    diag: Final = instance["diag"]
    budget: Final = instance["budget"]
    beg: Final = parse_cell(instance["cell_from"])
    end: Final = parse_cell(instance["cell_to"])
    mid: Final = parse_cell(instance["cell_through"])
    CAP_FOR_NUM_OPT_SOLS: Final[int] = min(
        instance["CAP_FOR_NUM_OPT_SOLS"], limits["CAP_FOR_NUM_OPT_SOLS"])

    expected_dptable_shape = (budget + 1, *grid.shape)

    DPtable_num_to = dp_num_to(
        grid, cell=beg, budget=budget, diag=diag)
    assert DPtable_num_to.shape == expected_dptable_shape
    DPtable_num_from = dp_num_from(
        grid, cell=end, budget=budget, diag=diag)
    assert DPtable_num_to.shape == expected_dptable_shape

    DPtable_opt_to = dp_opt_to(
        grid, cell=beg, budget=budget, diag=diag)
    assert DPtable_opt_to.shape == expected_dptable_shape
    DPtable_opt_from = dp_opt_from(
        grid, cell=end, budget=budget, diag=diag)
    assert DPtable_opt_from.shape == expected_dptable_shape

    DPtable_num_opt_to = dp_num_opt_to(
        grid, beg, DPtable_opt_to, budget, diag)
    assert DPtable_num_opt_to.shape == expected_dptable_shape
    DPtable_num_opt_from = dp_num_opt_from(
        grid, end, DPtable_opt_from, budget, diag)
    assert DPtable_num_opt_from.shape == expected_dptable_shape

    num_paths = query_num(DPtable_num_to, DPtable_num_from, mid)
    opt_val = query_opt(DPtable_opt_to, DPtable_opt_from, mid)
    num_opt_paths = query_num_opt(DPtable_opt_to, DPtable_opt_from,
                                  DPtable_num_opt_to, DPtable_num_opt_from, mid)

    problem = Instance(
        grid=grid,
        cost=budget,
        diag=diag,
        beg=beg,
        mid=mid,
        end=end,
    )

    # extract only the required limited number of solutions
    list_opt_paths = list(itertools.islice(
        yield_opt_paths(problem, DPtable_opt_to, DPtable_opt_from),
        CAP_FOR_NUM_OPT_SOLS))
    opt_path = list_opt_paths[0] if len(list_opt_paths) > 0 else []

    # convert dptable to standard python (nested) lists
    DPtable_num_to = DPtable_num_to.tolist()
    DPtable_num_from = DPtable_num_from.tolist()
    DPtable_opt_to = DPtable_opt_to.tolist()
    DPtable_opt_from = DPtable_opt_from.tolist()
    DPtable_num_opt_to = DPtable_num_opt_to.tolist()
    DPtable_num_opt_from = DPtable_num_opt_from.tolist()

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

        print("---------1--------------")
        print(self.goals)
        print("---------2--------------")
        print(self.long_answer_dict)
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

        if 'opt_path' in self.goals:
            path = self.goals['opt_path'].answ
            if not check_path_feasible(path, diag=self.I.diag):
                return SEF.feasibility_NO('opt_path', f"Path {path} cannot be followed by valid moves")

        if 'list_opt_path' in self.goals:
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
        if 'opt_val' in self.goals:
            opt_val = self.goals['opt_val']

            if 'opt_path' in self.goals:
                opt_path = [parse_cell(x) for x in self.goals['opt_path']]

            if 'list_opt_paths' in self.goals:
                list_opt_paths = [[parse_cell(x) for x in p]
                                  for p in self.goals['list_opt_paths']]

        return True
