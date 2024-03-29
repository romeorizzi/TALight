import unittest

import numpy.testing as npt
from robot_lib import *


class InputParsingTest(unittest.TestCase):
    def test_raw_cell_parsing(self):
        testcases = [
            (["10", "a"], (9, 0)),
            (["99", "A"], (98, 0)),
            (["11", "z"], (10, 25)),
        ]
        for i, (text, cell) in enumerate(testcases):
            with self.subTest(i=i, text=text, cell=cell):
                self.assertEqual(cell, parse_raw_cell(text))

    def test_raw_path_parsing(self):
        testcases = [
            ([["1", "a"], ["1", "b"], ["2", "b"]], [(0, 0), (0, 1), (1, 1)]),
            ([["1", "a"], ["2", "a"], ["2", "b"]], [(0, 0), (1, 0), (1, 1)]),
        ]
        for i, (text, path) in enumerate(testcases):
            with self.subTest(i=i, text=text, path=path):
                self.assertListEqual(path, parse_raw_path(text))


class UilityFunctions(unittest.TestCase):
    def test_cell_value_function(self):
        matches = [
            (0, 0),
            (+10, 10),
            (+100, 100),
            (-10, 0),
            (-100, 0),
        ]
        for i, (content, expected_gain) in enumerate(matches):
            with self.subTest(i=i):
                self.assertEqual(expected_gain, cell_gain(content))

    def test_cell_cost_function(self):
        matches = [
            (0, 0),
            (+10, 0),
            (+100, 0),
            (-10, 10),
            (-100, 100),
        ]
        for i, (content, expected_cost) in enumerate(matches):
            with self.subTest(i=i):
                self.assertEqual(expected_cost, cell_cost(content))


class DPTableGeneratorsTest(unittest.TestCase):

    def test_num_to_cell(self):
        grid = [[0, -1, 2],
                [0, +1, 0],
                [2, -1, 0]]
        grid = np.array(grid)

        expect = [[[1, 0, 0],
                   [1, 1, 1],
                   [1, 0, 1]]]
        actual = dp_num_to(grid, cell=(0, 0), budget=0, diag=False)
        npt.assert_array_equal(actual, expect)

        expect = [[[1, 0, 0],
                   [1, 2, 2],
                   [1, 0, 4]]]
        actual = dp_num_to(grid, cell=(0, 0), budget=0, diag=True)
        npt.assert_array_equal(actual, expect)

    def test_num_from_cell(self):
        grid = [[0, -1, 2],
                [0, +1, 0],
                [2, -1, 0]]
        grid = np.array(grid)

        expect = [[[1, 0, 1],
                   [1, 1, 1],
                   [0, 0, 1]]]
        actual = dp_num_from(grid, cell=(2, 2), budget=0, diag=False)
        npt.assert_array_equal(actual, expect)

        expect = [[[4, 0, 1],
                   [2, 2, 1],
                   [0, 0, 1]]]
        actual = dp_num_from(grid, cell=(2, 2), budget=0, diag=True)
        npt.assert_array_equal(actual, expect)

    def test_opt_to_cell(self):
        grid = [[0, -1, 2],
                [0, +1, 0],
                [2, -1, 0]]
        grid = np.array(grid)

        expect = [[[0, -1, -1],
                   [0,  1,  1],
                   [2, -1,  1]]]
        actual = dp_opt_to(grid, cell=(0, 0), budget=0, diag=False)
        npt.assert_array_equal(actual, expect)

        expect = [[[0, -1, -1],
                   [0,  1,  1],
                   [2, -1,  1]]]
        actual = dp_opt_to(grid, cell=(0, 0), budget=0, diag=True)
        npt.assert_array_equal(actual, expect)

    def test_opt_from_cell(self):
        grid = [[0, -1, 2],
                [0, +1, 0],
                [2, -1, 0]]
        grid = np.array(grid)

        expect = [[[1,  -1, 2],
                   [1,   1, 0],
                   [-1, -1, 0]]]
        actual = dp_opt_from(grid, cell=(2, 2), budget=0, diag=False)
        npt.assert_array_equal(actual, expect)

        expect = [[[1, -1, 2],
                   [1,  1, 0],
                   [-1, -1, 0]]]
        actual = dp_opt_from(grid, cell=(2, 2), budget=0, diag=True)
        npt.assert_array_equal(actual, expect)

    def test_num_opt_to_cell(self):
        grid = [[0, -1, 2],
                [0, +1, 0],
                [2, -1, 0]]
        grid = np.array(grid)
        COST = 0
        CELL = (0, 0)  # top-left cell

        expect = [[[1, 0, 0],
                   [1, 1, 1],
                   [1, 0, 1]]]
        dptable = dp_opt_to(grid, cell=CELL, budget=COST, diag=False)
        actual = dp_num_opt_to(
            grid, cell=CELL, dptable=dptable, budget=COST, diag=False)
        npt.assert_array_equal(actual, expect)

        expect = [[[1, 0, 0],
                   [1, 2, 2],
                   [1, 0, 4]]]
        dptable = dp_opt_to(grid, cell=CELL, budget=COST, diag=True)
        actual = dp_num_opt_to(
            grid, cell=CELL, dptable=dptable, budget=COST, diag=True)
        npt.assert_array_equal(actual, expect)

    def test_num_opt_from_cell(self):
        grid = [[0, -1, 2],
                [0, +1, 0],
                [2, -1, 0]]
        grid = np.array(grid)
        COST = 0
        CELL = (grid.shape[0] - 1, grid.shape[1] - 1)  # bottom-right cell

        expect = [[[1, 0, 1],
                   [1, 1, 1],
                   [0, 0, 1]]]
        dptable = dp_opt_from(grid, cell=CELL, budget=COST, diag=False)
        actual = dp_num_opt_from(
            grid, cell=CELL, dptable=dptable, budget=COST, diag=False)
        npt.assert_array_equal(actual, expect)

        expect = [[[4, 0, 1],
                   [2, 2, 1],
                   [0, 0, 1]]]
        dptable = dp_opt_from(grid, cell=CELL, budget=COST, diag=True)
        actual = dp_num_opt_from(
            grid, cell=CELL, dptable=dptable, budget=COST, diag=True)
        npt.assert_array_equal(actual, expect)


