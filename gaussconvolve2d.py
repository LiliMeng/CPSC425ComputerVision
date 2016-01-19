from PIL import Image
import numpy as np
import math
import cv2
from scipy import signal

def gauss1d(sigma):
    tmp=round(sigma*6)
    if tmp%2!=0:
    	length=tmp
    else:
    	length=tmp+1
    x=range(-(int)(length/2),(int)(length/2+1))
    PI=3.1415926 
    results=[]
    print "the result for sigma value %f is the following:" %sigma
    for index in range(len(x)):
    	result= 1/(math.sqrt(2*PI)*math.pow(sigma, 2))*math.exp(-math.pow(x[index],2)/(2*math.pow(sigma,2))) 
    	results.append(result)
    total=sum(results)
    results[:] = [x / total for x in results]
    #print results
    return np.array(results)

def gauss2d(sigma):
    gaus1d=gauss1d(sigma)
    gaus1d = gaus1d[np.newaxis]
    gaus1dTrans=np.transpose(gaus1d)
    finalResult=signal.convolve2d(gaus1d,gaus1dTrans)  # a 2D Gaussian can be formed by convolution of a 1D Gaussian with its transpose.
    return finalResult


def gaussconvolve2d(array,sigma):
    filter=gauss2d(sigma)
    gaussconvolve2dresult=signal.convolve2d(array,filter,'same')
    return gaussconvolve2dresult


rgb_image = Image.open('lena.jpg')
rgb_array=np.asarray(rgb_image)
gray_image=cv2.cvtColor(rgb_array, cv2.COLOR_BGR2GRAY)
im2_array = np.asarray(gray_image)
im3_array = im2_array.copy()
cv2.imwrite('gray_image.png',gray_image)
gray_image1 = Image.fromarray(gray_image)
gray_image1.save('gray_image.png','PNG')
cv2.imshow('gray_image',gray_image)
filtered_image=gaussconvolve2d(gray_image,3)
print filtered_image
filtered_image = filtered_image.astype('uint8')
filtered_image1 = Image.fromarray(filtered_image)
filtered_image1.save('filtered_image.png','PNG')
cv2.imshow('filtered_image',filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
