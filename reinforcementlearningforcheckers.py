import copy
import ast
import pickle
import numpy as np
from tensorflow.keras.optimizers import SGD
from keras.callbacks import  TensorBoard
from keras import regularizers
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
import time
import random
tensorboard_callback = TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True, write_images=True)

def killdownright(clone,i,j):#checking whether there is eating down right for black
    if (clone[i][j] == -1 or clone[i][j] == -2):
        if (i < 6 and j < 6) and clone[i + 2][j + 2] == 0 and (clone[i + 1][j + 1] == 2 or clone[i + 1][j + 1] == 1):
            return True
    return False
def killdownleft(clone,i,j):#checking whether there is eating down left for black
    if (clone[i][j] == -1 or clone[i][j] == -2):
        if (i < 6 and j > 1) and clone[i + 2][j - 2] == 0 and (clone[i + 1][j - 1] == 2 or clone[i + 1][j - 1] == 1):
            return True
    return False
def BlackQueenupleftkill(clone,i,j):#checking whether there is eating up left for black queen
    if clone[i][j] == -2:
        if (i>1 and j>1) and clone[i-2][j-2] == 0 and (clone[i - 1][j - 1] == 1 or clone[i - 1][j - 1] == 2):
            return True
    return False
def BlackQueenuprightkill(clone,i,j):#checking whether there is eating up right for black queen
    if clone[i][j] == -2:
        if (i > 1 and j < 6) and clone[i - 2][j + 2] == 0 and (clone[i - 1][j + 1] == 1 or clone[i - 1][j + 1] == 2):
            return True
    return False
def killupleft(clone,i,j):#checking whether there is eating up left for white
    if (clone[i][j] == 1 or clone[i][j] == 2):
        if (i > 1 and j > 1) and clone[i - 2][j -2] == 0 and (clone[i -1][j -1] == -1 or clone[i - 1][j - 1] == -2):
            return True
    return False
def killupright(clone,i,j):#checking whether there is eating up right for white
    if (clone[i][j] == 1 or clone[i][j] == 2):
        if (i >1 and j <6) and clone[i -2][j +2] == 0 and (clone[i -1][j +1] == -1 or clone[i - 1][j + 1] == -2):
            return True
    return False
def WhiteQueenEatdownleft(clone,i,j):#checking whether there is eating down left for white queen
    if clone[i][j] == 2:
        if (i <6 and j >1) and clone[i +2][j -2] == 0 and (clone[i +1][j -1] == -1 or clone[i + 1][j - 1] == -2):
            return True
    return False
def WhiteQueenEatdownright(clone,i,j):#checking whether there is eating down right for white queen
    if clone[i][j] == 2:
        if (i < 6 and j < 6) and clone[i +2][j +2] == 0 and (clone[i +1][j +1] == -1 or clone[i + 1][j + 1] == -2):
            return True
    return False
def WhiteSoldierMoves(clone,i,j,AvailableMoves):#adding the white solider moves
    if (clone[i][j] == 1 or clone[i][j] == 2):
        if (i > 0 and j > 0) and clone[i-1][j-1] == 0:
            AvailableMoves.append((i, j, i-1, j - 1))
        if (i > 0 and j < 7) and clone[i-1][j+1] == 0:
            AvailableMoves.append((i, j, i-1, j+1))
def WhiteQueensMoves(clone,i,j,AvailableMoves):#adding the white queen moves
    if clone[i][j] == 2:
        if (i < 7 and j > 0) and clone[i + 1][j - 1] == 0:
            AvailableMoves.append((i, j, i + 1, j - 1))
        if (i < 7 and j < 7) and clone[i + 1][j + 1] == 0:
            AvailableMoves.append((i, j, i + 1, j + 1))
def BlackSoldierMoves(clone,i,j,AvailableMoves):#adding the black solider moves
    if (clone[i][j] == -1 or clone[i][j] == -2):
        if (i < 7 and j > 0) and clone[i + 1][j - 1] == 0:
            AvailableMoves.append((i, j, i + 1, j - 1))
        if (i < 7 and j < 7) and clone[i + 1][j + 1] == 0:
            AvailableMoves.append((i, j, i + 1, j + 1))
