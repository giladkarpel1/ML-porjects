#collecting the data base
import numpy as np
import os
from numpy import asarray
import keras
import matplotlib.pyplot as plt
import face_recognition
from tensorflow.keras.utils import to_categorical
from PIL import Image
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Dense,LSTM, Dropout, Flatten
from numpy import argmax
from sklearn.model_selection import train_test_split
from keras.models import load_model
import cv2
import mediapipe as mp
import time
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
data_base=os.listdir(r"C:\Users\User\Data_base")
print(len(data_base))
lists=[]
time1=time.time()
path=r"C:\Users\User\Data_base"
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") #Note the change
num=0
for i in range(len(data_base)):
    img = Image.open(r"C:\Users\User\Data_base\\"+str(data_base[i]))
    img = asarray(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    try:
        for (x, y, w, h) in faces:
            img = Image.fromarray(img)
            img1 = img.crop((x, y, x+w, y+h)).resize((224, 224), Image.ANTIALIAS)
            back_img = Image.open('black-background.jpg').resize((224, 224), Image.ANTIALIAS)
            results = selfie_segmentation.process(asarray(img1))
            condition = np.stack((results.segmentation_mask,)*3,axis=-1)>0.5
            output_image = np.where(condition, img1, back_img)
        lists.append(output_image)
        num+=1
    except:
        pass
    if i%100==0:
        print(i)

data_base1=os.listdir(r"C:\Users\User\Data_base1")
print(time.time()-time1)
for i in range(len(data_base1)):
    img=Image.open(r"C:\Users\User\Data_base1\\"+str(data_base1[i])).resize((224, 224), Image.ANTIALIAS)
    img = asarray(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    try:
        for (x,y,w,h) in faces:
            img=Image.fromarray(img)
            img1=img.crop((x,y,x+w,y+h)).resize((224, 224), Image.ANTIALIAS)
            back_img=Image.open('black-background.jpg').resize((224, 224), Image.ANTIALIAS)
            results=selfie_segmentation.process(asarray(img1))
            condition=np.stack((results.segmentation_mask,)*3,axis=-1)>0.5
            output_image=np.where(condition,img1,back_img)
        lists.append(output_image)
    except:
        pass
    if i%100==0:
        print(i)
lists=np.array(lists)
lists=lists.astype('float32')
lists=lists/256.0
answers=[]
for i in range(num):
    answers.append(1)
for i in range(len(lists)-num):
    answers.append(0)
answers=np.array(answers)
x_train,x_test,y_train,y_test=train_test_split(lists,answers,train_size=0.7,shuffle=True)
print(x_train.shape)
def define_model():
    model = Sequential()
    model.add(Conv2D(input_shape=(224, 224, 3), filters=32, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Flatten())
    model.add(Dense(units=512, activation="relu"))
    model.add(Dense(units=512, activation="relu"))
    model.add(Dense(1))  # output layer
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model
model=define_model()
model.fit(x_train,y_train,batch_size=34,epochs=30)
model.save('Face_Recognition')