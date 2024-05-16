import numpy as np
import copy
import random
from datetime import datetime as d
def get_available_moves(game_state):
    list = []
    for i in range(len(game_state)):
        for j in range(len(game_state[i])):
            if game_state[i][j] == 0:
                list.append([i, j])
    return list

def win(game_state):
    wincondition = np.diag(game_state)
    wincondition.flatten()
    if sum(wincondition) == 30:
        return 1
    if sum(wincondition) == 3:
        return 2
    np.flip(wincondition, 0)
    wincondition = np.diag(np.fliplr(game_state))
    if sum(wincondition) == 30:
        return 1
    if sum(wincondition) == 3:
        return 2
    wincondition = game_state[:1, :3]
    wincondition = wincondition.flatten()
    if sum(wincondition) == 30:
        return 1
    if sum(wincondition) == 3:
        return 2
    wincondition = game_state[1:2, :3]
    wincondition = wincondition.flatten()
    if sum(wincondition) == 30:
        return 1
    if sum(wincondition) == 3:
        return 2
    wincondition = game_state[2:3, :3]
    wincondition = wincondition.flatten()
    if sum(wincondition) == 30:
        return 1
    if sum(wincondition) == 3:
        return 2
    wincondition = game_state[:3, :1]
    wincondition = wincondition.flatten()
    if sum(wincondition) == 30:
        return 1
    if sum(wincondition) == 3:
        return 2
    wincondition = game_state[:3, 1:2]
    wincondition = wincondition.flatten()
    if sum(wincondition) == 30:
        return 1
    if sum(wincondition) == 3:
        return 2
    wincondition = game_state[:3, 2:3]
    wincondition = wincondition.flatten()
    if sum(wincondition) == 30:
        return 1
    if sum(wincondition) == 3:
        return 2
    return 0
def draw1(game_state):
    for i in range(len(game_state)):
        for j in range(len(game_state[i])):
            if game_state[i][j]==0:
                return False
    return True
def gameover(game_state):
    if win(game_state)==1 or win(game_state)==2 or draw1(game_state):
        return True
    return False
def next_state(game_state, move,turn):
    clone = copy.deepcopy(game_state)
    clone[move[0]][move[1]]=turn
    return clone
def all_the_states(game_state):#כל המהלכים האפשריים למחשב
    listallboards=[]
    moves=get_available_moves(game_state)
    clone=copy.deepcopy(game_state)
    for move in moves:
        clone=next_state(clone,move,10)
        listallboards.append((clone,move))
        clone=copy.deepcopy(game_state)
    return listallboards    
#1-X, 10-O
class reinforcement:
    def __init__(self):
        self.alpha=0.9
        self.AllBoards={}
        self.states=[]
    def givereward(self,game_state):
        if win(game_state)==1 :
            self.update(1)
        elif win(game_state)==2:
            self.update(-1)
        else:
            self.update(-0.4)

    def ranking(self):
        game_state=[[0,0,0],
                    [0,0,0],
                    [0,0,0]]
        for i in range(20000):
            if i%1000==0:
                print(i)
                try:
                    print((d.now()-time).total_seconds())
                except:
                    None
                time=d.now()
            game_state1 = np.array(game_state)
            self.states=[]
            while not gameover(game_state1):
                moves=get_available_moves(game_state1)
                x=random.randint(0,len(moves)-1)
                game_state1=next_state(game_state1,moves[x],1)
                self.states.append(game_state1)
                if not gameover(game_state1):
                    nextstates = all_the_states(game_state1)
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
                    game_state1 = next_state(game_state1, move,10)
                    self.states.append(game_state1)
                else:
                    break
            self.givereward(game_state1)
        return self.AllBoards
    def update(self,reward):
        for st in reversed(self.states):
            if self.AllBoards.get(str(st)) is None:
                self.AllBoards[str(st)] = 0
            self.AllBoards[str(st)] += self.alpha * (reward - self.AllBoards[str(st)])
            reward = self.AllBoards[str(st)]
reinforcement1=reinforcement()
lists=reinforcement1.ranking()
game_state=[[0,0,0],
            [0,0,0],
            [0,0,0]]
game_won=0
game_lost=0
game_draw=0
for i in range(1000):
    move1=0
    game_state1 = np.array(game_state)
    while not gameover(game_state1):
        moves=get_available_moves(game_state1)
        x=random.randint(0,len(moves)-1)
        game_state1=next_state(game_state1,moves[x],1)
        move1+=1
        if not gameover(game_state1):  
            nextstates = all_the_states(game_state1)
            max = -999
            move = None
            for state in nextstates:
                value = 0
                if str(state[0]) in lists:
                    value = lists.get(str(state[0]))
                else:
                    value = 0
                if value > max:
                    max = value
                    move = state[1]
            game_state1 = next_state(game_state1, move, 10)
        else:
            break
    if win(game_state1)==1:
        game_won+=1
    elif win(game_state1)==2:
        game_lost+=1
    else:
        game_draw+=1
print(game_draw)
print(game_lost)
print(game_won)