def BlackQueensMoves(clone,i,j,AvailableMoves):#adding the black queen moves
    if clone[i][j] == -2:
        if (i > 0 and j >0) and clone[i-1][j-1] == 0:
            AvailableMoves.append((i, j, i-1, j-1))
        if (i > 0 and j <7) and clone[i-1][j+1] == 0:
            AvailableMoves.append((i, j, i-1, j+1))
def killsBlack(game_state, i, j, AvailableMoves):#caculating all the kills of black soliders, including mult kills
    Ifirst = i
    JFirst = j
    clone = copy.deepcopy(game_state)
    symbol = clone[Ifirst][JFirst]
    while killdownleft(clone, i, j) or killdownright(clone, i, j) or BlackQueenuprightkill(clone, i,j) or BlackQueenupleftkill(clone, i, j) or (Ifirst != i or JFirst != j):
        Eat = False
        if killdownleft(clone, i, j):
            Eat = True
            clone[i + 1][j - 1] = 5
            clone[i][j] = 0
            i, j = i + 2, j - 2
            clone[i][j] = symbol
        if killdownright(clone, i, j):
            Eat = True
            clone[i + 1][j + 1] = 5
            clone[i][j] = 0
            i, j = i + 2, j + 2
            clone[i][j] = symbol
        if BlackQueenuprightkill(clone, i, j) and clone[i][j]==-2:
            Eat = True
            clone[i - 1][j + 1] = 5
            clone[i][j] = 0
            i, j = i - 2, j + 2
            clone[i][j] = symbol
        if BlackQueenupleftkill(clone, i, j) and clone[i][j]==-2:
            Eat = True
            clone[i - 1][j - 1] = 5
            clone[i][j] = 0
            i, j = i - 2, j - 2
            clone[i][j] = symbol
        if Eat:
            AvailableMoves.append((Ifirst, JFirst, i, j))
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
    clone[Ifirst][JFirst] = symbol
    return clone


def killsWhite(game_state, i, j, AvailableMoves):#calculating all the kills of white soliders, including mult kills
    Ifirst = i
    JFirst = j
    clone = copy.deepcopy(game_state)
    symbol = clone[Ifirst][JFirst]
    while killupleft(clone, i, j) or killupright(clone, i, j) or WhiteQueenEatdownleft(clone, i,j) or WhiteQueenEatdownright(clone, i, j) or (Ifirst != i or JFirst != j):
        Eat = False
        if killupleft(clone, i, j):
            Eat = True
            clone[i - 1][j - 1] = 5
            clone[i][j] = 0
            i, j = i - 2, j - 2
            clone[i][j] = symbol
        if killupright(clone, i, j):
            Eat = True
            clone[i - 1][j + 1] = 5
            clone[i][j] = 0
            i, j = i - 2, j + 2
            clone[i][j] = symbol
        if WhiteQueenEatdownright(clone, i, j) and clone[i][j]==2:
            Eat = True
            clone[i + 1][j + 1] = 5
            clone[i][j] = 0
            i, j = i + 2, j + 2
            clone[i][j] = symbol
        if WhiteQueenEatdownleft(clone, i, j) and clone[i][j]==2:
            Eat = True
            clone[i + 1][j - 1] = 5
            clone[i][j] = 0
            i, j = i + 2, j - 2
            clone[i][j] = symbol
        if Eat:
            AvailableMoves.append((Ifirst, JFirst, i, j))
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
            clone[i][j] = symbol
    clone[Ifirst][JFirst] = symbol
    return clone


def get_available_moves(game_state, flag):#returning all of the available moves in a current game state
    AvailableMoves = []
    board=  []
    for i in range(8):
        for j in range(8):
            if flag == "Black":
                killsBlack(game_state, i, j, AvailableMoves)
            if flag == "White":
                killsWhite(game_state, i, j, AvailableMoves)
    if len(AvailableMoves) == 0:
        for i in range(8):
            for j in range(8):
                if flag == "White":
                    WhiteSoldierMoves(game_state, i, j, AvailableMoves)
                    WhiteQueensMoves(game_state, i, j, AvailableMoves)
                if flag == "Black":
                    BlackSoldierMoves(game_state, i, j, AvailableMoves)
                    BlackQueensMoves(game_state, i, j, AvailableMoves)
    return AvailableMoves

