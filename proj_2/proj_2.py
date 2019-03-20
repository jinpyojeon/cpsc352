
import random

PLAYER = 0
BOT = 1
EMPTY = 2

class TicTacToe:


    def __init__(self):
        
        self.board = [EMPTY] * 9
        
    def calculate_best_move(self, board, player):
        
        opponent = BOT if player == PLAYER else PLAYER
        
        moves = self.get_possible_moves(board)

        score_moves = []

        for m in moves:
            _, opponent_score = self.calculate_best_move(board, player)
            
            score_moves.append((m, opponent_score))

        move, score = min(score_moves, lambda x : x[1])[0]
        
        return move, score

    def make_move(self, pos, player):
        if self.board[pos - 1] == EMPTY:
            self.board[pos - 1] = player
            return True
        return False

    
    def calculate_board(self):
        pass

    def get_possible_moves(self, board):
        return [i for i in board if i == EMPTY]
        
    def print_board(self):
        
        print_map = { PLAYER: 'X', BOT: 'O', EMPTY: '_' } 
        print_list = [print_map[i] for i in self.board]

        print('{0}{1}{2}\n{3}{4}{5}\n{6}{7}{8}'.format(*print_list))

    def is_won(self, player):
        
        def all_taken(pos_list):
            return all(map(lambda x : x == player, [self.board[i] for i in pos_list]))

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
        t.make_move(move, PLAYER)
        t.print_board()

        if not t.game_ended():
            
            valid_move = t.make_move(random.randint(0, 8), BOT)
            while not valid_move:
                valid_move = t.make_move(random.randint(0, 8), BOT)
            t.print_board()

    print('O is the winner!' if t.is_won(BOT) else 'X is the winner!')
        
    
   
