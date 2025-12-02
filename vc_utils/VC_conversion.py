import numpy as np
import math
import sys
import cv2

greyscale_4levels = [[[1,0,1],
                      [1,0,1],
                      [0,0,1]], [[1,0,0],
                                 [1,1,1],
                                 [0,0,1]], [[0,1,1],
                                            [0,0,1],
                                            [1,0,1]], [[0,1,0],
                                                       [0,1,1],
                                                       [1,0,1]]]

def VC_conversion_diagonal(img):
    VC_img = np.zeros((img.shape[0]*2,img.shape[1]*2,4), np.uint8)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_px_val = img[i][j][0]

            VC_img[i*2][j*2][3] = 255 - img_px_val
            
            VC_img[i*2][j*2 + 1][3] = img_px_val

            VC_img[i*2 + 1][j*2][3] = img_px_val

            VC_img[i*2 + 1][j*2 + 1][3] = 255 - img_px_val
    return VC_img

def VC_conversion_vertical(img):
    VC_img = np.zeros((img.shape[0]*2,img.shape[1]*2,4), np.uint8)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_px_val = img[i][j][0]

            VC_img[i*2][j*2][3] = 255 - img_px_val
            
            VC_img[i*2][j*2 + 1][3] = img_px_val

            VC_img[i*2 + 1][j*2][3] = 255 - img_px_val

            VC_img[i*2 + 1][j*2 + 1][3] = img_px_val
    return VC_img

def VC_conversion_horizontal(img):
    VC_img = np.zeros((img.shape[0]*2,img.shape[1]*2,4), np.uint8)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_px_val = img[i][j][0]

            VC_img[i*2][j*2][3] = 255 - img_px_val
            
            VC_img[i*2][j*2 + 1][3] = 255 - img_px_val

            VC_img[i*2 + 1][j*2][3] = img_px_val

            VC_img[i*2 + 1][j*2 + 1][3] = img_px_val
    return VC_img

def VC_conversion_greyscale_4levels(img):
    VC_img = np.zeros((img.shape[0]*3,img.shape[1]*3,4), np.uint8)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            px_val = img[i][j][0]
            index = (int(px_val) + 1)//64 - 1
            for k in range(9):
                row = math.floor(k/3)
                column = k % 3
                VC_img[3*i+row][3*j+column][3] = greyscale_4levels[index][row][column]*255    #sets transparency to either 0 or 255 (all pixels are actually black)

    return VC_img

#filename = sys.argv[1]
#img = cv2.imread('outputs/' + filename)
#
#VC_img = VC_conversion_greyscale_4levels(img)
#
#cv2.imwrite('outputs/VC_' + filename, VC_img)
