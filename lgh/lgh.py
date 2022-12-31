#!/usr/bin/env python3

import re
import argparse

__version__ = "2.0.3"

dict_nb_solution = dict()


class LGH:
    def __init__(self, ghost_grid, find=False, number=False):
        self.find = find
        self.number = number
        self.pieces = (
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
        self.ghost_grid = ghost_grid
        self.solution = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        self.nb_solution = 0

    def print_torch(self, color, position):
        if color == "R":
            return f"\33[31m{position}\33[0m"
        if color == "B":
            return f"\33[34m{position}\33[0m"
        if color == "G":
            return f"\33[32m{position}\33[0m"
        if color == "A":
            return f"\33[90m{position}\33[0m"
        return ""

    def print_solution(self, solution, ghost_grid):
        print("\n")
        print(f"Solution {self.nb_solution} :")
        for row in range(0, 4):
            line = ""
            for col in range(0, 4):
                pos_val = 2 ** (col + 4 * row)
                if pos_val & self.ghost_grid:
                    line += "o"
                else:
                    aprint = False
                    for s in range(0, 5):
                        if self.solution[s][1] & pos_val:
                            line += self.print_torch(
                                self.pieces[s][self.solution[s][0]][3][1],
                                self.pieces[s][self.solution[s][0]][3][2],
                            )
                            aprint = True
                            break
                        if aprint:
                            break
                    if not aprint:
                        line += "."
            print(line)

    def test_piece(self, piece, rotation, position, grid, ghost):
        rot = self.pieces[piece][rotation][0]
        pos = self.pieces[piece][rotation][1][position]
        gho = self.pieces[piece][rotation][2]
        tor = self.pieces[piece][rotation][3][0]
        val_grid = rot * 2**pos
        val_ghost = gho * 2**pos
        val_torch = tor * 2**pos
        if not (grid & val_grid) and not ((self.ghost_grid ^ val_ghost) & val_grid):
            self.solution[piece][0] = rotation
            self.solution[piece][1] = val_torch
            if piece + 1 < len(self.pieces):
                self.test_piece(
                    piece + 1,
                    0,
                    0,
                    grid + val_grid,
                    ghost + val_ghost,
                )
            elif grid + val_grid == 65535 and ghost == self.ghost_grid:
                if not self.number:
                    self.nb_solution += 1
                    self.print_solution(self.solution, self.ghost_grid)
                else:
                    if self.ghost_grid in dict_nb_solution:
                        dict_nb_solution[self.ghost_grid] += 1
                    else:
                        dict_nb_solution[self.ghost_grid] = 1
                return
            else:
                print("impossible")
        if position + 1 < len(self.pieces[piece][rotation][1]):
            self.test_piece(piece, rotation, position + 1, grid, ghost)
        elif rotation + 1 < len(self.pieces[piece]):
            self.test_piece(piece, rotation + 1, 0, grid, ghost)
        return


def main(find=False, number=False):
    if not find:
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
        lgh = LGH(ghost_grid, find=False, number=number)
        lgh.test_piece(0, 0, 0, 0, 0)
        if number:
            print(dict_nb_solution)
    else:
        for ghost_grid in range(1, 65535):
            if bin(ghost_grid).count("1") == 6:
                lgh = LGH(ghost_grid, find=True, number=number)
                lgh.test_piece(0, 0, 0, 0, 0)
        if number:
            print(dict_nb_solution)
            print(f"Number of possible cards : {len(dict_nb_solution)}")
            print(f"Number of max solutions : {max(dict_nb_solution.values())}")
            for i in range(1, max(dict_nb_solution.values()) + 1):
                print(
                    f"{i} solution{'s' if i>1 else ''} : {list(dict_nb_solution.values()).count(i)}"
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Lazy Ghost Hunters",
        description="Find solutions for the game Ghost Hunters.",
    )
    parser.add_argument(
        "-f",
        "--find",
        help="Find solutions for every combination of ghosts",
        action="store_true",
    )
    parser.add_argument(
        "-n",
        "--number",
        help="Give only the number of solutions",
        action="store_true",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()
    main(find=args.find, number=args.number)
