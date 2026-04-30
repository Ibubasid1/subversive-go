from board import Board
import random

class RandomAgent:

    def __init__(self, color):
        self.color = color
    
    def make_move(self, board: "Board"):
        valid_moves = board.legal_moves(self.color)
        pick = random.choice(list(valid_moves))
        if pick is None:
            board.skip()
        else:
            board.place(pick[0], pick[1])