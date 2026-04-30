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

        
b = Board()
agent1 = RandomAgent(1)
agent2 = RandomAgent(2)
print("Starting game!")
x = 0
while(not b.game_over):
    x += 1
    agent1.make_move(b)
    print("Player 1 move: ")
    print(b)
    agent2.make_move(b)
    print("Player 2 move: ")
    print(b)

print("Game finished")