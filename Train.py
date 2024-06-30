from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from MinMax import *
import random
from keras.models import load_model
class Training():#Black Player
    def __init__(self):
        self.model = None
        self.alpha=0.9
        self.AllBoards_first={}
        self.AllBoards_second={}
        self.states=[]
        self.GameLogic = GameLogic()
        self.MinMax= MinMax()

    num_actions = 32  # The number of possible moves/actions

    def build_model (self, input_shape= (8,8,1)):
        model = Sequential ()
        model.add (Conv2D (32, (3, 3), activation='relu', input_shape=input_shape))
        model.add (MaxPooling2D ((2, 2)))
        model.add (Conv2D (64, (3, 3), activation='relu'))
        model.add (Flatten ())
        model.add (Dense (128, activation='relu'))
        model.add (Dense (1, activation='tanh'))
        model.compile (optimizer='adam', loss='mse')
        return model

    def givereward(self,game_state):#giving a evaluation when the game ended to the final board, black winning 1, white winnning -1
        if len(self.GameLogic.get_available_moves(game_state,"Black"))==0:
            self.update(1)

        elif len(self.GameLogic.get_available_moves(game_state,"White"))==0:
            self.update(-1)

        else:
            self.update(0)
    def white_won(self, game_state):
        if len (self.GameLogic.get_available_moves (game_state, "Black")) == 0:
            return True
    def black_won(self, game_state):
        if len(self.GameLogic.get_available_moves(game_state,"White"))==0:
            return True
    def update(self,reward1):#updating all the following boards
        previous_st = self.states[-1]
        self.AllBoards[np.array2string(previous_st)] = reward1
        for st in reversed(self.states):
            if self.AllBoards.get(np.array2string(st)) is None:
                self.AllBoards[np.array2string(st)] = 0
            value = self.AllBoards[np.array2string(st)] + self.alpha * self.AllBoards[np.array2string(previous_st)]
            if value>1:
                self.AllBoards[np.array2string(st)] = 1
            elif value<-1:
                self.AllBoards[np.array2string(st)] = -1
            else:
                self.AllBoards[np.array2string(st)] = value
            previous_st= st

    def execute_one_game_withModels(self, net_player1, net_player2):
        moves1 = 0
        game_state1 = self.GameLogic.get_initial_state()
        while not self.GameLogic.gameover(game_state1) and moves1<100:
            nextstates = self.GameLogic.get_all_nextstates (game_state1, "White")
            states = np.array ([t[0].reshape(8,8,1) for t in nextstates])
            predictions = net_player1.predict (states, verbose=0)
            i = np.argmax(predictions)
            game_state1 = states[i]
            self.AllBoards_first[np.array2string(game_state1)] = predictions[i][0]
            self.AllBoards_second[np.array2string(game_state1)] = net_player2.predict\
            (game_state1.reshape(1,8,8,1), verbose=0)[0][0]
            self.states.append(game_state1)
            moves1 += 1
            if not self.GameLogic.gameover(game_state1) and moves1<100:
                nextstates = self.GameLogic.get_all_nextstates (game_state1, "Black")
                states = np.array ([t[0].reshape(8,8,1) for t in nextstates])
                predictions = net_player2.predict \
                    (states, verbose=0)
                i = np.argmin(predictions)
                game_state1 = states[i]
                self.AllBoards_second[np.array2string (game_state1)] = predictions[i][0]
                self.AllBoards_first[np.array2string (game_state1)] = net_player1.predict \
                    (game_state1.reshape(1,8,8,1), verbose=0)[0][0]
                self.states.append(game_state1)
                #x.convertfromlisttogame (game_state1)
                moves1 += 1
            else:
                break
        return game_state1, moves1
    def execute_one_game_withoutModels(self):
        moves1 = 0
        game_state1 = self.GameLogic.get_initial_state()
        while not self.GameLogic.gameover (game_state1) and moves1 < 100:
            nextstates = self.GameLogic.get_all_nextstates (game_state1, "White")
            states = np.array ([t[0].reshape(8,8,1) for t in nextstates])
            i = random.randint(0, len(states)-1)
            game_state1 = states[i]
            self.states.append (game_state1)
            moves1 += 1
            if not self.GameLogic.gameover (game_state1) and moves1 < 100:
                nextstates = self.GameLogic.get_all_nextstates (game_state1, "Black")
                states = np.array ([t[0].reshape (8, 8, 1) for t in nextstates])
                i = random.randint (0, len(states)-1)
                game_state1 = states[i]
                self.states.append (game_state1)
                moves1 += 1
            else:
                break
        return game_state1, moves1
    def train_model(self, network, data, AllBoards1):
        X_test = np.array ([AllBoards1[str(key)] for key in data if str(key) in AllBoards1.keys()])
        X_train = np.array ([key for key in data if str(key) in AllBoards1.keys()])
        print(X_test)
        network.fit (X_train, X_test, epochs=24, batch_size=12)
    def ranking(self):#running all the games, firstly
        player = self.build_model()
        curr_player = self.build_model()
        for transform in range(26):
            print("Next Model:")
            print(transform)
            self.states = []
            self.AllBoards = {}
            self.AllBoards_first={}
            self.AllBoards_second={}
            white_winnings =0
            black_winnings =0
            if transform%2==0:
                k= False
            for eps in range(20):
                if k:
                    game_state1, moves1 = self.execute_one_game_withoutModels()
                    self.givereward(game_state1)
                else:
                    game_state1, moves1 = self.execute_one_game_withModels(player, curr_player)#old model- white, updated_model - black
                if self.white_won(game_state1):
                    white_winnings+=1
                if self.black_won(game_state1):
                    black_winnings+=1
            try:
                if k:
                    self.train_model(player, self.states, self.AllBoards)
                    self.train_model(curr_player, self.states, self.AllBoards)
                else:
                    if white_winnings/(white_winnings+black_winnings)>0.5:
                        curr_player = player
                        player = self.build_model()
                        self.train_model(player, self.states, self.AllBoards_first)
                    else:
                        player = self.build_model()
                        self.train_model(player, self.states, self.AllBoards_second)
            except:#No winnings for black and for white
                if not k:
                    curr_player = player
                    player = self.build_model()
                    self.train_model(player, self.states, self.AllBoards_first)
        self.model = player
        self.model.save('final_model')
        return self.AllBoards_second
training = Training()
training.ranking()