import unittest

from robot_lib import *


class TestInputParsing(unittest.TestCase):

    def test_cell_parsing(self):
        cells = [
            ("(a,10)", (0, 10)),
            ("(A,99)", (0, 99)),
        ]
        for i, (cell, expect) in enumerate(cells):
            with self.subTest(i=i):
                self.assertEqual(expect, parse_cell(cell))


class TestDPTableGenerators(unittest.TestCase):

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
        self.assertEqual(exclude, dptable_num_to_cell(field, diag=False))
        self.assertEqual(include, dptable_num_to_cell(field, diag=True))

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
        self.assertEqual(exclude, dptable_num_from_cell(field, diag=False))
        self.assertEqual(include, dptable_num_from_cell(field, diag=True))

    def test_opt_to_cell(self):
        field = [[0,  0, -1,  0, 0],
                 [0,  2,  0,  4, 0],
                 [3,  0,  0, -1, 0],
                 [0, -1,  5,  0, 0]]
        exclude = [[0,  0,  0,  0,  0],
                   [0,  2,  2,  6,  6],
                   [3,  3,  3,  0,  6],
                   [3,  0,  8,  8,  8]]
        include = [[0,  0,  0,  0,  0],
                   [0,  2,  2,  6,  6],
                   [3,  3,  3,  0,  6],
                   [3,  0,  8,  8,  8]]
        self.assertEqual(exclude, dptable_opt_to_cell(field, diag=False))
        self.assertEqual(include, dptable_opt_to_cell(field, diag=True))


if __name__ == "__main__":
    unittest.main()
