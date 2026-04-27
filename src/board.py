class Board:

    SIZE = 9

    def __init__(self):
        self.board = [[0]*Board.SIZE for _ in range(Board.SIZE)]
        self.moves = 0
        self.last_move = False
        self.current_player = 1

    
    def skip(self):
        if(self.last_move): #checks if opponent has already passed
            pass #if opponent has, then the game should end
        else: #if the opponent hasn't, then the game continues 
            self.moves += 1
            self.last_move = True

    def place(self, row, col): #uses a simply row and column to make the move
        #make a check to see whether the move is available
        if(self.board[row][col] == 1):
            print("Invalid move")
        else:
            self.board[row][col] = self.current_player

        self.moves += 1

        self.current_player = 2 if self.current_player == 1 else 1

    def __str__(self):
        rows = []
        for row in self.board:
            rows.append("|".join(str(cell) for cell in row))
        return "\n".join(rows)

    # def _traversal(self, row, col):
    #     run = True
    #     while run:
    #         if self.board[row + 1][col] == 



def main():
    b = Board()
    b.place(1, 1)
    b.place(1,2)
    b.place(2,1)
    print(b)
    
    




    #if even number of moves, then black turn
    #if odd number of moves, then white turn
    #two possible moves, place or pass (maybe resign later)
    #let's call move 1 place and move 2 pass. If there are two consecutive move 2s, the game ends. 
    #however, the ai will likely not willingly pass. The random move will definitely not since that won't even be an option.
    #so, it's more likely that the game will end by the move limit we set, which will be 400

    #have created a new branch for this code, which will specifically be restricted to this file

if __name__ == "__main__":
    main()