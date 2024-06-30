import copy
import numpy as np
class GameLogic():

    def killdownright (self, clone, i, j):  # checking whether there is eating down right for black
        if (clone[i][j] == -1 or clone[i][j] == -2):
            if (i < 6 and j < 6) and clone[i + 2][j + 2] == 0 and (
                    clone[i + 1][j + 1] == 2 or clone[i + 1][j + 1] == 1):
                return True
        return False

    def killdownleft (self, clone, i, j):  # checking whether there is eating down left for black
        if (clone[i][j] == -1 or clone[i][j] == -2):
            if (i < 6 and j > 1) and clone[i + 2][j - 2] == 0 and (
                    clone[i + 1][j - 1] == 2 or clone[i + 1][j - 1] == 1):
                return True
        return False

    def BlackQueenupleftkill (self, clone, i, j):  # checking whether there is eating up left for black queen
        if clone[i][j] == -2:
            if (i > 1 and j > 1) and clone[i - 2][j - 2] == 0 and (
                    clone[i - 1][j - 1] == 1 or clone[i - 1][j - 1] == 2):
                return True
        return False

    def BlackQueenuprightkill (self, clone, i, j):  # checking whether there is eating up right for black queen
        if clone[i][j] == -2:
            if (i > 1 and j < 6) and clone[i - 2][j + 2] == 0 and (
                    clone[i - 1][j + 1] == 1 or clone[i - 1][j + 1] == 2):
                return True
        return False

    def killupleft (self, clone, i, j):  # checking whether there is eating up left for white
        if (clone[i][j] == 1 or clone[i][j] == 2):
            if (i > 1 and j > 1) and clone[i - 2][j - 2] == 0 and (
                    clone[i - 1][j - 1] == -1 or clone[i - 1][j - 1] == -2):
                return True
        return False

    def killupright (self, clone, i, j):  # checking whether there is eating up right for white
        if (clone[i][j] == 1 or clone[i][j] == 2):
            if (i > 1 and j < 6) and clone[i - 2][j + 2] == 0 and (
                    clone[i - 1][j + 1] == -1 or clone[i - 1][j + 1] == -2):
                return True
        return False

    def WhiteQueenEatdownleft (self, clone, i, j):  # checking whether there is eating down left for white queen
        if clone[i][j] == 2:
            if (i < 6 and j > 1) and clone[i + 2][j - 2] == 0 and (
                    clone[i + 1][j - 1] == -1 or clone[i + 1][j - 1] == -2):
                return True
        return False

    def WhiteQueenEatdownright (self, clone, i, j):  # checking whether there is eating down right for white queen
        if clone[i][j] == 2:
            if (i < 6 and j < 6) and clone[i + 2][j + 2] == 0 and (
                    clone[i + 1][j + 1] == -1 or clone[i + 1][j + 1] == -2):
                return True
        return False

    def WhiteSoldierMoves (self, clone, i, j, AvailableMoves):  # adding the white solider moves
        if (clone[i][j] == 1 or clone[i][j] == 2):
            if (i > 0 and j > 0) and clone[i - 1][j - 1] == 0:
                AvailableMoves.append ((i, j, i - 1, j - 1))
            if (i > 0 and j < 7) and clone[i - 1][j + 1] == 0:
                AvailableMoves.append ((i, j, i - 1, j + 1))

    def WhiteQueensMoves (self, clone, i, j, AvailableMoves):  # adding the white queen moves
        if clone[i][j] == 2:
            if (i < 7 and j > 0) and clone[i + 1][j - 1] == 0:
                AvailableMoves.append ((i, j, i + 1, j - 1))
            if (i < 7 and j < 7) and clone[i + 1][j + 1] == 0:
                AvailableMoves.append ((i, j, i + 1, j + 1))

    def BlackSoldierMoves (self, clone, i, j, AvailableMoves):  # adding the black solider moves
        if (clone[i][j] == -1 or clone[i][j] == -2):
            if (i < 7 and j > 0) and clone[i + 1][j - 1] == 0:
                AvailableMoves.append ((i, j, i + 1, j - 1))
            if (i < 7 and j < 7) and clone[i + 1][j + 1] == 0:
                AvailableMoves.append ((i, j, i + 1, j + 1))

    def BlackQueensMoves (self, clone, i, j, AvailableMoves):  # adding the black queen moves
        if clone[i][j] == -2:
            if (i > 0 and j > 0) and clone[i - 1][j - 1] == 0:
                AvailableMoves.append ((i, j, i - 1, j - 1))
            if (i > 0 and j < 7) and clone[i - 1][j + 1] == 0:
                AvailableMoves.append ((i, j, i - 1, j + 1))

    def killsBlack (self, game_state, i, j,
                    AvailableMoves):  # calculating all the kills of black soliders, including mult kills
        Ifirst = i
        JFirst = j
        clone = copy.deepcopy (game_state)
        symbol = game_state[i][j]
        while self.killdownleft ( clone, i, j) or self.killdownright ( clone, i, j) or\
                self.BlackQueenuprightkill ( clone, i,j) or self.BlackQueenupleftkill (
                 clone, i, j) or (Ifirst != i or JFirst != j):
            Eat = False
            if self.killdownleft ( clone, i, j):
                Eat = True
                clone[i + 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j - 2
                clone[i][j] = symbol
            elif self.killdownright ( clone, i, j):
                Eat = True
                clone[i + 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j + 2
                clone[i][j] = symbol
            elif self.BlackQueenuprightkill ( clone, i, j) and clone[i][j] == -2:
                Eat = True
                clone[i - 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j + 2
                clone[i][j] = symbol
            elif self.BlackQueenupleftkill ( clone, i, j) and clone[i][j] == -2:
                Eat = True
                clone[i - 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j - 2
                clone[i][j] = symbol
            if Eat and not (self.killdownleft (clone, i, j) or self.killdownright (clone, i, j) or
                            self.BlackQueenuprightkill (clone, i, j) or self.BlackQueenupleftkill (clone, i, j)):
                AvailableMoves.append ((Ifirst, JFirst, i, j))
            if not Eat:
                if (i > 0 and j > 0) and clone[i - 1][j - 1] == 5:
                    clone[i - 1][j - 1] = 0
                    clone[i][j] = 0
                    i, j = i - 2, j - 2
                elif (i > 0 and j < 7) and clone[i - 1][j + 1] == 5:
                    clone[i - 1][j + 1] = 0
                    clone[i][j] = 0
                    i, j = i - 2, j + 2
                elif symbol == -2:
                    if (i < 7 and j > 0) and clone[i + 1][j - 1] == 5:
                        clone[i + 1][j - 1] = 0
                        clone[i][j] = 0
                        i, j = i + 2, j - 2
                    elif (i < 7 and j < 7) and clone[i + 1][j + 1] == 5:
                        clone[i + 1][j + 1] = 0
                        clone[i][j] = 0
                        i, j = i + 2, j + 2
                clone[i][j] = clone[Ifirst][JFirst]


        clone[Ifirst][JFirst] = symbol
        return clone

    def killsWhite (self, game_state, i, j,
                    AvailableMoves):  # calculating all the kills of white soliders, including mult kills
        Ifirst = i
        JFirst = j
        clone = copy.deepcopy (game_state)
        symbol = game_state[i][j]
        while self.killupleft ( clone, i, j) or self.killupright ( clone, i, j) or \
                self.WhiteQueenEatdownleft\
                    ( clone, i,j) or self.WhiteQueenEatdownright ( clone, i, j) or (Ifirst != i or JFirst != j):
            Eat = False
            if self.killupleft ( clone, i, j):
                Eat = True
                clone[i - 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j - 2
                clone[i][j] = symbol
            elif self.killupright ( clone, i, j):
                Eat = True
                clone[i - 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j + 2
                clone[i][j] = symbol
            elif self.WhiteQueenEatdownright ( clone, i, j) and clone[i][j] == 2:
                Eat = True
                clone[i + 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j + 2
                clone[i][j] = symbol
            elif self.WhiteQueenEatdownleft ( clone, i, j) and clone[i][j] == 2:
                Eat = True
                clone[i + 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j - 2
                clone[i][j] = symbol
            if Eat and not (self.killupleft (clone, i, j) or self.killupright (clone, i, j) or
                            self.WhiteQueenEatdownleft (clone, i, j) or self.WhiteQueenEatdownright (clone, i, j)):
                AvailableMoves.append ((Ifirst, JFirst, i, j))
            if not Eat:
                if i < 7 and j > 0 and clone[i + 1][j - 1] == 5:
                    clone[i + 1][j - 1] = 0
                    clone[i][j] = 0
                    i, j = i + 2, j - 2
                if i < 7 and j < 7 and clone[i + 1][j + 1] == 5:
                    clone[i + 1][j + 1] = 0
                    clone[i][j] = 0
                    i, j = i + 2, j + 2
                if symbol == 2:
                    if i > 0 and j > 0 and clone[i - 1][j - 1] == 5:
                        clone[i - 1][j - 1] = 0
                        clone[i][j] = 0
                        i, j = i - 2, j - 2
                    if (i > 0 and j < 7) and clone[i - 1][j + 1] == 5:
                        clone[i - 1][j + 1] = 0
                        clone[i][j] = 0
                        i, j = i - 2, j + 2
                clone[i][j] = symbol

        clone[Ifirst][JFirst] = symbol
        return clone

    def get_available_moves (self, game_state, flag):  # returning all of the available moves in a current game state
        AvailableMoves = []
        for i in range (8):
            for j in range (8):
                if flag == "Black":
                    self.killsBlack (game_state, i, j, AvailableMoves)
                if flag == "White":
                    self.killsWhite (game_state, i, j, AvailableMoves)
        if len (AvailableMoves) == 0:
            for i in range (8):
                for j in range (8):
                    if flag == "White":
                        self.WhiteSoldierMoves ( game_state, i, j, AvailableMoves)
                        self.WhiteQueensMoves ( game_state, i, j, AvailableMoves)
                    if flag == "Black":
                        self.BlackSoldierMoves ( game_state, i, j, AvailableMoves)
                        self.BlackQueensMoves (game_state, i, j, AvailableMoves)
        return AvailableMoves

    def gameover (self, game_state):  # checks whether the game is finished
        if len (self.get_available_moves (game_state, "White")) == 0 or len (self.get_available_moves (game_state, "Black")) == 0:
            return True
        return False

    def get_all_nextstates (self, game_state, flag):  # getting all the next states from a current state
        All_next_Boards = []
        for move in self.get_available_moves (game_state, flag):
            All_next_Boards.append ((self.next_state (game_state, move, flag), move))
        return All_next_Boards

    def next_state (self, game_state, move, flag):  # getting a move and returning the new board after the move
        clone = copy.deepcopy (game_state)
        if not move[0] in (move[2] + 1, move[2] - 1):
            if flag == "White":
                clone = self.WhiteEatNextState (clone, move)
            if flag == "Black":
                clone = self.BlackEatNextState (clone, move)
        else:
            clone[move[2]][move[3]] = clone[move[0]][move[1]]
            clone[move[0]][move[1]] = 0
        if move[2] == 0 and clone[move[2]][move[3]] == 1:
            clone[move[2]][move[3]] = 2
        if move[2] == 7 and clone[move[2]][move[3]] == -1:
            clone[move[2]][move[3]] = -2
        return np.array(clone)

    def WhiteEatNextState (self, game_state, Move):  # getting the move and returning the new board after the move, for mult kills
        i = Move[0]
        j = Move[1]
        Ifirst = i
        JFirst = j
        clone = copy.deepcopy (game_state)
        symbol = game_state[i][j]
        while self.killupleft (clone, i, j) or self.killupright ( clone, i, j) or \
                self.WhiteQueenEatdownleft (clone, i,j) or self.WhiteQueenEatdownright ( clone, i, j) \
                or (Ifirst != i or JFirst != j):
            Eat = False
            if self.killupleft (clone, i, j):
                Eat = True
                clone[i - 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j - 2
                clone[i][j] = symbol
            elif self.killupright (clone, i, j):
                Eat = True
                clone[i - 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j + 2
                clone[i][j] = symbol
            elif self.WhiteQueenEatdownright (clone, i, j):
                Eat = True
                clone[i + 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j + 2
                clone[i][j] = symbol
            elif self.WhiteQueenEatdownleft (clone, i, j):
                Eat = True
                clone[i + 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j - 2
                clone[i][j] = symbol

            if i == Move[2] and j == Move[3]:
                for i1 in range (len (clone)):
                    for j1 in range (len (clone[i1])):
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
                for i1 in range (len (clone)):
                    for j1 in range (len (clone[i1])):
                        if clone[i1][j1] == 5:
                            clone[i1][j1] = 0
                break
        return clone

    def BlackEatNextState (self, game_state, Move):  # getting the move and returning the new board after the move, for mult kills
        i = Move[0]
        j = Move[1]
        Ifirst = i
        JFirst = j
        clone = copy.deepcopy(game_state)
        symbol = game_state[i][j]
        while self.killdownleft (clone, i, j) or self.killdownright (clone, i, j) or \
                self.BlackQueenuprightkill (clone, i,j) or self.BlackQueenupleftkill (clone, i, j) or \
                (Ifirst != i or JFirst != j):
            Eat = False
            if self.killdownleft (clone, i, j):
                Eat = True
                clone[i + 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j - 2
                clone[i][j] = symbol
            elif self.killdownright (clone, i, j):
                Eat = True
                clone[i + 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i + 2, j + 2
                clone[i][j] = symbol
            elif self.BlackQueenuprightkill (clone, i, j):
                Eat = True
                clone[i - 1][j + 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j + 2
                clone[i][j] = symbol
            elif self.BlackQueenupleftkill (clone, i, j):
                Eat = True
                clone[i - 1][j - 1] = 5
                clone[i][j] = 0
                i, j = i - 2, j - 2
                clone[i][j] = symbol
            if i == Move[2] and j == Move[3]:
                for i1 in range (len (clone)):
                    for j1 in range (len (clone[i1])):
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
                if symbol == -2:
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
                for i1 in range (len (clone)):
                    for j1 in range (len (clone[i1])):
                        if clone[i1][j1] == 5:
                            clone[i1][j1] = 0
                break
        return clone
    def change_perspective(self, clone):
        game= np.array([-j for j in np.rot90(np.rot90(clone))]).reshape(8,8)
        return game
    def get_opponent(self, player):
        if player == "White":
            return "Black"
        return "White"
    def get_initial_state (self):
        list = np.zeros ((8, 8))
        for i in range (8):
            for j in range (8):
                if j % 2 == 0 and i % 2 == 1 and i < 3 or j % 2 == 1 and i % 2 == 0 and i < 3:
                    list[i][j] = -1
                if j % 2 == 0 and i % 2 == 1 and i >= 5 or j % 2 == 1 and i % 2 == 0 and i >= 5:
                    list[i][j] = 1
        return list
