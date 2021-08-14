import cv2
import numpy as np

def process(filename):
    img = cv2.imread(f"./Project_Camera/{filename}.bmp")
    img = img[10:120,20:130] #Crop img
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Converting an image to gray scale
    
    frame = ''
    Quarter1_avg = np.mean((gray[10][15], gray[10][40], gray[40][15], gray[40][40]), dtype=int)
    Quarter2_avg = np.mean((gray[10][70], gray[10][95], gray[40][70], gray[40][95]), dtype=int)
    Quarter3_avg = np.mean((gray[60][15], gray[60][40], gray[85][15], gray[85][40]), dtype=int)
    Quarter4_avg = np.mean((gray[60][70], gray[60][95], gray[85][70], gray[85][95]), dtype=int)

    Quarter1 = [gray[10][15], gray[10][40], gray[40][15], gray[40][40],Quarter1_avg]
    Quarter2 = [gray[10][70], gray[10][95], gray[40][70], gray[40][95],Quarter2_avg]
    Quarter3 = [gray[60][15], gray[60][40], gray[85][15], gray[85][40],Quarter3_avg]
    Quarter4 = [gray[60][70], gray[60][95], gray[85][70], gray[85][95],Quarter4_avg]

    frame = Quarter2+Quarter4+Quarter1+Quarter3
    frame.append('A')
    
    return frame
