
import random

PLAYER = 0
BOT = 1
EMPTY = 2

def opponent(player):
    return BOT if player == PLAYER else PLAYER

class TicTacToe:

    def __init__(self):
        
        self.board = [EMPTY] * 9
        
    
    def calculate_best_move(self, board, player):
        
        opponent = BOT if player == PLAYER else PLAYER

        moves = self.get_possible_moves(board)

        score_moves = []

        score = 0

        for m in moves:    

            moved_board = self.get_moved_board(board, m, player) 
            
            if self.is_won(player, moved_board):
                score += 1
            
            
            _, opponent_score = self.calculate_best_move(moved_board, 
                                                         opponent)
            
            score_moves.append((m, opponent_score))
        
        if len(score_moves) > 0: 
            move, score = min(score_moves, key = lambda x : x[1])
        
        return move, score

    def max_value(self, board, player):
        ended = terminal_state(self, board, player)
        if ended != 0:
            return ended
        
        score = float('inf')
        moves = self.get_possible_moves(board)

        for m in moves:
            score = max(score, self.min_value(board, player))   

        return score

    def max_value(self, board, player):
        ended = terminal_state(self, board, player)
        if ended != 0:
            return ended
        
        score = float('inf')
        moves = self.get_possible_moves(board)

        for m in moves:
            score = min(score, self.min_value(board, player))   

        return score
    
    def terminal_test(self, board, player):
        if self.is_won(player, board):
            return 1
        elif self.is_won(opponent(player), board):
            return -1
        else:
            return 0

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
        return self.is_won(PLAYER) or self.is_won(BOT)      

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
            best_move, _ = t.calculate_best_move(t.board, BOT) 
            t.make_move(best_move, BOT)
            t.print_board()
    print('O is the winner!' if t.is_won(BOT) else 'X is the winner!')
        
    
   
