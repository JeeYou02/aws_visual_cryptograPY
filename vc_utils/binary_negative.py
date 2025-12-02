import cv2

img = cv2.imread('binary_image.png')

for row in range(img.shape[0]):
    for column in range(img.shape[1]):
        img[row,column] = 255 - img[row,column]

cv2.imwrite('negative_binary_image.png', img)
