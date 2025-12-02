import numpy as np
import cv2

def rgb_to_binary(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)[1]
    return binary_image

def negative(img):
    neg_img = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            neg_img[i][j] = 255 - neg_img[i][j]
    return neg_img

def encrypt_binary(img, key):
    bw_img = rgb_to_binary(img)
    neg_img = negative(bw_img)

    cypher = np.zeros((key.shape[0], key.shape[1],3), np.uint8)

    for i in range(key.shape[0]):
        for j in range(key.shape[1]):
            key_px = float(key[i][j][0])
            img_px = float(neg_img[i][j])
            cypher[i][j] = int(abs(key_px - img_px))   #XOR
    
    return cypher

#filename = sys.argv[1]
#key = cv2.imread('outputs/key.png')
#img = cv2.imread('inputs/' + filename)
#
#bw_img = rgb_to_binary(img)
#neg_img = negative(bw_img)
#
#cypher = np.zeros((key.shape[0], key.shape[1],3), np.uint8)
#
#for i in range(key.shape[0]):
#    for j in range(key.shape[1]):
#        key_px = float(key[i][j][0])
#        img_px = float(neg_img[i][j])
#        cypher[i][j] = int(abs(key_px - img_px))   #XOR
#
#cv2.imwrite('outputs/cypher.png', cypher)
