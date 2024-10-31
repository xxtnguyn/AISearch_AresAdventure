from CONSTAINTS import *

import numpy as np

class Game:
    def __init__(self) -> None:
        self.board = None
        self.ares_start_pos = None
        self.goals = []
    
    def read_map_from_string(self, string):
        lines = string.strip().split('\n')

        # Read the weights
        weights = list(map(int, lines[0].strip().split())) 
        weight_index = 0

        max_width = max(len(line) for line in lines[1:]) # Find the row with max length
        nrow = len(lines) - 1
        ncol = max_width
        board = np.zeros((nrow, ncol), dtype=int)

        for row in range(nrow):
            line = lines[row + 1].ljust(max_width)
            for col in range(ncol):
                char = line[col]

                if char == WALL_CHAR:
                    board[row, col] = WALL_NUM
                if char == ARES_CHAR or char == ARES_GOAL_CHAR:
                    board[row, col] = ARES_NUM
                    self.ares_start_pos = (row, col)
                if char == ROCK_CHAR or char == ROCK_GOAL_CHAR:
                    board[row, col] = weights[weight_index]
                    weight_index += 1
                if char == GOAL_CHAR or char == ARES_GOAL_CHAR or char == ROCK_GOAL_CHAR:
                    self.goals.append((row, col))

        self.board = board

class State:
    def __init__(self, ares_pos, board, cost) -> None:
        self.ares_pos = ares_pos

        self.board = board # Ma trận 
        self.cost = cost
        self.heuristic = 0

    def __eq__(self, value: object) -> bool:
        return np.array_equal(self.board, value.board)
    
    def __hash__(self):
        return hash(self.board.tobytes())
    