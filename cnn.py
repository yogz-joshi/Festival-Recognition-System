# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 13:34:27 2018

@author: YOGESH
"""
# Convolutional Neural Network

# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(32, (3, 3), input_shape = (64,64,3), activation = 'relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = 128, activation = 'relu'))

classifier.add(Dense(units = 6, activation = 'softmax'))
#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)'''
# Compiling the CNN
  
classifier.compile(optimizer='adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
# Part 2 - Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('dataset2/training_set',
                                                 target_size = (64,64),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('dataset2/test_set',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'categorical')
classifier.fit_generator(training_set,
                         steps_per_epoch = (4800/32),
                         epochs = 25,
                         validation_data = test_set,
                         validation_steps = (1200/32))
#classifier.save('festival.h5')
import numpy as np
from keras.preprocessing import image
test_image=image.load_img('rahul.jpg', target_size = (64,64 ))
test_image=image.img_to_array(test_image)
test_image = test_image/255
test_image=np.expand_dims(test_image , axis=0)
result = classifier.predict(test_image)

ind = np.unravel_index(np.argmax(result, axis=None), result.shape)
       
if(ind[1]==0):
     fest="Chhat Pooja"
    
if(ind[1]==1):
     fest="Christmas"   
if(ind[1]==2):
     fest="Diwali"
if(ind[1]==3):
     fest="Eid"       
if(ind[1]==4):
     fest="Holi"       
if(ind[1]==5):
     fest="Lohadi"   
     
from tkinter import *  
from PIL import ImageTk,Image  
root = Tk()  
canvas_width = 700
canvas_height = 580
canvas = Canvas(root,width=canvas_width , height=canvas_height )  
canvas.pack()  
Label(root, text=fest,padx = 10, bg="red", fg="white").pack()
img = ImageTk.PhotoImage(Image.open('rahul.jpg'))  
canvas.create_image(20, 20, anchor=NW, image=img)  

root.mainloop()  
   
