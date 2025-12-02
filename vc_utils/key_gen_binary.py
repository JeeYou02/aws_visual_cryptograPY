import random
import numpy as np
import sys
import cv2

def key_gen_binary(img):
    height = img.shape[0]
    width = img.shape[1]

    key = np.zeros((height, width, 3), np.uint8)

    for i in range(height):
        for j in range(width):
            key[i][j] = random.randint(0,1)*255
    
    return key

#filename = sys.argv[1]
#
#img = cv2.imread('inputs/' + filename)
#
#height = img.shape[0]
#width = img.shape[1]
#
#key = np.zeros((height, width, 3), np.uint8)
#
#for i in range(height):
#    for j in range(width):
#        key[i][j] = random.randint(0,1)*255
#
#
#cv2.imwrite('outputs/key.png', key)
