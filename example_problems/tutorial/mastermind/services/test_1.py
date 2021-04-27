import unittest
from engine import check

class Test_test_1(unittest.TestCase): 

    def test_A(self):
        pos, col = check("A B C D", "A B C D")
        assert pos == 4
        assert col == 0

    def test_B(self):
        pos, col = check("B C D A", "A B C D")
        assert pos == 0
        assert col == 4  
      
    def test_C(self):
        pos, col = check("A B C D", "A B B B")
        assert pos == 2
        assert col == 0

    def test_D(self):
        pos, col = check("A B C D", "D D D D")
        assert pos == 1
        assert col == 0

    def test_E(self):
        pos, col = check("B C B B", "C A A A")
        assert pos == 0
        assert col == 1

    def test_F(self):
        pos, col = check("B C B B", "A A C C")
        assert pos == 0
        assert col == 1

    def test_G(self):
        pos, col = check("D D D D", "A A A A")
        assert pos == 0
        assert col == 0

    def test_H(self):
        pos, col = check("A B B C", "A D D B")
        assert pos == 1
        assert col == 1

if __name__ == '__main__':
    unittest.main()
