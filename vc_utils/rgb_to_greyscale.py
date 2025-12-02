import sys
import cv2

def rgb_to_greyscale(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    to_return = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    return to_return

#img = cv2.imread('inputs/lenna.png')
#gray_img = rgb_to_greyscale(img)
#cv2.imwrite('outputs/gray_image.png', gray_img)

#filename = sys.argv[1]
#img = cv2.imread('inputs/' + filename)
#
#gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#cv2.imwrite('outputs/gray_image.png', gray_img)
