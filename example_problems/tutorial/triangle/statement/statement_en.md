# PROBLEM

The figure below shows a triangle. Write a program that calculates the biggest sum of numbers you can get from a path which goes from the top to somewhere in the base of the triangle.


                                                            7
                                                          3   8
                                                        8   1   0
                                                      2   7   4   4
                                                    4   5   2   6   5


1) At each step you can proceed towards bottom-left or bottom-right.
2) The number of rows of the triangle shall be comprised between 1 and 100 (1 <= n <= 100).
3) The values of the triangle shall be comprised between 0 and 99 (0 <= v <= 99).

# INPUT DATA

The data is contained in the ***INPUT.TXT*** file. The value on the first line represents the triangle's number of rows, while the remaining lines represent its rows. In our example, ***INPUT.TXT*** is as follows: 

```
5
7
3 8
8 1 0
2 7 4 4
4 5 2 6 5
```
# OUTPUT DATA

The maximum sum is an integer written in the ***OUTPUT.TXT*** file. In our example the result is: 

```
30
```