class DPTableQueryTest(unittest.TestCase):
    
    def test_query_opt(self):
        grid = [[0, 1, 0, 3, 0], [-1, 2,-1,-1, 0], [0, 0, 2, 1, 0], [0,-1, 0, 1, 1] ]
        grid = np.array(grid)
        beg2any = dp_opt_to(grid, (0,0), budget=0, diag=False)
        any2end = dp_opt_from(grid, (3,4), budget=0, diag=False)
        opt = query_opt(grid, opt_beg2any=beg2any, opt_any2end=any2end, through=(2,2))
        self.assertEqual(opt, 8)


class PathGeneratorsTest(unittest.TestCase):

    def test_yield_opt_paths_beg2mid(self):
        testcases = [
            {
                "instance": Instance(
                    grid=np.array([[1, 1, 1],
                                   [1, 0, 1],
                                   [1, 1, 1]]),
                    cost=0, diag=False,
                    beg=(0, 0), mid=(1, 1), end=(2, 2),
                ),
                "solution": [
                    [(0, 0), (0, 1), (1, 1)],
                    [(0, 0), (1, 0), (1, 1)],
                ]
            },
            {
                "instance": Instance(
                    grid=np.array([[1, 1, -1],
                                   [1, 0,  1],
                                   [-1, 1,  1]]),
                    cost=0, diag=False,
                    beg=(0, 0), mid=(1, 1), end=(2, 2),
                ),
                "solution": [
                    [(0, 0), (0, 1), (1, 1)],
                    [(0, 0), (1, 0), (1, 1)],
                ]
            },
        ]
        for i, testcase in enumerate(testcases):
            instance = testcase["instance"]
            beg2any = dp_opt_to(
                instance.grid, cell=instance.beg, budget=instance.cost, diag=instance.diag)
            with self.subTest(i=i, instance=instance, beg2any=beg2any):
                paths = list(yield_opt_paths_beg_to_mid(
                    instance, opt_beg2any=beg2any, cost=0))
                self.assertEqual(sorted(testcase["solution"]), sorted(paths))

    def test_yield_opt_paths_mid2end(self):
        testcases = [
            {
                "instance": Instance(
                    grid=np.array([[1, 1, -1],
                                   [1, 0,  1],
                                   [-1, 1,  1]]),
                    cost=0, diag=False,
                    beg=(0, 0), mid=(1, 1), end=(2, 2),
                ),
                "solution": [
                    [(1, 1), (1, 2), (2, 2)],
                    [(1, 1), (2, 1), (2, 2)],
                ]
            },
        ]
        for i, testcase in enumerate(testcases):
            instance = testcase["instance"]
            any2end = dp_opt_from(instance.grid, cell=instance.end,
                                  budget=instance.cost, diag=instance.diag)
            with self.subTest(i=i, instance=instance, any2end=any2end):
                paths = list(yield_opt_paths_mid_to_end(
                    instance, opt_any2end=any2end, cost=0))
                self.assertEqual(sorted(testcase["solution"]), sorted(paths))

    def test_yield_opt_paths(self):
        testcases = [
            {
                "instance": Instance(
                    grid=np.array([[1, 1, 1],
                                   [1, 0, 1],
                                   [1, 1, 1]]),
                    cost=0, diag=False,
                    beg=(0, 0), mid=(0, 0), end=(2, 2),
                ),
                "solution": [
                    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
                    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
                ]
            },
            {
                "instance": Instance(
                    grid=np.array([[1, 1, 1],
                                   [1, 0, 1],
                                   [1, 1, 1]]),
                    cost=0, diag=False,
                    beg=(0, 0), mid=(0, 0), end=(2, 2),
                ),
                "solution": [
                    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
                    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
                ]
            },
            {
                "instance": Instance(
                    grid=np.array([[1, 1, -1],
                                   [1, 0,  1],
                                   [-1, 1,  1]]),
                    cost=0, diag=False,
                    beg=(0, 0), mid=(1, 1), end=(2, 2),
                ),
                "solution": [
                    [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
                    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
                    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],
                    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
                ]
            },
            {
                "instance": Instance(
                    grid=np.array([[1,  1, -1],
                                   [1, -1,  1],
                                   [-1, 1,  1]]),
                    cost=0, diag=True,
                    beg=(0, 0), mid=(0, 0), end=(2, 2),
                ),
                "solution": [
                    [(0, 0), (0, 1), (1, 2), (2, 2)],
                    [(0, 0), (1, 0), (2, 1), (2, 2)],
                ]
            },
        ]

        for testcase in testcases:
            i = testcase["instance"]
            beg2any = dp_opt_to(i.grid, cell=i.beg,
                                budget=i.cost, diag=i.diag)
            any2end = dp_opt_from(i.grid, cell=i.end,
                                  budget=i.cost, diag=i.diag)
            with self.subTest(instance=i, beg2any=beg2any, any2end=any2end):
                paths = list(yield_opt_paths(
                    i, opt_beg2any=beg2any, opt_any2end=any2end))
                self.assertEqual(sorted(testcase["solution"]), sorted(paths))


if __name__ == "__main__":
    unittest.main()
