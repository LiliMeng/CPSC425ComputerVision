from PIL import Image
import numpy as np
import math
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

print gauss2d(0.5)
print gauss2d(1)
