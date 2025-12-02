import cv2

img = cv2.imread('baboon.png')

small_img = cv2.resize(img,(128,128))

cv2.imwrite('baboon_128.jpg', small_img)
