#!/usr/bin/env python3
import sys

board = [['0' for _ in range(1024)] for _ in range(1024)]

def compute_tiling(first_row, last_row, first_col, last_col, hole_row, hole_col):
    tiling(first_row, last_row, first_col, last_col, hole_row, hole_col)
    return board    

def tiling(first_row, last_row, first_col, last_col, hole_row, hole_col):
    k = last_row - first_row + 1

    if k <= 1:        
        return

    half_k = int(k / 2)

    row_holes = [['0' for i in range(2)] for j in range(2)]
    col_holes = [['0' for i in range(2)] for j in range(2)]
    row_holes[0][0] = first_row + half_k - 1
    col_holes[0][0] = first_col + half_k - 1
    row_holes[0][1] = first_row + half_k - 1
    col_holes[0][1] = first_col + half_k
    row_holes[1][0] = first_row + half_k
    col_holes[1][0] = first_col + half_k - 1
    row_holes[1][1] = first_row + half_k
    col_holes[1][1] = first_col + half_k

    if (hole_row < first_row + half_k and hole_col < first_col + half_k ):
        row_holes[0][0] = hole_row
        col_holes[0][0] = hole_col
        board[first_row + half_k - 1][first_col + half_k] = "N"
        board[first_row + half_k][first_col + half_k] = "4"
        board[first_row + half_k][first_col + half_k - 1] = "W"

    if (hole_row < first_row + half_k and hole_col >= first_col + half_k):
        row_holes[0][1] = hole_row
        col_holes[0][1] = hole_col        
        board[first_row + half_k - 1][first_col + half_k - 1] = "N"
        board[first_row + half_k][first_col + half_k - 1] = "1"
        board[first_row + half_k][first_col + half_k] = "E"

    if (hole_row >= first_row + half_k and hole_col < first_col + half_k ):
        row_holes[1][0] = hole_row
        col_holes[1][0] = hole_col        
        board[first_row + half_k - 1][first_col + half_k - 1] = "W"
        board[first_row + half_k - 1][first_col + half_k] = "3"
        board[first_row + half_k][first_col + half_k] = "S"

    if (hole_row >= first_row + half_k and hole_col >= first_col + half_k):
        row_holes[1][1] = hole_row
        col_holes[1][1] = hole_col        
        board[first_row + half_k - 1][first_col + half_k] = "E"
        board[first_row + half_k - 1][first_col + half_k - 1] = "2"
        board[first_row + half_k][first_col + half_k - 1] = "S"

    tiling(first_row, first_row + half_k - 1, first_col, first_col + half_k - 1, row_holes[0][0], col_holes[0][0])
    tiling(first_row, first_row + half_k - 1, first_col + half_k, last_col, row_holes[0][1], col_holes[0][1])
    tiling(first_row + half_k, last_row, first_col, first_col + half_k - 1, row_holes[1][0], col_holes[1][0])
    tiling(first_row + half_k, last_row, first_col + half_k, last_col, row_holes[1][1], col_holes[1][1])  