def gameover(game_state):#checks whether the game is finished
    if len(get_available_moves(game_state,"White"))==0 or len(get_available_moves(game_state,"Black"))==0:
        return True
    return False

def get_all_nextstates(game_state,flag):#getting all the next states from a current state
    All_next_Boards=[]
    for move in get_available_moves(game_state,flag):
        All_next_Boards.append((next_state(game_state,move,flag),move))
    return np.array(All_next_Boards)
def numberPieces(game_state):
    NumberPieces = 0
    for i in range(8):
        for j in range(8):
            if game_state[i][j] != 0:
                NumberPieces += 1
    return NumberPieces
def makeemptylist():#make a new game list
  list=np.zeros((8,8))
  for i in range(8):
      for j in range(8):
          if j%2==0 and i%2==1 and i<3 or j%2==1 and i%2==0 and i<3:
              list[i][j]=-1
          if j%2==0 and i%2==1 and i>=5 or j%2==1 and i%2==0 and i>=5:
              list[i][j]=1
  return list


def next_state(game_state, move, flag):#getting a move and returning the new board after the move
    clone = copy.deepcopy(game_state)
    if not move[0] in (move[2] + 1, move[2] - 1):
        if flag == "White":
            clone = WhiteEatNextState(clone, move)
        if flag == "Black":
            clone = BlackEatNextState(clone, move)
    else:
        clone[move[2]][move[3]] = clone[move[0]][move[1]]
        clone[move[0]][move[1]] = 0
    if move[2] == 0 and clone[move[2]][move[3]] == 1:
        clone[move[2]][move[3]] = 2
    if move[2] == 7 and clone[move[2]][move[3]] == -1:
        clone[move[2]][move[3]] = -2
    return clone

def WhiteEatNextState(clone, Move):#getting the move and returning the new board after the move, for mult kills
    i = Move[0]
    j = Move[1]
    Ifirst = i
    JFirst = j
    symbol = clone[Ifirst][JFirst]
    while killupleft(clone, i, j) or killupright(clone, i, j) or WhiteQueenEatdownleft(clone, i,j) or WhiteQueenEatdownright(clone, i, j) or (Ifirst != i or JFirst != j):
        Eat = False
        if killupleft(clone, i, j):
            Eat = True
            clone[i - 1][j - 1] = 5
            clone[i][j] = 0
            i, j = i - 2, j - 2
            clone[i][j] = symbol
        elif killupright(clone, i, j):
            Eat = True
            clone[i - 1][j + 1] = 5
            clone[i][j] = 0
            i, j = i - 2, j + 2
            clone[i][j] = symbol
        elif WhiteQueenEatdownright(clone, i, j):
            Eat = True
            clone[i + 1][j + 1] = 5
            clone[i][j] = 0
            i, j = i + 2, j + 2
            clone[i][j] = symbol
        elif WhiteQueenEatdownleft(clone, i, j):
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
    return clone


def BlackEatNextState(clone, Move):#getting the move and returning the new board after the move, for mult kills
    i = Move[0]
    j = Move[1]
    Ifirst = i
    JFirst = j
    symbol = clone[Ifirst][JFirst]
    while killdownleft(clone, i, j) or killdownright(clone, i, j) or BlackQueenuprightkill(clone, i,j) or BlackQueenupleftkill(clone, i, j) or (Ifirst != i or JFirst != j):
        Eat = False
        if killdownleft(clone, i, j):
            Eat = True
            clone[i + 1][j - 1] = 5
            clone[i][j] = 0
            i, j = i + 2, j - 2
            clone[i][j] = symbol
        elif killdownright(clone, i, j):
            Eat = True
            clone[i + 1][j + 1] = 5
            clone[i][j] = 0
            i, j = i + 2, j + 2
            clone[i][j] = symbol
        elif BlackQueenuprightkill(clone, i, j):
            Eat = True
            clone[i - 1][j + 1] = 5
            clone[i][j] = 0
            i, j = i - 2, j + 2
            clone[i][j] = symbol
        elif BlackQueenupleftkill(clone, i, j):
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
            for i1 in range(len(clone)):
                for j1 in range(len(clone[i1])):
                    if clone[i1][j1] == 5:
                        clone[i1][j1] = 0
            break
    return clone



