import cv2

def rgb_to_binary(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)[1]
    return binary_image

## Load the input image
#image = cv2.imread('andrea.jpg')
#cv2.imshow('Original', image)
#cv2.waitKey(0)
#
## Use the cvtColor() function to grayscale the image
#gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#cv2.imshow('Grayscale', gray_image)
#cv2.waitKey(0)
#
#thresh = 127
#binary_image = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)[1]
#cv2.imshow('Binary', binary_image)
#cv2.waitKey(0)
#
#cv2.imwrite('binary_image.png', binary_image)
