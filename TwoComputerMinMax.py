import time
import numpy as np
import copy
class AI:
    @staticmethod
    def minimax(game_state,level):  # first call- computer player
        alpha = float('-inf')
        beta = float('inf')
        moves = AI.get_available_moves(game_state,"Black")
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            clone = AI.next_state(game_state, move,"Black")
            score = AI.min_play(clone,level-1,alpha,beta)
            if score > best_score:
                best_move = move
                best_score = score
            alpha = max(alpha, best_score)
            if beta <=alpha:
                break
        return best_move,best_score
    @staticmethod
    def min_play(game_state,level,alpha,beta):  # human player
        if AI.gameover(game_state) or level==0:
            return AI.evaluate(game_state)
        moves =AI.get_available_moves(game_state,"White")
        best_score = float('inf')
        for move in moves:
            clone = AI.next_state(game_state, move,"White")
            score = AI.max_play(clone,level-1,alpha,beta)
            if score < best_score:
                best_score = score
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score
    @staticmethod
    def max_play(game_state,level,alpha,beta):  # computer
        if AI.gameover(game_state) or level==0:
            return AI.evaluate(game_state)
        moves = AI.get_available_moves(game_state,"Black")
        best_score = float('-inf')
        for move in moves:
            clone = AI.next_state(game_state, move,"Black")
            score = AI.min_play(clone,level-1,alpha,beta)
            if score > best_score:
                best_score = score
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    @staticmethod
    def killdownright(clone,i,j):
        if (clone[i][j] == 3 or clone[i][j] == 4):
            if (i < 6 and j < 6) and clone[i + 2][j + 2] == 0 and (clone[i + 1][j + 1] == 2 or clone[i + 1][j + 1] == 1):
                return True
        return False
    @staticmethod
    def killdownleft(clone,i,j):
        if (clone[i][j] == 3 or clone[i][j] == 4):
            if (i < 6 and j > 1) and clone[i + 2][j - 2] == 0 and (clone[i + 1][j - 1] == 2 or clone[i + 1][j - 1] == 1):
                return True
        return False
    @staticmethod
    def BlackQueenupleftkill(clone,i,j):
        if clone[i][j] == 4:
            if (i>1 and j>1) and clone[i-2][j-2] == 0 and (clone[i - 1][j - 1] == 1 or clone[i - 1][j - 1] == 2):
                return True
        return False
    @staticmethod
    def BlackQueenuprightkill(clone,i,j):
        if clone[i][j] == 4:
            if (i > 1 and j < 6) and clone[i - 2][j + 2] == 0 and (clone[i - 1][j + 1] == 1 or clone[i - 1][j + 1] == 2):
                return True
        return False
    @staticmethod
    def killupleft(clone,i,j):
        if (clone[i][j] == 1 or clone[i][j] == 2):
            if (i > 1 and j > 1) and clone[i - 2][j -2] == 0 and (clone[i -1][j -1] == 3 or clone[i - 1][j - 1] == 4):
                return True
        return False
    @staticmethod
    def killupright(clone,i,j):
        if (clone[i][j] == 1 or clone[i][j] == 2):
            if (i >1 and j <6) and clone[i -2][j +2] == 0 and (clone[i -1][j +1] == 3 or clone[i - 1][j + 1] == 4):
                return True
        return False
    @staticmethod
    def WhiteQueenEatdownleft(clone,i,j):
        if clone[i][j] == 2:
            if (i <6 and j >1) and clone[i +2][j -2] == 0 and (clone[i +1][j -1] == 3 or clone[i + 1][j - 1] == 4):
                return True
        return False
    @staticmethod
    def WhiteQueenEatdownright(clone,i,j,):
        if clone[i][j] == 2:
            if (i < 6 and j < 6) and clone[i +2][j +2] == 0 and (clone[i +1][j +1] == 3 or clone[i + 1][j + 1] == 4):
                return True
        return False
    @staticmethod
    def WhiteSoldierMoves(clone,i,j,AvaibleMoves):
        if (clone[i][j] == 1 or clone[i][j] == 2):
            if (i > 0 and j > 0) and clone[i-1][j-1] == 0:
                AvaibleMoves.append((i, j, i-1, j - 1))
            if (i > 0 and j < 7) and clone[i-1][j+1] == 0:
                AvaibleMoves.append((i, j, i-1, j+1))
    @staticmethod
    def WhiteQueensMoves(clone,i,j,AvaibleMoves):
        if clone[i][j] == 2:
            if (i < 7 and j > 0) and clone[i + 1][j - 1] == 0:
                AvaibleMoves.append((i, j, i + 1, j - 1))
            if (i < 7 and j < 7) and clone[i + 1][j + 1] == 0:
                AvaibleMoves.append((i, j, i + 1, j + 1))
    @staticmethod
    def BlackSoldierMoves(clone,i,j,AvaibleMoves):
        if (clone[i][j] == 3 or clone[i][j] == 4):
            if (i < 7 and j > 0) and clone[i + 1][j - 1] == 0:
                AvaibleMoves.append((i, j, i + 1, j - 1))
            if (i < 7 and j < 7) and clone[i + 1][j + 1] == 0:
                AvaibleMoves.append((i, j, i + 1, j + 1))

    @staticmethod
    def BlackQueensMoves(clone,i,j,AvaibleMoves):
        if clone[i][j] == 4:
            if (i > 0 and j >0) and clone[i-1][j-1] == 0:
                AvaibleMoves.append((i, j, i-1, j-1))
            if (i > 0 and j <7) and clone[i-1][j+1] == 0:
                AvaibleMoves.append((i, j, i-1, j+1))
    @staticmethod
    def killsBlack(game_state, i, j, AvaibleMoves):
        Ifirst = i
        JFirst = j
        clone = copy.deepcopy(game_state)
        symbol = clone[Ifirst][JFirst]
        while AI.killdownleft(clone, i, j) or AI.killdownright(clone, i, j) or AI.BlackQueenuprightkill(clone, i,j) or AI.BlackQueenupleftkill(clone, i, j) or (Ifirst != i or JFirst != j):
            Eat = False
            if AI.killdownleft(clone, i, j):
                Eat = True
                clone[i + 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j - 2
                clone[i][j] = symbol
            elif AI.killdownright(clone, i, j):
                Eat = True
                clone[i + 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j + 2
                clone[i][j] = symbol
            elif AI.BlackQueenuprightkill(clone, i, j):
                Eat = True
                clone[i - 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j + 2
                clone[i][j] = symbol
            elif AI.BlackQueenupleftkill(clone, i, j):
                Eat = True
                clone[i - 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j - 2
                clone[i][j] = symbol
            if Eat:
                AvaibleMoves.append((Ifirst, JFirst, i, j))
            if not Eat:
                if (i > 0 and j > 0) and clone[i - 1][j - 1] == 5:
                    clone[i - 1][j - 1] = 0
                    clone[i][j] = 0
                    i, j = i - 2, j - 2
                if (i > 0 and j < 7) and clone[i - 1][j + 1] == 5:
                    clone[i - 1][j + 1] = 0
                    clone[i][j] = 0
                    i, j = i - 2, j + 2
                if symbol == 4:
                    if (i < 7 and j > 0) and clone[i + 1][j - 1] == 5:
                        clone[i + 1][j - 1] = 0
                        clone[i][j] = 0
                        i, j = i + 2, j - 2
                    if (i < 7 and j < 7) and clone[i + 1][j + 1] == 5:
                        clone[i + 1][j + 1] = 0
                        clone[i][j] = 0
                        i, j = i + 2, j + 2
                clone[i][j] = clone[Ifirst][JFirst]
        clone[Ifirst][JFirst] = symbol
        return clone
    @staticmethod
    def killsWhite(game_state, i, j, AvaibleMoves):
        Ifirst = i
        JFirst = j
        clone = copy.deepcopy(game_state)
        symbol = clone[Ifirst][JFirst]
        while AI.killupleft(clone, i, j) or AI.killupright(clone, i, j) or AI.WhiteQueenEatdownleft(clone, i,j) or AI.WhiteQueenEatdownright(clone, i, j) or (Ifirst != i or JFirst != j):
            Eat = False
            if AI.killupleft(clone, i, j):
                Eat =True
                clone[i-1][j-1] = 5
                clone[i][j] = 0
                i ,j =i-2,j-2
                clone[i][j] = symbol
            elif AI.killupright(clone, i, j):
                Eat =True
                clone[i-1][j+1] = 5
                clone[i][j] = 0
                i ,j =i-2,j+2
                clone[i][j] = symbol
            elif AI.WhiteQueenEatdownright(clone, i, j):
                Eat =True
                clone[i+1][j + 1] = 5
                clone[i][j] = 0
                i, j = i+2,j+2
                clone[i][j] = symbol
            elif AI.WhiteQueenEatdownleft(clone, i, j):
                Eat =True
                clone[i+1][j-1] = 5
                clone[i][j] = 0
                i, j = i + 2, j - 2
                clone[i][j] = symbol
            if Eat:
                AvaibleMoves.append((Ifirst, JFirst, i, j))
            if not Eat:
                if (i<7 and j>0) and clone[i+1][j-1] == 5:
                    clone[i+1][j-1] = 0
                    clone[i][j] = 0
                    i, j = i+2,j-2
                if (i < 7 and j < 7) and clone[i+1][j+1] == 5:
                    clone[i+1][j+1] = 0
                    clone[i][j] = 0
                    i, j =i+2, j+2
                if symbol == 2:
                    if (i > 0 and j > 0) and clone[i-1][j-1] == 5:
                        clone[i-1][j-1] = 0
                        clone[i][j] = 0
                        i, j =i-2, j-2
                    if (i > 0 and j <7) and clone[i-1][j+1] == 5:
                        clone[i-1][j+1] = 0
                        clone[i][j] = 0
                        i, j =i-2, j+2
                clone[i][j] = symbol
        clone[Ifirst][JFirst] = symbol
        return clone
    @staticmethod
    def get_available_moves(game_state,flag):
        AvailableMoves=[]
        Eat=False
        for i in range(8):
            for j in range(8):
                if flag=="Black":
                    AI.killsBlack(AI.killsBlack(game_state, i, j, AvailableMoves), i, j, AvailableMoves)
                if flag=="White":
                    AI.killsWhite(AI.killsWhite(game_state, i, j, AvailableMoves), i, j, AvailableMoves)
        if len(AvailableMoves)!=0:
            Eat=True
        if not Eat:
            for i in range(8):
                for j in range(8):
                    if flag=="White":
                        AI.WhiteSoldierMoves(game_state,i,j,AvailableMoves)
                        AI.WhiteQueensMoves(game_state,i,j,AvailableMoves)
                    if flag=="Black":
                        AI.BlackSoldierMoves(game_state,i,j,AvailableMoves)
                        AI.BlackQueensMoves(game_state,i,j,AvailableMoves)
        return AvailableMoves
    @staticmethod
    def next_state(game_state,move,flag):
        clone=copy.deepcopy(game_state)
        if not move[0] in (move[2]+1,move[2]-1) :
            if flag=="White":
                clone=AI.WhiteEatNextState(clone,move)
            if flag=="Black":
                clone=AI.BlackEatNextState(clone,move)
        else:
            clone[move[2]][move[3]] = clone[move[0]][move[1]]
            clone[move[0]][move[1]] = 0
        if move[2]==0 and clone[move[2]][move[3]]==1:
            clone[move[2]][move[3]]=2
        if move[2]==7 and clone[move[2]][move[3]]==3:
            clone[move[2]][move[3]]=4

        return clone

    @staticmethod
    def WhiteEatNextState(clone, Move):
        i = Move[0]
        j = Move[1]
        Ifirst = i
        JFirst = j
        symbol = clone[Ifirst][JFirst]
        while AI.killupleft(clone, i, j) or AI.killupright(clone, i, j) or AI.WhiteQueenEatdownleft(clone, i,
                                                                                                    j) or AI.WhiteQueenEatdownright(
            clone, i, j) or (Ifirst != i or JFirst != j):
            Eat = False
            if AI.killupleft(clone, i, j):
                Eat = True
                clone[i - 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j - 2
                clone[i][j] = symbol
            elif AI.killupright(clone, i, j):
                Eat = True
                clone[i - 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j + 2
                clone[i][j] = symbol
            elif AI.WhiteQueenEatdownright(clone, i, j):
                Eat = True
                clone[i + 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j + 2
                clone[i][j] = symbol
            elif AI.WhiteQueenEatdownleft(clone, i, j):
                Eat = True
                clone[i + 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j - 2
                clone[i][j] = symbol

            if i == Move[2] and j == Move[3]:
                for i1 in range(len(clone)):
                    for j1 in range(len(clone[i1])):
                        if clone[i1][j1] == 5:
                            clone[i1][j1] = 0
                break
            if not Eat:
                if (i < 7 and j > 0) and clone[i + 1][j - 1] == 5:
                    clone[i + 1][j - 1] = 0
                    clone[i][j] = 0
                    i, j = i + 2, j - 2
                if (i < 7 and j < 7) and clone[i + 1][j + 1] == 5:
                    clone[i + 1][j + 1] = 0
                    clone[i][j] = 0
                    i, j = i + 2, j + 2
                if symbol == 2:
                    if (i > 0 and j > 0) and clone[i - 1][j - 1] == 5:
                        clone[i - 1][j - 1] = 0
                        clone[i][j] = 0
                        i, j = i - 2, j - 2
                    if (i > 0 and j < 7) and clone[i - 1][j + 1] == 5:
                        clone[i - 1][j + 1] = 0
                        clone[i][j] = 0
                        i, j = i - 2, j + 2
            if i == Move[2] and j == Move[3]:
                for i1 in range(len(clone)):
                    for j1 in range(len(clone[i1])):
                        if clone[i1][j1] == 5:
                            clone[i1][j1] = 0
                break
                clone[i][j] = symbol
        return clone

    @staticmethod
    def BlackEatNextState(clone, Move):
        i = Move[0]
        j = Move[1]
        Ifirst = i
        JFirst = j
        symbol = clone[Ifirst][JFirst]
        while AI.killdownleft(clone, i, j) or AI.killdownright(clone, i, j) or AI.BlackQueenuprightkill(clone, i,
                                                                                                        j) or AI.BlackQueenupleftkill(
            clone, i, j) or (Ifirst != i or JFirst != j):
            Eat = False
            if AI.killdownleft(clone, i, j):
                Eat = True
                clone[i + 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j - 2
                clone[i][j] = symbol
            elif AI.killdownright(clone, i, j):
                Eat = True
                clone[i + 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j + 2
                clone[i][j] = symbol
            elif AI.BlackQueenuprightkill(clone, i, j):
                Eat = True
                clone[i - 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j + 2
                clone[i][j] = symbol
            elif AI.BlackQueenupleftkill(clone, i, j):
                Eat = True
                clone[i - 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j - 2
                clone[i][j] = symbol
            if i == Move[2] and j == Move[3]:
                for i1 in range(len(clone)):
                    for j1 in range(len(clone[i1])):
                        if clone[i1][j1] == 5:
                            clone[i1][j1] = 0
                break
            if not Eat:
                if (i > 0 and j > 0) and clone[i - 1][j - 1] == 5:
                    clone[i - 1][j - 1] = 0
                    clone[i][j] = 0
                    i, j = i - 2, j - 2
                if (i > 0 and j < 7) and clone[i - 1][j + 1] == 5:
                    clone[i - 1][j + 1] = 0
                    clone[i][j] = 0
                    i, j = i - 2, j + 2
                if symbol == 4:
                    if (i < 7 and j > 0) and clone[i + 1][j - 1] == 5:
                        clone[i + 1][j - 1] = 0
                        clone[i][j] = 0
                        i, j = i + 2, j - 2
                    if (i < 7 and j < 7) and clone[i + 1][j + 1] == 5:
                        clone[i + 1][j + 1] = 0
                        clone[i][j] = 0
                        i, j = i + 2, j + 2
                clone[i][j] = clone[Ifirst][JFirst]
            if i == Move[2] and j == Move[3]:
                for i1 in range(len(clone)):
                    for j1 in range(len(clone[i1])):
                        if clone[i1][j1] == 5:
                            clone[i1][j1] = 0
                break
        return clone
    @staticmethod
    def evaluate(game_state):
        score=0
        NumberWhitePieces=0
        NumberBlackPieces=0
        for i in range(8):
            for j in range(8):
                if game_state[i][j]==2:
                    score-=50
                if game_state[i][j]==4:
                    score+=50
                if game_state[i][j]==3:
                    NumberBlackPieces+=1
                    score+=i
                if game_state[i][j]==1:
                    NumberWhitePieces+=1
                    score-=8-i
        score+=-NumberWhitePieces*30+NumberBlackPieces*30
        if len(AI.get_available_moves(game_state,"White"))==0:
            return float('inf')
        elif len(AI.get_available_moves(game_state,"Black"))==0:
            return float('-inf')
        return score
    @staticmethod
    def gameover(game_state):
        if len(AI.get_available_moves(game_state,"White"))==0 or len(AI.get_available_moves(game_state,"Black"))==0:
            return True
        return False
class AI1:
    @staticmethod
    def minimax(game_state, level):  # first call- computer player
        alpha = float('-inf')
        beta = float('inf')
        moves = AI.get_available_moves(game_state, "White")
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            clone = AI.next_state(game_state, move, "White")
            score = AI1.min_play(clone, level - 1, alpha, beta)
            if score > best_score:
                best_move = move
                best_score = score
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_move, best_score

    @staticmethod
    def min_play(game_state, level, alpha, beta):  # human player
        if AI.gameover(game_state) or level == 0:
            return -AI.evaluate(game_state)
        moves = AI.get_available_moves(game_state, "Black")
        best_score = float('inf')
        for move in moves:
            clone = AI.next_state(game_state, move, "Black")
            score = AI1.max_play(clone, level - 1, alpha, beta)
            if score < best_score:
                best_score = score
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

    @staticmethod
    def max_play(game_state, level, alpha, beta):  # computer
        if AI.gameover(game_state) or level == 0:
            return -AI.evaluate(game_state)
        moves = AI.get_available_moves(game_state, "White")
        best_score = float('-inf')
        for move in moves:
            clone = AI.next_state(game_state, move, "White")
            score = AI1.min_play(clone, level - 1, alpha, beta)
            if score > best_score:
                best_score = score
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
time1 = time.time()
for i in range(100000):
    AI.killupleft(np.zeros((8,8)),0,0)
print((time1 - time.time())/100000)