class Reinforcement:#Black Player
    def __init__(self):
        self.alpha=0.9
        self.AllBoards={}
        self.states=[]
        self.model = self.build_model()
    def build_model (self):
        model = Sequential ()
        model.add (Dense (64, input_shape=(64,)))
        model.add (Dense (4, activation='relu', kernel_regularizer=regularizers.l2 (0.01)))
        # output is passed to relu() because labels are binary
        model.add (Dense (1, activation='sigmoid', kernel_regularizer=regularizers.l2 (0.01)))
        model.compile (optimizer='adam', loss='mean_squared_error', metrics=['mae', 'mse'])
        return model
    def givereward(self,game_state,moves):#giving a evaluation when the game ended to the final board
        if len(get_available_moves(game_state,"White"))==0:
            self.update(1)
        if len(get_available_moves(game_state,"Black"))==0:
            self.update(-1)
        if moves>=100:
            self.update(0)

    def update(self,reward):#updating all the following boards
        for st in reversed(self.states):
            if self.AllBoards.get(np.array2string(st)) is None:
                self.AllBoards[np.array2string(st)] = 0
            self.AllBoards[np.array2string(st)] += self.alpha * (reward - self.AllBoards[np.array2string(st)])
            reward = self.AllBoards[np.array2string(st)]

    def ranking(self):#running all the games, firstly
        for i in range(10000):
            if i%100==0:
                print(i)
            game_state1 = np.array(makeemptylist())
            self.states=[]
            moves1=0
            while not gameover(game_state1) and moves1<100:
                moves = get_available_moves(game_state1, "White")
                value= np.random.uniform(0,1)
                if value<0.2 or i<20:
                    x= random.randint(0, len(moves)-1)
                    game_state1= next_state(game_state1, moves[x], "White")
                else:
                    nextstates = get_all_nextstates(game_state1, "White")
                    states = np.array ([t[0] for t in nextstates])
                    i = np.argmax(self.model.predict (states.reshape(states.shape[0], 64)))
                    game_state1 = next_state (game_state1, nextstates[i][1], "White")
                self.states.append (game_state1)
                moves1 += 1
                if not gameover(game_state1) and moves1<100:
                    moves = get_available_moves (game_state1, "Black")
                    value = np.random.uniform (0,1)
                    if value<0.2 or i<20:
                        x = random.randint (0, len(moves)-1)
                        game_state1 = next_state(game_state1, moves[x], "Black")
                    else:
                        nextstates = get_all_nextstates(game_state1, "Black")
                        states = np.array([t[0] for t in nextstates])
                        i = np.argmin (self.model.predict (states.reshape(states.shape[0], 64)))
                        game_state1 = next_state (game_state1, nextstates[i][1], "Black")
                    self.states.append (game_state1)
                    moves1 += 1
                else:
                    break
            self.givereward(game_state1, moves1)
            X_test = np.array([self.AllBoards[str(key)] for key in self.states])
            X_train= np.array(self.states)
            X_train = X_train.reshape(X_train.shape[0], 64)
            self.model.fit(X_train, X_test, epochs=16, batch_size=12, verbose=0, callbacks=[tensorboard_callback])
        self.model.save('final_model')
        return self.AllBoards
reinforcement1= Reinforcement()
lists= reinforcement1.ranking()

def loadPolicy(file):
    fr = open(file, 'rb')
    lists = pickle.load(fr)
    fr.close()
    return lists
def savePolicy():
    fw = open('model', 'wb')
    pickle.dump(lists, fw)
    fw.close()
savePolicy()
