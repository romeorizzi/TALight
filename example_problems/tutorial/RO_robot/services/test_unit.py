import unittest

from robot_lib import *


class InputParsing(unittest.TestCase):
    @unittest.skip("Not yet finalized, may not be required")
    def test_cell_parsing(self):
        cells = [
            ("(a,10)", (0, 10)),
            ("(A,99)", (0, 99)),
            ("(z,11)", (25, 11)),
        ]
        for i, (cell, expect) in enumerate(cells):
            with self.subTest(i=i):
                self.assertEqual(expect, parse_cell(cell))


class DPTableGenerators(unittest.TestCase):

    def test_cost_table_building(self):
        grids = [
                [[1, 2, 3, 4]],
                [[-1, 1], [1, -1]],
                [[100, -100], [0, -10000], [1000, 10000]],
        ]
        for g in grids:
            with self.subTest(g=g):
                costs = build_cost_table(g)
                rows, cols = shape(costs)
                for row in range(rows):
                    for col in range(cols):
                        if g[row][col] >= 0:
                            self.assertEqual(costs[row][col], 0)
                        else:
                            self.assertEqual(costs[row][col], -g[row][col])

    def test_num_to_cell(self):
        field = [[0,  0, -1,  0, 0],
                 [0,  0,  0,  0, 0],
                 [0,  0,  0, -1, 0],
                 [0, -1,  0,  0, 0]]
        exclude = [[1,  1,  0,  0,  0],
                   [1,  2,  2,  2,  2],
                   [1,  3,  5,  0,  2],
                   [1,  0,  5,  5,  7]]
        include = [[1,  1,   0,   0,   0],
                   [1,  3,   4,   4,   4],
                   [1,  5,  12,   0,   8],
                   [1,  0,  17,  29,  37]]
        self.assertEqual(exclude, dptable_num_to(field, diag=False))
        self.assertEqual(include, dptable_num_to(field, diag=True))

    def test_num_from_cell(self):
        field = [[0,  0, -1,  0, 0],
                 [0,  0,  0,  0, 0],
                 [0,  0,  0, -1, 0],
                 [0, -1,  0,  0, 0]]
        exclude = [[7, 3, 0, 2, 1],
                   [4, 3, 2, 1, 1],
                   [1, 1, 1, 0, 1],
                   [0, 0, 1, 1, 1]]
        include = [[37, 13, 0, 4, 1],
                   [15,  9, 4, 2, 1],
                   [3,  3, 2, 0, 1],
                   [0,  0, 1, 1, 1]]
        self.assertEqual(exclude, dptable_num_from(field, diag=False))
        self.assertEqual(include, dptable_num_from(field, diag=True))

    def test_opt_to_cell(self):
        budget = 1
        field = [[0, -1, +2],
                 [0, +1, 0],
                 [+2, -1, 0]]
        exclude = [[[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]],
                   [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]]
        include = [[0,  0,  0,  0,  0],
                   [0,  2,  2,  6,  6],
                   [3,  3,  3,  0,  6],
                   [3,  0,  8,  8,  8]]
        self.assertEqual(exclude, dptable_opt_to(field, diag=False))
        self.assertEqual(include, dptable_opt_to(field, diag=True))

    def test_opt_from_cell(self):
        # TODO: change the example because diagonal moves produce the same result
        field = [[0,  0, -1,  0, 0],
                 [0,  2,  0,  4, 0],
                 [3,  0,  0, -1, 0],
                 [0, -1,  5,  0, 0]]
        exclude = [[8, 7, 0, 4, 0],
                   [8, 7, 5, 4, 0],
                   [8, 5, 5, 0, 0],
                   [0, 0, 5, 0, 0]]
        include = [[8, 7, 0, 4, 0],
                   [8, 7, 5, 4, 0],
                   [8, 5, 5, 0, 0],
                   [0, 0, 5, 0, 0]]
        self.assertEqual(exclude, dptable_opt_from(field, diag=False))
        self.assertEqual(include, dptable_opt_from(field, diag=True))

    def test_num_opt_to_cell(self):
        field = [[0,  3, -1,  0],
                 [0,  0,  0,  4],
                 [2, -1,  0,  0]]
        exclude = [[(1, 0), (1, 3), (0, 0), (0, 0)],
                   [(1, 0), (1, 3), (1, 3), (1, 7)],
                   [(1, 2), (0, 0), (1, 3), (1, 7)]]
        include = [[(1, 0), (1, 3), (0, 0), (0, 0)],
                   [(1, 0), (1, 3), (2, 3), (2, 7)],
                   [(1, 2), (0, 0), (3, 3), (2, 7)]]
        self.assertEqual(exclude, dptable_num_opt_to(field, diag=False))
        self.assertEqual(include, dptable_num_opt_to(field, diag=True))

    def test_num_opt_from_cell(self):
        field = [[0,  3, -1,  0],
                 [0,  0,  0,  4],
                 [2, -1,  0,  0]]
        exclude = [[(1, 7), (1, 7), (0, 0), (1, 4)],
                   [(1, 4), (1, 4), (1, 4), (1, 4)],
                   [(0, 2), (0, 0), (1, 0), (1, 0)]]
        include = [[(2, 7), (2, 7), (0, 0), (1, 4)],
                   [(1, 4), (1, 4), (1, 4), (1, 4)],
                   [(0, 2), (0, 0), (1, 0), (1, 0)]]
        self.assertEqual(exclude, dptable_num_opt_from(field, diag=False))
        self.assertEqual(include, dptable_num_opt_from(field, diag=True))

    def test_num_to_with_budget(self):
        testcases = [
            ([[1, 2, 3, 4]], [[[1, 1, 1, 1]]]),
            ([[1, 2, -1, 4]], [[[1, 1, 1, 0]]]),
        ]
        for grid, expect in testcases:
            with self.subTest(grid=grid, expect=expect):
                actual = dptable_num_to_with_budget(grid, budget=1, diag=False)
                self.assertEqual(expect, actual)


class PathGenerators(unittest.TestCase):

    @unittest.skip("Not yet finalized, may not be required")
    def test_single_opt_path(self):
        field = [[1, 1, 1, 0, 1],
                 [0, 0, 1, 1, 1],
                 [1, 0, 0, 0, 1],
                 [1, 1, 1, 0, 1]]
        path = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4)]
        table = dptable_opt_from(field, diag=False)
        self.assertEqual(path, build_opt_path(table, diag=False))

    def test_list_all_opt_paths(self):
        field = [[1, 1, 1, 0, 1],
                 [1, 0, 1, 1, 1],
                 [1, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1]]
        expect = [[(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4)],
                  [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4)]]
        table = dptable_opt_from(field, diag=False)
        actual = build_all_opt_path(field, table, diag=False)
        self.assertEqual(sorted(expect), sorted(actual))

        expect = [[(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4)],
                  [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4)]]
        table = dptable_opt_from(field, diag=True)
        actual = build_all_opt_path(field, table, diag=True)
        self.assertEqual(sorted(expect), sorted(actual))


if __name__ == "__main__":
    unittest.main()
