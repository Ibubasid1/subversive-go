from optimized_board import Board
from random_agent import RandomAgent
from alphabeta import AlphaBetaAgent
from mcts_agent import MCTS
import time


def winner(board):
    """Replaces the old board.result. Returns 1 if black wins (or ties), 2 if white wins."""
    board.fast_score()
    return 2 if board.white_score > board.black_score else 1


agent1win = 0
agent2win = 0
start_time = time.time()
for i in range(50):
    board = Board()
    randAgent = RandomAgent(1)
    randAgent2 = RandomAgent(2)
    while not board.game_over:
        randAgent.make_move(board)
        randAgent2.make_move(board)
    if winner(board) == 1:
        agent1win += 1
    else:
        agent2win += 1

for i in range(50):
    board = Board()
    randAgent = RandomAgent(2)
    randAgent2 = RandomAgent(1)
    while not board.game_over:
        randAgent2.make_move(board)
        randAgent.make_move(board)
    if winner(board) == 2:
        agent1win += 1
    else:
        agent2win += 1
print("Time taken: ", time.time() - start_time, " seconds.")

print("One wins: ", str(agent1win))
print("Two wins: ", str(agent2win))
#Gives roughly 50:50 win ratio, meaning the two agents are completely random. for any model to outperform them it has to have a higher than 50% winrate
#If looking at just white vs black on the board, white wins almost 70% of the time, meaning most of the wins come down to komi

randWins = 0
abWins = 0
start_time = time.time()
for i in range(50):
    board = Board()
    randAgent = RandomAgent(1)
    abAgent = AlphaBetaAgent()
    while not board.game_over:
        randAgent.make_move(board)
        _, move = abAgent.search(board, abAgent.depth, float('-inf'), float('inf'), False)
        board.place(move)
    if winner(board) == 1:
        randWins += 1
    else:
        abWins += 1

for i in range(50):
    board = Board()
    randAgent = RandomAgent(2)
    abAgent = AlphaBetaAgent()
    while not board.game_over:
        _, move = abAgent.search(board, abAgent.depth, float('-inf'), float('inf'), True)
        board.place(move)
        randAgent.make_move(board)
    if winner(board) == 2:
        randWins += 1
    else:
        abWins += 1

print("Time taken: ", time.time() - start_time, " seconds.")

print("Random wins: ", str(randWins))
print("Alpha Beta wins: ", str(abWins))


randWins = 0
mWins = 0
start_time = time.time()
for i in range(6):
    board = Board()
    randAgent = RandomAgent(1)
    mctsAgent = MCTS()
    while not board.game_over:
        randAgent.make_move(board)
        move = mctsAgent.get_best_move(board, 1)
        board.place(move)
    if winner(board) == 2:
        mWins += 1
    else:
        randWins += 1
        
print("Time taken: ", time.time() - start_time, " seconds.")

print("MCTS wins: ", str(mWins))
print("Random wins: ", str(randWins))
        
        