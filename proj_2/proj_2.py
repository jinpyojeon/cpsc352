
import random

PLAYER = 0
BOT = 1
EMPTY = 2

def opponent(player):
    return BOT if player == PLAYER else PLAYER

class TicTacToe:

    def __init__(self):
        
        self.board = [EMPTY] * 9
        
    def terminal_state(self, board, player):
        if self.is_won(player, board):
            return 1
        elif self.is_won(opponent(player), board):
            return -1
        else:
            return 0
    
    def max_value(self, board, player):
        ended = self.terminal_state(board, player)
        if ended != 0:
            return ended
        
        score = float('inf')
        moves = self.get_possible_moves(board)

        for m in moves:
            moved_board = self.get_moved_board(board, m, player)
            score = max(score, self.min_value(moved_board, opponent(player)))   

        return score

    def min_value(self, board, player):
        ended = self.terminal_state(board, player)
        if ended != 0:
            return ended
        
        score = float('inf')
        moves = self.get_possible_moves(board)

        for m in moves:
            moved_board = self.get_moved_board(board, m, player)
            score = min(score, self.max_value(moved_board, opponent(player)))   

        return score
    
    def calculate_best_move(self, board, player):
        
        moves = self.get_possible_moves(board)
        
        scored_moves = []

        for m in moves:
            if self.terminal_state(self.get_moved_board(board, m, player), player) == 1:
                return m

            moved_board = self.get_moved_board(board, m, player)
            scored_moves.append((m, self.min_value(moved_board, opponent(player))))

        best_move = max(scored_moves, key= lambda x : x[1])[0]

        return best_move
    

    def make_move(self, pos, player):
        if self.board[pos - 1] == EMPTY:
            self.board[pos - 1] = player
            return True
        return False

    def get_moved_board(self, board, move, player):
        assert(board[move - 1] == EMPTY)
        new_board = list(board)
        new_board[move - 1] = player
        return new_board

    def get_possible_moves(self, board):
        possible_moves = [i + 1 for i, v in enumerate(board) if v == EMPTY]
        return possible_moves        

    def print_board(self, board=None):
        if board is None:
            board = self.board
        
        print_map = { PLAYER: 'X', BOT: 'O', EMPTY: '_' } 
        print_list = [print_map[i] for i in board]

        print('{0}{1}{2}\n{3}{4}{5}\n{6}{7}{8}'.format(*print_list))

    def is_won(self, player, board=None):

        if not board:
            board = self.board
        
        def all_taken(pos_list):
            return all(map(lambda x : x == player, [board[i] for i in pos_list]))

        horizontal_list = [[i, i + 1, i + 2] for i in [0, 3, 6]]
        vert_list = [[i, i + 3, i + 6] for i in [0, 1, 2]]

        any_hori = any(map(all_taken, horizontal_list))
        any_vert = any(map(all_taken, vert_list))
        any_diag = all_taken([0, 4, 8]) or all_taken([2, 4, 6])

        return any_hori or any_vert or any_diag
  
    def game_ended(self):
        return self.is_won(PLAYER) or self.is_won(BOT) or len(self.get_possible_moves(self.board)) == 0     

if __name__ == '__main__':

    t = TicTacToe()
    print('Welcome to TTT! Make your move (row-major order):')

    while not t.game_ended():
        move = int(input())
        valid = t.make_move(move, PLAYER)
        while not valid:
            print('Not a valid move! Make your move: ')
            move = int(input())
            valid = t.make_move(move, PLAYER)
        if not t.game_ended():
            best_move = t.calculate_best_move(t.board, BOT) 
            t.make_move(best_move, BOT)
            t.print_board()
    
    if t.is_won(BOT):
        print('O is the winner!') 
    elif t.is_won(PLAYER):
        print('X is the winner!')
    else:
        print('It is a draw!')
            
        
    
   
