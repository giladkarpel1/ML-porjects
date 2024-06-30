from GameLogic import *
class MinMax:
    def __init__(self):
        self.GameLogic= GameLogic()
    def minimax(self, game_state,level ,model, flag):  # first call- computer player
        alpha = float('-inf')
        beta = float('inf')
        moves =  self.GameLogic.get_available_moves(game_state,flag)
        best_move = moves[0]
        best_score = None
        if flag== "White":#White will try to minimize
            best_score = float('-inf')
            for move in moves:
                clone =  self.GameLogic.next_state(game_state, move,flag)
                score = self.min_play(clone,level-1,alpha,beta,model)
                if score > best_score:
                    best_move = move
                    best_score = score
                alpha = max(alpha, best_score)
                if beta <=alpha:
                    break
        if flag== "Black":#Black will try to maximize
            best_score = float('inf')
            for move in moves:
                clone = self.GameLogic.next_state (game_state, move, flag)
                score = self.max_play(clone,level-1,alpha,beta,model)
                if score < best_score:
                    best_score = score
                beta = min(beta, best_score)
                if beta <=alpha:
                    break
        return best_move, best_score

    def min_play(self, game_state,level,alpha,beta,model):  # human player
        if self.GameLogic.gameover(game_state) or level==0:
            value = model.predict (game_state.reshape (1, 8, 8), verbose=0)
            return value
        moves = self.GameLogic.get_available_moves(game_state,"Black")
        best_score = float('inf')
        for move in moves:
            clone =  self.GameLogic.next_state(game_state, move,"Black")
            score = self.max_play(clone,level-1,alpha,beta,model)
            if score < best_score:
                best_score = score
            beta = min(beta, best_score)
            if beta <=alpha:
                break
        return best_score

    def max_play(self, game_state,level,alpha,beta,model):  # computer
        if self.GameLogic.gameover(game_state) or level==0:
            value = model.predict (game_state.reshape (1, 8, 8), verbose=0)
            return value
        moves = self.GameLogic.get_available_moves(game_state,"White")
        best_score = float('-inf')
        for move in moves:
            clone = self.GameLogic.next_state(game_state, move,"White")
            score = self.min_play(clone,level-1,alpha,beta,model)
            if score > best_score:
                best_score = score
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score