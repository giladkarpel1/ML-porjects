import numpy as np
from tensorflow.keras.utils import to_categorical
import datetime
import tensorflow as tf
from sklearn.model_selection import train_test_split
import json
import random
from tensorflow.keras.optimizers import SGD
from keras.callbacks import  TensorBoard
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
import time
import pickle
data_base=10000
def loadPolicy(file):
    fr = open(file, 'rb')
    lists = pickle.load(fr)
    fr.close()
    return lists
lists=loadPolicy('model4')
def putIntolistThedata():
    newlist = []  # list with all the integers element in lists, the game states
    i=0
    s=False
    x=False
    for element in lists.keys():
        for element1 in element:
            if i%1000000 == 0:
                print(i)
            try:
                if s:
                    newlist.append(-int(element1))
                    s=False
                    i+=1
                else:
                    newlist.append(int(element1))
                    i+=1
                if i==64*data_base:
                    x=True
                    break
            except:
                if element1=='-':
                    s=True
        if x:
            break
    return newlist
def putTheAnswersIntoList():
    answers=[]#the values to a certain game state
    a=0
    for element in lists.values():
        a+=1
        if a==data_base+1:
            break
        answers.append(element)
    return answers
x=500
newlists=np.array(putIntolistThedata())
newlists=newlists.reshape((int(newlists.shape[0]/64),64))
answers=putTheAnswersIntoList()
answers=np.round((np.array(answers,dtype='float32'))*10)+10
counter=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
i=0
def purning(newlist,answers):
    l=0
    for i in range(len(answers)):#balancing the data, deleting boards
        if i%10000==0:
            print(i)
        if i<len(answers)-1 and l<len(answers)-1:
            counter[int(answers[l])]+=1
        else:
            break
        if counter[int(answers[l])]>=x:
            indexs=np.argwhere(answers==answers[l])
            indexs=indexs[indexs>l]
            answers = np.delete(answers,indexs)
            newlist = np.delete(newlist,indexs,0)
            indexs-=1
        l+=1
    return answers,newlist
answers,newlists=purning(newlists,answers)
for i in range(21):
    print(np.count_nonzero(i==answers),"  ",i)
answers=to_categorical(answers)
x,x_test,y,y_test=train_test_split(newlists,answers,shuffle=True,test_size=0.2)#shuffling the game states and answers
def build_model():
    model = Sequential()
    model.add(Dense(64, activation='tanh',input_shape=(64,)))#input layer
    model.add(Dense(120, activation='tanh'))#first hidden layer
    model.add(Dense(280, activation='tanh'))#second hidden layer
    model.add(Dense(320, activation='tanh'))#third hidden layer
    model.add(Dense(100, activation='tanh'))#fourth hidden layer
    model.add(Dense(21, activation='softmax'))#output layer
    opt = SGD(learning_rate=0.001,momentum=0.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    return model
model=build_model()
model.fit(x,y,batch_size=220,epochs=5000,validation_split=.1)
model.evaluate(x_test,y_test)
model.save('final_model')
