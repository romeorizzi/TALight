#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, Final, List, Tuple, TypeVar
import itertools

import numpy as np

from RO_verify_submission_gen_prob_lib import verify_submission_gen
from RO_std_eval_lib import std_eval_feedback


instance_objects_spec = [
    ("grid", "matrix_of_int"),
    ("budget", int),
    ("diag", bool),
    ("cell_from", tuple[int, str]),
    ("cell_to", tuple[int, str]),
    ("cell_through", tuple[int, str]),
    ('CAP_FOR_NUM_SOLS',int),
    ('CAP_FOR_NUM_OPT_SOLS',int),
]
additional_infos_spec = [
    ('partialDP_to', 'matrix_of_int'),
    ('partialDP_from', 'matrix_of_int'),
]
answer_objects_spec = {
    'num_paths': 'int',  # the number of feasible paths
    # the number of feasible paths that collect the maximum total prize
    'num_opt_paths': 'int',
    'opt_val': 'int',  # the maximum total prize a feasible path can collect
    # a path collecting the maximum possible total prize
    'opt_path': 'list_of_list_of_str',
    'list_opt_paths': 'list_of_list_of_list_of_str',  # the list of all optimum paths
    # the DP table meant to tell the number of paths from top-left cell to the generic cell
    'DPtable_num_to': 'matrix_of_list_of_int',
    # the DP table meant to tell the number of paths from the generic cell to the bottom-right cell
    'DPtable_num_from': 'matrix_of_list_of_int',
    # the DP table meant to tell the maximum value of a feasible path path moving from top-left cell to the generic cell
    'DPtable_opt_to': 'matrix_of_list_of_int',
    # the DP table meant to tell the maximum value of a feasible path moving from the generic cell to the bottom-right cell
    'DPtable_opt_from': 'matrix_of_list_of_int',
    # the DP table meant to tell the number of optimal paths from top-left cell to the generic cell
    'DPtable_num_opt_to': 'matrix_of_list_of_int',
    # the DP table meant to tell the number of optimal paths from the generic cell to the bottom-right cell
    'DPtable_num_opt_from': 'matrix_of_list_of_int',
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
_Path = List[_Cell]
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


def parse_raw_cell(cell: tuple[int, str]) -> _Cell:
    """Parse a cell from the raw textual representation."""
    # the format specification is [row, col]
    row, col = cell
    row, col = int(row) - 1, ord(col.lower()) - ord("a")
    return (row, col)


def parse_raw_path(cells: List[tuple[int, str]]) -> _Path:
    """Parse a path from the raw textual representation."""
    return [parse_raw_cell(x) for x in cells]


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


def check_instance_consistency(instance: Dict):
    grid = instance['grid']
    rows, cols = shape(grid)
    # TODO: ask whether this check is necessary for the type 'matrix_of_int'
    if not check_matrix_shape(grid):
        print(f"Error: {grid} must be a matrix")
        exit(0)

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if (c := grid[row][col]) < -1:
                print(f"Error: value {c} in {(row, col)} is not allowed")
                exit(0)

    if grid[0][0] == -1 or grid[-1][-1] == -1:
        print(f"Error")
        exit(0)

    # TODO: validate cells coordinates
    for argname in ["cell_from", "cell_to", "cell_through"]:
        cell = parse_raw_cell(instance[argname])
        if cell[0] > rows or cell[1] > cols:
            print(f"Invalid {argname} {cell}")
            exit(0)


def cell_gain(content_inside_cell: int) -> int:
    """The solution gain of a cell."""
    # only cells with positive content have a value
    return max(content_inside_cell, 0)


def cell_cost(content_inside_cell: int) -> int:
    """The solution cost on the budget of a cell."""
    # only cells with negative content have a cost
    return max(-content_inside_cell, 0)


def path_gain(grid: _Mat, path: _Path):
    """Total gain of a path over a specific grid."""
    assert grid is not None
    assert path is not None
    return sum(map(lambda x: cell_gain(grid[x[0]][x[1]]), path))


def path_cost(grid: _Mat, path: _Path):
    """Total cost of a path over a specific grid."""
    assert grid is not None
    assert path is not None
    return sum(map(lambda x: cell_cost(grid[x[0]][x[1]]), path))


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
        if cell_cost(grid[row0][col0]) <= b:
            mat[b][row0][col0] = 1

    # NOTE: start iteration from the reference cell
    for b in range(budget + 1):  # iterate on all possible values of budget
        for x in range(row0, rows):
            for y in range(col0, cols):
                cost_at_prev_cell = b - cell_cost(grid[x][y])
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
        if cell_cost(grid[row0][col0]) <= b:
            mat[b][row0][col0] = cell_gain(grid[row0][col0])

    # NOTE: start iteration from the reference cell
    for b in range(budget + 1):  # iterate on all possible values of budget
        for x in range(row0, rows):
            for y in range(col0, cols):
                prev_cost = b - cell_cost(grid[x][y])
                if prev_cost >= 0:
                    v = cell_gain(grid[x][y])
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
        if cell_cost(grid[row0][col0]) <= b:
            mat[b][row0][col0] = 1

    # NOTE: start iteration from the reference cell
    for x in range(cell[0], rows):
        for y in range(cell[1], cols):
            for b in range(budget + 1):
                # the budget left at a previous cell required to move in the current cell
                # with the current total budget
                bud = b - cell_cost(grid[x][y])

                # the optimal value of a path that gets at the current
                opt = dptable[bud][x][y] - cell_gain(grid[x][y])

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


def yield_opt_paths_beg_to_mid(p: Instance, opt_beg2any: np.ndarray, cost: int):
    assert cost >= 0

    def build(path: List[_Cell], c: int):
        x, y = path[-1]

        # check if we have reached the end
        if (x, y) == p.beg:
            # NOTE: the build process is reversed, so flip the path order
            path.reverse()
            yield path

        # the value of any optimal path that reaches this cell
        opt = opt_beg2any[c][x][y] - cell_gain(p.grid[x][y])
        # remove the cost of the current cell
        c1 = c - cell_cost(p.grid[x][y])
        assert c1 >= 0, "Underflowed minimum cost"

        # if the result path is optimal, keep building from the cell in the previuos row
        if x > p.beg[0]:
            if opt_beg2any[c1][x - 1][y] == opt:
                yield from build(path + [(x - 1, y)], c1)

        # if the result path is optimal, keep building from the cell in the previuos column
        if y > p.beg[1]:
            if opt_beg2any[c1][x][y - 1] == opt:
                yield from build(path + [(x, y - 1)], c1)

        # if the result path is optimal, keep building from the cell in the previuos diagonal
        if p.diag and x > p.beg[0] and y > p.beg[1]:
            if opt_beg2any[c1][x - 1][y - 1] == opt:
                yield from build(path + [(x - 1, y - 1)], c1)

    # NOTE: for this case the build process is reversed,
    # starting from the <mid> cell and moving towards the <beg> cell
    yield from build([p.mid], cost)


def yield_opt_paths_mid_to_end(p: Instance, opt_any2end: np.ndarray, cost: int):
    assert cost >= 0

    def build(path: List[_Cell], c: int):
        x, y = path[-1]

        # check if we have reached the end
        if (x, y) == p.end:
            yield path

        # remove the cost of the current cell
        opt = opt_any2end[c][x][y] - cell_gain(p.grid[x][y])
        c1 = c + cell_cost(p.grid[x][y])
        assert c1 <= cost, "Overflowed maximum cost"

        # if the result path is optimal, keep building from the cell in the previuos row
        if x < p.end[0]:
            if opt_any2end[c1][x + 1][y] == opt:
                yield from build(path + [(x + 1, y)], c1)

        # if the result path is optimal, keep building from the cell in the previuos column
        if y < p.end[1]:
            if opt_any2end[c1][x][y + 1] == opt:
                yield from build(path + [(x, y + 1)], c1)

        # if the result path is optimal, keep building from the cell in the previuos diagonal
        if p.diag and x < p.end[0] and y < p.end[1]:
            if opt_any2end[c1][x + 1][y + 1] == opt:
                yield from build(path + [(x + 1, y + 1)], c1)

    yield from build([p.mid], cost)


def yield_opt_paths(p: Instance, opt_beg2any: np.ndarray, opt_any2end: np.ndarray):
    assert opt_beg2any.shape == opt_any2end.shape

    # list all cost combinations for the subpaths with associated complete path value
    midx, midy = p.mid
    solutions = []
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
        beg2mid = yield_opt_paths_beg_to_mid(
            p, opt_beg2any=opt_beg2any, cost=c0)
        mid2end = yield_opt_paths_mid_to_end(
            p, opt_any2end=opt_any2end, cost=c1)
        # merge all possible subpaths combinations
        for p0, p1 in itertools.product(beg2mid, mid2end):
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

    solutions = []
    for b0, b1 in zip(range(budget), reversed(range(budget))):
        num_A_to_B = num_beg2any[b0][x][y]
        num_B_to_C = num_any2end[b1][x][y]
        solutions.append(num_A_to_B * num_B_to_C)

    # pick all the solutions
    return sum(solutions)


def query_opt(grid: np.ndarray, opt_beg2any: np.ndarray, opt_any2end: np.ndarray, through: _Cell):
    assert opt_beg2any.shape == opt_any2end.shape
    x, y = through
    budget = opt_beg2any.shape[0]  # dptable matrix is [budget][row][col]

    solutions = []
    for b0, b1 in zip(range(budget), reversed(range(budget))):
        opt_A_to_B = opt_beg2any[b0][x][y]
        opt_B_to_C = opt_any2end[b1][x][y]
        solutions.append(opt_A_to_B + opt_B_to_C)

    # pick the best solution
    # NOTE: all solutions include the gain of the <through> cell two times,
    # we need to remove it once
    return max(solutions) - cell_gain(grid[x][y])


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

    solutions = []
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

    instance: Final[Dict] = input_to_oracle["input_data_assigned"]

    # extract and parse inputs
    grid: Final = np.array(instance["grid"])
    diag: Final = instance["diag"]
    budget: Final = instance["budget"]
    beg: Final = parse_raw_cell(instance["cell_from"])
    end: Final = parse_raw_cell(instance["cell_to"])
    mid: Final = parse_raw_cell(instance["cell_through"])
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
    opt_val = query_opt(grid, DPtable_opt_to, DPtable_opt_from, mid)
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

        if 'num_paths' in self.goals:
            g = self.goals['num_paths']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"Come `{g.alias}` hai immesso un intero come richiesto",
                          f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")
            
        if 'num_opt_paths' in self.goals:
            g = self.goals['num_opt_paths']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"Come `{g.alias}` hai immesso un intero come richiesto",
                          f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")
            
        if 'opt_val' in self.goals:
            g = self.goals['opt_val']
            if type(g.answ) != int:
                return SEF.format_NO(g, f"Come `{g.alias}` hai immesso `{g.answ}` dove era invece richiesto di immettere un intero.")
            SEF.format_OK(g, f"Come `{g.alias}` hai immesso un intero come richiesto",
                          f"ovviamente durante lo svolgimento dell'esame non posso dirti se l'intero immesso sia poi la risposta corretta, ma il formato è corretto")
            
        if 'opt_path' in self.goals:
            g = self.goals['opt_path']
            # Controllo se si tratta di una lista
            if type(g.answ) != list:
                return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una lista di celle (esempio [['1', 'A'], ...]). Hai invece immesso `{g.answ}`.")

            # Controllo se gli elemnti della lista sono celle
            for ele in g.answ:
                if type(ele) != list or len(ele) != 2 or type(ele[0]) != str or type(ele[1]) != str:
                    return SEF.format_NO(g, f"Ogni oggetto che collochi nella lista `{g.alias}` deve essere una cella. L'elemento `{ele}` da te inserito non è un cella.")
                if not str.isdigit(ele[0]) or not str.isalpha(ele[1]) or len(ele[1]) > 1:
                    return SEF.format_NO(g, f"Ogni cella in `{g.alias}` deve avere coordinate valide (esempio ['1', 'A']). L'elemento `{ele}` da te inserito non è una cella valida.")

            SEF.format_OK(g, f"Come `{g.alias}` hai immesso una lista di celle",
                          f"resta da stabilire l'ammissibilità di `{g.alias}`")
            
        if 'list_opt_paths' in self.goals:
            g = self.goals['list_opt_paths']
            # Controllo se si tratta di una lista di liste
            if type(g.answ) != list:
                return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una lista di liste di celle (esempio [[['1', 'A'], ...], ['1', 'A'], ...]]). Hai invece immesso `{g.answ}`.")

            # Controllo se le liste sono liste di celle
            for obj in g.answ:
                if type(obj) != list:
                    return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una lista di liste di celle (esempio [[['1', 'A'], ...], ['1', 'A'], ...]]). Hai invece immesso `{g.answ}`.")

            # Controllo se gli elemnti della lista sono tutte celle
            for obj in g.answ:
                for ele in obj:
                    if type(ele) != list or len(ele) != 2 or type(ele[0]) != str or type(ele[1]) != str:
                        return SEF.format_NO(g, f"Ogni oggetto che collochi nella lista di liste `{g.alias}` deve essere una cella. L'elemento `{ele}` da te inserito non è una cella.")
                    if not str.isdigit(ele[0]) or not str.isalpha(ele[1]) or len(ele[1]) > 1:
                        return SEF.format_NO(g, f"Ogni cella in `{g.alias}` deve avere coordinate valide (esempio ['1', 'A']). L'elemento `{ele}` da te inserito non è una cella valida.")
                        
            SEF.format_OK(g, f"Come `{g.alias}` hai immesso una lista di liste di celle",
                          f"resta da stabilire l'ammissibilità di `{g.alias}`")

        dptable_goal_names = [f"DPtable_{x}" for x in
                              ['num_to', 'num_from', 'opt_to', 'opt_from', 'num_opt_to', 'num_opt_from']]
        for name in dptable_goal_names:
            if name in self.goals:
                g = self.goals[name]
                # Controllo se si tratta di una lista di liste
                if type(g.answ) != list:
                    return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una matrice tridimensionale di interi (esempio [[[0, ...]], [[1, ...]]]). Hai invece immesso `{g.answ}`.")

                # Controllo se le liste sono liste di interi
                for obj in g.answ:
                    if type(obj) != list:
                        return SEF.format_NO(g, f"Come `{g.alias}` è richiesto si inserisca una matrice tridimensionale di interi (esempio [[0, 0], ...,]]). Hai invece immesso `{g.answ}`.")

                # Controllo se gli elemnti della lista sono tutti interi
                for obj in g.answ:
                    for ele in obj:
                        for val in ele:
                            if type(val) != int:
                                return SEF.format_NO(g, f"Ogni oggetto che collochi nella lista di liste `{g.alias}` deve essere un intero. L'elemento `{ele}` da te inserito non è un itero.")
                SEF.format_OK(g, f"Come `{g.alias}` hai immesso una matrice tridimensionale",
                              f"resta da stabilire l'ammissibilità di `{g.alias}`")

        return True

    def set_up_and_cash_handy_data(self):
        self.beg = parse_raw_cell(self.I.cell_from)
        self.mid = parse_raw_cell(self.I.cell_through)
        self.end = parse_raw_cell(self.I.cell_to)

        rows, cols = shape(self.I.grid)
        self.expected_dp_shape = (self.I.budget, rows, cols)

    def verify_feasibility(self, SEF: std_eval_feedback):
        if not super().verify_feasibility(SEF):
            return False

        if 'opt_path' in self.goals:
            g = self.goals['opt_path']
            print("opt_path answ:", g.answ)
            path = parse_raw_path(g.answ)
            if path[0] != self.beg:
                reason = f"Il percorso non comincia dalla cella {self.beg}."
                return SEF.feasibility_NO(g, reason)

            if path[-1] != self.end:
                reason = f"Il percorso non termina alla cella {self.end}."
                return SEF.feasibility_NO(g, reason)

            if self.mid not in path:
                reason = f"Il percorso non passa dalla cella {self.mid}."
                return SEF.feasibility_NO(g, reason)

            if not check_path_feasible(path, diag=self.I.diag):
                reason = f"Il percorso {path} usa movimenti non validi."
                return SEF.feasibility_NO(g, reason)

            if path_cost(self.I.grid, path) > self.I.budget:
                reason = f"Il costo del percorso {path} supera il budget."
                return SEF.feasibility_NO(g, reason)

        if 'list_opt_paths' in self.goals:
            g = self.goals['list_opt_paths']
            paths = [parse_raw_path(x) for x in g.answ]
            for path in paths:
                if path[0] != self.beg:
                    reason = f"Il percorso non comincia dalla cella {self.beg}."
                    return SEF.feasibility_NO(g, reason)

                if path[-1] != self.end:
                    reason = f"Il percorso non termina alla cella {self.end}."
                    return SEF.feasibility_NO(g, reason)

                if self.mid not in path:
                    reason = f"Il percorso non passa dalla cella {self.mid}."
                    return SEF.feasibility_NO(g, reason)

                if not check_path_feasible(path, diag=self.I.diag):
                    reason = f"Il percorso {path} usa movimenti non validi."
                    return SEF.feasibility_NO(g, reason)

                if path_cost(self.I.grid, path) > self.I.budget:
                    reason = f"Il costo del percorso {path} supera il budget."
                    return SEF.feasibility_NO(g, reason)

        return True

    def verify_consistency(self, SEF: std_eval_feedback):
        if not super().verify_consistency(SEF):
            return False

        if 'num_paths' in self.goals and 'num_opt_paths' in self.goals:
            g_all = self.goals['num_paths']
            g_opt = self.goals['num_opt_paths']
            if g_opt.answ > g_all.answ:
                reason = f"La soluzione in `{g_opt.alias}` non può essere maggiore di `{g_all.alias}`."
                return SEF.consistency_NO(['num_paths', 'num_opt_paths'], reason)

        if 'opt_val' in self.goals and 'opt_path' in self.goals:
            g_val = self.goals['opt_val']
            g_sol = self.goals['opt_path']
            opt_path = parse_raw_path(g_sol.answ)
            if (gain := path_gain(self.I.grid, opt_path)) != g_val.answ:
                reason = f"Il valore totale della soluzione immessa in `{g_sol.alias}` è {gain}, non {g_val.answ} come hai invece immesso in `{g_val.alias}`. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}."
                return SEF.consistency_NO(['opt_val', 'opt_path'], reason)

        if 'opt_val' in self.goals and 'list_opt_paths' in self.goals:
            g_val = self.goals['opt_val']
            g_sol = self.goals['list_opt_paths']
            list_opt_paths = [parse_raw_path(p) for p in g_sol.answ]
            for p in list_opt_paths:
                if (gain := path_gain(self.I.grid, p)) != g_val.answ:
                    reason = f"Il valore totale della soluzione immessa in `{g_sol.alias}` è {gain}, non {g_val.answ} come hai invece immesso in `{g_val.alias}`. La soluzione (ammissibile) che hai immesso è `{g_sol.alias}`={g_sol.answ}."
                    return SEF.consistency_NO(['opt_val', 'list_opt_paths'], reason)

        return True
