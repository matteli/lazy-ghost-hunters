#!/usr/bin/env python3

import re

pieces = (
    (
        (19, (0, 1, 2, 4, 5, 6, 8, 9, 10), 18, (1, "A", "↱")),
        (35, (0, 1, 2, 4, 5, 6, 8, 9, 10), 33, (2, "A", "↰")),
        (50, (0, 1, 2, 4, 5, 6, 8, 9, 10), 18, (32, "A", "↲")),
        (49, (0, 1, 2, 4, 5, 6, 8, 9, 10), 33, (16, "A", "↳")),
    ),
    (
        (19, (0, 1, 2, 4, 5, 6, 8, 9, 10), 2, (1, "B", "→")),
        (35, (0, 1, 2, 4, 5, 6, 8, 9, 10), 32, (2, "B", "↓")),
        (50, (0, 1, 2, 4, 5, 6, 8, 9, 10), 16, (32, "B", "←")),
        (49, (0, 1, 2, 4, 5, 6, 8, 9, 10), 1, (16, "B", "↑")),
    ),
    (
        (19, (0, 1, 2, 4, 5, 6, 8, 9, 10), 16, (1, "B", "↓")),
        (35, (0, 1, 2, 4, 5, 6, 8, 9, 10), 1, (2, "B", "←")),
        (50, (0, 1, 2, 4, 5, 6, 8, 9, 10), 2, (32, "B", "↑")),
        (49, (0, 1, 2, 4, 5, 6, 8, 9, 10), 32, (16, "B", "→")),
    ),
    (
        (19, (0, 1, 2, 4, 5, 6, 8, 9, 10), 1, (16, "G", "↑")),
        (35, (0, 1, 2, 4, 5, 6, 8, 9, 10), 2, (1, "G", "→")),
        (50, (0, 1, 2, 4, 5, 6, 8, 9, 10), 32, (2, "G", "↓")),
        (49, (0, 1, 2, 4, 5, 6, 8, 9, 10), 16, (32, "G", "←")),
    ),
    (
        (3, (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14), 2, (1, "R", "→")),
        (17, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 16, (1, "R", "↓")),
        (3, (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14), 1, (2, "R", "←")),
        (17, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 1, (16, "R", "↑")),
    ),
    (
        (3, (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14), 0, (0, "", "")),
        (17, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), 0, (0, "", "")),
    ),
)
solution = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]


def print_torch(color, position):
    if color == "R":
        return f"\33[31m{position}\33[0m"
    if color == "B":
        return f"\33[34m{position}\33[0m"
    if color == "G":
        return f"\33[32m{position}\33[0m"
    if color == "A":
        return f"\33[90m{position}\33[0m"
    return ""


def print_solution(solution):
    for row in range(0, 4):
        line = ""
        for col in range(0, 4):
            pos_val = 2 ** (col + 4 * row)
            if pos_val & ghost_grid:
                line += "o"
            else:
                aprint = False
                for s in range(0, 5):
                    if solution[s][1] & pos_val:
                        line += print_torch(
                            pieces[s][solution[s][0]][3][1],
                            pieces[s][solution[s][0]][3][2],
                        )
                        aprint = True
                        break
                    if aprint:
                        break
                if not aprint:
                    line += "."
        print(line)


def test_piece(piece, rotation, position, grid, ghost, ghost_grid, solution):
    if grid == 65535 and ghost == ghost_grid:
        print("\n")
        print("Solution :")
        print_solution(solution)
        return
    rot = pieces[piece][rotation][0]
    pos = pieces[piece][rotation][1][position]
    gho = pieces[piece][rotation][2]
    tor = pieces[piece][rotation][3][0]
    val_grid = rot * 2**pos
    val_ghost = gho * 2**pos
    val_torch = tor * 2**pos
    if not (grid & val_grid) and not ((ghost_grid ^ val_ghost) & val_grid):
        solution[piece][0] = rotation
        solution[piece][1] = val_torch
        test_piece(
            piece + 1, 0, 0, grid + val_grid, ghost + val_ghost, ghost_grid, solution
        )
    if position + 1 < len(pieces[piece][rotation][1]):
        test_piece(piece, rotation, position + 1, grid, ghost, ghost_grid, solution)
    else:
        if rotation + 1 < len(pieces[piece]):
            test_piece(piece, rotation + 1, 0, grid, ghost, ghost_grid, solution)
    return


ghost_grid = 0
p = 0
print("Indicate with 0 for no ghost and 1 for ghost:")
while True:
    line = input()
    if not re.match(r"[0-1]{4}$", line):
        print("Put only 4 digits of 0 or 1")
    else:
        for l in line:
            ghost_grid += int(l) * 2**p
            p += 1
    if p > 15:
        break

test_piece(0, 0, 0, 0, 0, ghost_grid, solution)
