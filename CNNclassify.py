#
# @author: Stella Kim (hyunjunk), Kevin Song (kmsong)
#
# Some of the codes are from https://github.com/asingh33/CNNGestureRecognizer


from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD,RMSprop,adam
from keras.utils import np_utils
from keras import backend as K # for theano
K.set_image_dim_ordering('th')

import numpy as np
import os
import theano

import json

import cv2

# input image dimensions
img_rows, img_cols = 28, 28

# number of channels
# For grayscale use 1 value and for color images use 3 (R,G,B channels)
img_channels = 1

# Batch_size to train
batch_size = 32

# Number of output classes
nb_classes = 5

# Number of epochs to train
nb_epoch = 20

# Total number of convolutional filters to use
nb_filters = 32
# Max pooling
nb_pool = 2
# Size of convolution kernel
nb_conv = 3

# data
path = "./"
path1 = "./gestures"    #path of folder of images

# Path2 is the folder which is fed in to training model
# path2 = './imgfolder'
path2 = './small'
# WeightFileName = ["28x28half.hdf5"]
WeightFileName = ["28x28final.hdf5"]
output = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "NOTHING"]
# output = ["ZERO", "ONE", "TWO", "THREE", "FOUR"]


# Load CNN model
def loadCNN(wf_index):
    global get_output
    model = Sequential()
    
    model.add(Conv2D(nb_filters, (nb_conv, nb_conv),
                        padding='valid',
                        input_shape=(img_channels, img_rows, img_cols)))
    convout1 = Activation('relu')
    model.add(convout1)
    model.add(Conv2D(nb_filters, (nb_conv, nb_conv)))
    convout2 = Activation('relu')
    model.add(convout2)
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    
    
    # Model summary
    model.summary()
    # Model config details
    model.get_config()
    
    # from keras.utils import plot_model
    # plot_model(model, to_file='new_model.png', show_shapes = True)
    

    if wf_index >= 0:
        #Load pretrained weights
        fname = WeightFileName[int(wf_index)]
        print "loading ", fname
        model.load_weights(fname)
    
    layer = model.layers[11]
    get_output = K.function([model.layers[0].input, K.learning_phase()], [layer.output,])
    
    return model

# guess gesture
def guessGesture(model, img):
    global output, get_output
    #Load image and flatten 
    image = np.array(img).flatten()
    
    # reshape 
    image = image.reshape(img_channels, img_rows, img_cols)
    
    # float32
    image = image.astype('float32') 
    
    # normalize 
    image = image / 255
    
    # reshape for NN
    rimage = image.reshape(1, img_channels, img_rows, img_cols)
    # rimage = np.resize(rimage, (28, 28))
    # print(rimage)
    # feed it to the NN, to fetch the predictions
    prob_array = get_output([rimage, 0])[0]
    d = {}
    i = 0
    for items in output:
        d[items] = prob_array[0][i] * 100
        i += 1
    
    # Get the output with maximum probability
    import operator
    
    guess = max(d.iteritems(), key=operator.itemgetter(1))[0]
    prob  = d[guess]

    if prob > 70.0:
        
        with open('gesturejson.txt', 'w') as outfile:
            json.dump(d, outfile)

        return output.index(guess)

    else:
        return 1
