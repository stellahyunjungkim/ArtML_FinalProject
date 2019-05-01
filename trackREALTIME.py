#
# @author: Stella Kim (hyunjunk), Kevin Song (kmsong)
#
# Some of the codes are from https://github.com/asingh33/CNNGestureRecognizer


import cv2
import numpy as np
import os
import time
import serial

import CNNclassify as myNN

minValue = 70

x0 = 400
y0 = 200
height = 200
width = 200

guessGesture = False
lastgesture = -1

kernel = np.ones((15,15),np.uint8)
kernel2 = np.ones((1,1),np.uint8)
skinkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

mod = 0
ArduinoSerial = 0


def skinMask(frame, x0, y0, width, height):
    global guessGesture, mod, lastgesture, ArduinoSerial
    # HSV values
    low_range = np.array([0, 50, 80])
    upper_range = np.array([30, 200, 255])
    # low_range = np.array([0, 58, 40])
    # upper_range = np.array([35, 174, 255])
    
    cv2.rectangle(frame, (x0,y0),(x0+width,y0+height),(0,255,0),1)
    roi = frame[y0:y0+height, x0:x0+width]
    
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    #Apply skin color range
    mask = cv2.inRange(hsv, low_range, upper_range)
    
    mask = cv2.erode(mask, skinkernel, iterations = 1)
    mask = cv2.dilate(mask, skinkernel, iterations = 1)
    
    # blur
    mask = cv2.GaussianBlur(mask, (15,15), 1)
    
    # bitwise and mask original frame
    res = cv2.bitwise_and(roi, roi, mask = mask)
    # color to grayscale
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    if guessGesture == True:


        res = cv2.resize(res, (28, 28)) 
        retgesture = myNN.guessGesture(mod, res)

        if lastgesture != retgesture :
            lastgesture = retgesture
            print myNN.output[lastgesture]
            ArduinoSerial.write(myNN.output[lastgesture])
            print "sending \"", myNN.output[lastgesture], "\" to Arduino"
            time.sleep(0.01)
            print ArduinoSerial.readline()
            time.sleep(0.01)
    
    return res


def Main():
    global guessGesture, mod, x0, y0, width, height, gestname, path, ArduinoSerial
    quietMode = False
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = 0.5
    fx = 10
    fy = 355
    fh = 18
    
    #Call CNN model loading callback
    while True:
        mod = myNN.loadCNN(0)
        break

    # Grab laptop camera input
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Original', cv2.WINDOW_NORMAL)

    # set rt size as 640x480
    ret = cap.set(3,640)
    ret = cap.set(4,480)

    ArduinoSerial = serial.Serial(port = '/dev/tty.usbmodem14401', baudrate = 9600) #com - Device manager on your computer
    time.sleep(0.01)
    
    while(True):
        ret, frame = cap.read()
        max_area = 0
        
        frame = cv2.flip(frame, 3)
        
        if ret == True:
            roi = skinMask(frame, x0, y0, width, height)
            roi = cv2.resize(roi, (200, 200)) 

        cv2.putText(frame,'Options:',(fx,fy + 3*fh), font, 0.7,(255,255,255),2,1)
        cv2.putText(frame,'ESC - Exit',(fx,fy + 6*fh), font, size,(255,255,255),1,1)
        if guessGesture:
            cv2.putText(frame,'p- Stop Prediction Mode',(fx,fy + 5*fh), font, size,(255,255,255),1,1)
        else:
            cv2.putText(frame,'p- Start Prediction Mode',(fx,fy + 5*fh), font, size,(255,255,255),1,1)

        cv2.imshow('Original',frame)
        cv2.imshow('ROI', roi)
        
        # Keyboard inputs
        key = cv2.waitKey(10) & 0xff
        
        ## Use Esc key to close the program
        if key == 27:
            break
        
        ## Use g key to start gesture predictions via CNN
        elif key == ord('p'):
            guessGesture = not guessGesture
            print "Prediction Mode - {}".format(guessGesture)

        ## Use i,j,k,l to adjust ROI window
        elif key == ord('i'):
            y0 = y0 - 5
        elif key == ord('k'):
            y0 = y0 + 5
        elif key == ord('j'):
            x0 = x0 - 5
        elif key == ord('l'):
            x0 = x0 + 5

    #Realse & destroy
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    Main()

