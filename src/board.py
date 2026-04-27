class Board:
    def __init__(self):
        pass
    
    board_size = 9
    moves = 0
    board = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    last_move = 0;
    
    def move(move):
        if(move == 2 && last_move == 2) #end
        else


    #if even number of moves, then black turn
    #if odd number of moves, then white turn
    #two possible moves, place or pass (maybe resign later)
    #let's call move 1 place and move 2 pass. If there are two consecutive move 2s, the game ends. 
    #however, the ai will likely not willingly pass. The random move will definitely not since that won't even be an option.
    #so, it's more likely that the game will end by the move limit we set, which will be 400

    #have created a new branch for this code, which will specifically be restricted to this file