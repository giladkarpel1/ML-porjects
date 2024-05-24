import numpy as np
from time import time
import copy
import pickle
import random
from datetime import datetime as d

def killdownright(clone,i,j):
    if (clone[i][j] == -1 or clone[i][j] == -2):
        if (i < 6 and j < 6) and clone[i + 2][j + 2] == 0 and (clone[i + 1][j + 1] == 2 or clone[i + 1][j + 1] == 1):
            return True
    return False

def killdownleft(clone,i,j):
    if (clone[i][j] == -1 or clone[i][j] == -2):
        if (i < 6 and j > 1) and clone[i + 2][j - 2] == 0 and (clone[i + 1][j - 1] == 2 or clone[i + 1][j - 1] == 1):
            return True
    return False

def BlackQueenupleftkill(clone,i,j):
    if clone[i][j] == -2:
        if (i>1 and j>1) and clone[i-2][j-2] == 0 and (clone[i - 1][j - 1] == 1 or clone[i - 1][j - 1] == 2):
            return True
    return False

def BlackQueenuprightkill(clone,i,j):
    if clone[i][j] == -2:
        if (i > 1 and j < 6) and clone[i - 2][j + 2] == 0 and (clone[i - 1][j + 1] == 1 or clone[i - 1][j + 1] == 2):
            return True
    return False

def killupleft(clone,i,j):
    if (clone[i][j] == 1 or clone[i][j] == 2):
        if (i > 1 and j > 1) and clone[i - 2][j -2] == 0 and (clone[i -1][j -1] == -1 or clone[i - 1][j - 1] == -2):
            return True
    return False

def killupright(clone,i,j):
    if (clone[i][j] == 1 or clone[i][j] == 2):
        if (i >1 and j <6) and clone[i -2][j +2] == 0 and (clone[i -1][j +1] == -1 or clone[i - 1][j + 1] == -2):
            return True
    return False

def WhiteQueenEatdownleft(clone,i,j):
    if clone[i][j] == 2:
        if (i <6 and j >1) and clone[i +2][j -2] == 0 and (clone[i +1][j -1] == -1 or clone[i + 1][j - 1] == -2):
            return True
    return False

def WhiteQueenEatdownright(clone,i,j,):
    if clone[i][j] == 2:
        if (i < 6 and j < 6) and clone[i +2][j +2] == 0 and (clone[i +1][j +1] == -1 or clone[i + 1][j + 1] == -2):
            return True
    return False

def WhiteSoldierMoves(clone,i,j,AvailableMoves):
    if (clone[i][j] == 1 or clone[i][j] == 2):
        if (i > 0 and j > 0) and clone[i-1][j-1] == 0:
            AvailableMoves.append((i, j, i-1, j - 1))
        if (i > 0 and j < 7) and clone[i-1][j+1] == 0:
            AvailableMoves.append((i, j, i-1, j+1))

def WhiteQueensMoves(clone,i,j,AvailableMoves):
    if clone[i][j] == 2:
        if (i < 7 and j > 0) and clone[i + 1][j - 1] == 0:
            AvailableMoves.append((i, j, i + 1, j - 1))
        if (i < 7 and j < 7) and clone[i + 1][j + 1] == 0:
            AvailableMoves.append((i, j, i + 1, j + 1))

def BlackSoldierMoves(clone,i,j,AvailableMoves):
    if (clone[i][j] == -1 or clone[i][j] == -2):
        if (i < 7 and j > 0) and clone[i + 1][j - 1] == 0:
            AvailableMoves.append((i, j, i + 1, j - 1))
        if (i < 7 and j < 7) and clone[i + 1][j + 1] == 0:
            AvailableMoves.append((i, j, i + 1, j + 1))

def BlackQueensMoves(clone,i,j,AvailableMoves):
    if clone[i][j] == -2:
        if (i > 0 and j >0) and clone[i-1][j-1] == 0:
            AvailableMoves.append((i, j, i-1, j-1))
        if (i > 0 and j <7) and clone[i-1][j+1] == 0:
            AvailableMoves.append((i, j, i-1, j+1))

