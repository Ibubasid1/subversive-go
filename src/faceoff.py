from board import Board
from random_agent import RandomAgent
from alphabeta import AlphaBetaAgent


agent1win = 0
agent2win = 0
for i in range(25):
    board = Board()
    randAgent = RandomAgent(1)
    randAgent2 = RandomAgent(2)
    while(not board.game_over):    
        randAgent.make_move(board)
        randAgent2.make_move(board)
    if board.result == 1:
        agent1win += 1
    else:
        agent2win += 1  
    
for i in range(25):
    board = Board()
    randAgent = RandomAgent(2)
    randAgent2 = RandomAgent(1)
    while(not board.game_over):   
        randAgent2.make_move(board) 
        randAgent.make_move(board)
    if board.result == 2:
        agent1win += 1
    else:
        agent2win += 1  
    
    

print("One wins: ", str(agent1win))
print("Two wins: ", str(agent2win))
#Gives roughly 50:50 win ratio, meaning the two agents are completely random. for any model to outperform them it has to have a higher than 50% winrate
#If looking at just white vs black on the board, white wins almost 70% of the time, meaning most of the wins come down to komi

randWins = 0
abWins = 0
for i in range(25):
    board = Board()
    randAgent = RandomAgent(1)
    abAgent = AlphaBetaAgent()
    while(not board.game_over):
        randAgent.make_move(board)
        _, move = abAgent.search(board, abAgent.depth, float('-inf'), float('inf'), False)
        if move is None:
            board.skip()
        else:
            board.place(move[0], move[1])
    if board.result == 1:
        randWins += 1
    else:
        abWins += 1
    
for i in range(25):
    board = Board()
    randAgent = RandomAgent(2)
    abAgent = AlphaBetaAgent()
    while(not board.game_over):
        randAgent.make_move(board)
        _, move = abAgent.search(board, abAgent.depth, float('-inf'), float('inf'), True)
        if move is None:
            board.skip()
        else:
            board.place(move[0], move[1])
    if board.result == 2:
        randWins += 1
    else:
        abWins += 1
    print("Round ", i, " done.")
        
print("Random wins: ", str(randWins))
print("Alpha Beta wins: ", str(abWins))