import sys
import cv2
import math

def saturate(val):
    if val < 0:
        return 0
    return val

def quantize_and_dither(img, N=4):  #N is number of gray levels (should be a power of 2)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            old_val = img[i][j][0]
            new_val = math.ceil(((old_val+1)/256.0)*N)*256/N - 1  #quantization
            error = new_val - old_val

            img[i][j] = new_val

            #floyd-steinberg dithering
            if(j+1 < img.shape[1]):
                img[i][j+1] = saturate(img[i][j+1][0] -  error * 7/16)
            if(i+1 < img.shape[0]):
                img[i+1][j] = saturate(img[i+1][j][0] - error * 5/16)
                if(j-1 >= 0):
                    img[i+1][j-1] = saturate(img[i+1][j-1][0] - error * 3/16)
                if(j+1 < img.shape[1]):
                    img[i+1][j+1] = saturate(img[i+1][j+1][0] - error * 1/16)
    return img

#N = 4   #gray levels (should be a power of 2)
#
##filename = sys.argv[1]
#img = cv2.imread('outputs/gray_image.png')
#
#img = quantize_and_dither(img, N)
#
#cv2.imwrite('outputs/quantized_dithered_image.png', img)