def killsBlack(game_state, i, j, AvailableMoves):
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


def killsWhite(game_state, i, j, AvailableMoves):
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


def get_available_moves(game_state, flag):
    AvailableMoves = []
    for i in range(8):
        for j in range(8):
            if flag == "Black":
                killsBlack(killsBlack(game_state, i, j, AvailableMoves), i, j, AvailableMoves)
            if flag == "White":
                killsWhite(killsWhite(game_state, i, j, AvailableMoves), i, j, AvailableMoves)
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

def gameover(game_state,counterTimes):
    if len(get_available_moves(game_state,"White"))==0 or len(get_available_moves(game_state,"Black"))==0 or counterTimes==15:
        return True
    return False

def get_all_nextstates(game_state,flag):
    All_next_Boards=[]
    for move in get_available_moves(game_state,flag):
        All_next_Boards.append((next_state(game_state,move,flag),move))
    return All_next_Boards

def numberPieces(game_state):
    NumberPieces = 0
    for i in range(8):
        for j in range(8):
            if game_state[i][j] != 0:
                NumberPieces += 1
    return NumberPieces

def makeemptylist():
  list=np.zeros((8,8))
  for i in range(8):
      for j in range(8):
          if j%2==0 and i%2==1 and i<3 or j%2==1 and i%2==0 and i<3:
              list[i][j]=-1
          if j%2==0 and i%2==1 and i>=5 or j%2==1 and i%2==0 and i>=5:
              list[i][j]=1
  return list


def next_state(game_state, move, flag):
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

def WhiteEatNextState(clone, Move):
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

def BlackEatNextState(clone, Move):
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
    
    def ranking(self):#running all the games
        for i in range(100000):
            if i%10==0:
                print(i)
            game_state1 = np.array(makeemptylist())
            self.states=[]
            counterTimes=0
            moves1=0
            while not gameover(game_state1,counterTimes):
                previousNumber=numberPieces(game_state1)
                moves=get_available_moves(game_state1,"White")
                x=random.randint(0,len(moves)-1)
                game_state1=next_state(game_state1,moves[x],"White")
                if not gameover(game_state1,counterTimes):
                    '''moves=get_available_moves(game_state1,"Black")
                    x=random.randint(0,len(moves)-1)
                    game_state1=next_state(game_state1, moves[x],"Black")'''
                    nextstates = get_all_nextstates(game_state1, "Black")
                    max = -999
                    move = None
                    for state in nextstates:
                        if str(state[0]) in self.AllBoards:
                            value = self.AllBoards.get(str(state[0]))
                        else:
                            value = 0
                        if value > max:
                            max = value
                            move = state[1]
                    game_state1 = next_state(game_state1, move, "Black")
                    self.states.append(game_state1)
                    moves1+=1
                    if previousNumber==numberPieces(game_state1):
                        counterTimes+=1
                    else:
                        counterTimes=0
                else:
                    break
            self.givereward(game_state1,counterTimes)
        return self.AllBoards
    
    def givereward(self,game_state,counterTimes):#giving a evaluation when the game ended to the final board
        if len(get_available_moves(game_state,"White"))==0:
            self.update(1)
        if len(get_available_moves(game_state,"Black"))==0:
            self.update(-1)
        if counterTimes==25:
            self.update(-0.4)
            
    def update(self,reward):#updating all the following boards
        for st in reversed(self.states):
            if self.AllBoards.get(str(st)) is None:
                self.AllBoards[str(st)] = 0
            self.AllBoards[str(st)] += self.alpha * (reward - self.AllBoards[str(st)])
            reward = self.AllBoards[str(st)]
def loadPolicy(file):
    fr = open(file, 'rb')
    lists = pickle.load(fr)
    fr.close()
    return lists
reinforcement1=Reinforcement()
lists=reinforcement1.ranking()
def savePolicy():
    fw = open('model4', 'wb')
    pickle.dump(lists, fw)
    fw.close()
savePolicy()
