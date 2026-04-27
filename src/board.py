class Board:

    SIZE = 9

    def __init__(self):
        self.board = [[0]*Board.SIZE for _ in range(Board.SIZE)]
        self.moves = 0
        self.last_move = False

    
    def skip(self):
        if(self.last_move): #checks if opponent has already passed
            pass #if opponent has, then the game should end
        else: #if the opponent hasn't, then the game continues 
            self.moves += 1
            self.last_move = True

    def place(self, row, col): #uses a simply row and column to make the move
        #make a check to see whether the move is available
        if(self.moves % 2 == 0):
            piece = 1
        else:
            piece = 2

        if(self.board[row][col] == 1):
            print("Invalid move")
        else:
            self.board[row][col] = piece
        self.moves += 1
        
    def view_board(self):
        counter = 0
        for row in self.board:
            for col in row:
                print(col, end="")
                if(counter < 8):
                    print("|", end="")
                    counter += 1
                else:
                    print("")
                    counter = 0


def main():
    b = Board()
    b.place(1, 1)
    b.place(1,2)
    b.place(2,1)
    b.view_board()
    




    #if even number of moves, then black turn
    #if odd number of moves, then white turn
    #two possible moves, place or pass (maybe resign later)
    #let's call move 1 place and move 2 pass. If there are two consecutive move 2s, the game ends. 
    #however, the ai will likely not willingly pass. The random move will definitely not since that won't even be an option.
    #so, it's more likely that the game will end by the move limit we set, which will be 400

    #have created a new branch for this code, which will specifically be restricted to this file

if __name__ == "__main__":
    main()