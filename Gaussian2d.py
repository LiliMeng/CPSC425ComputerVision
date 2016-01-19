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
    #print "the new sgima value is %f:" %newSigma
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

def guass2d(sigma):
    guas1d=gauss1d(sigma)
    guas1d = guas1d[np.newaxis]
    guas1dTrans=np.transpose(guas1d)
    #guas1dTrans=guas1dTrans[np.newaxis]
    finalResult=signal.convolve2d(guas1d,guas1dTrans)
    return finalResult

print guass2d(0.5)
print guass2d(1)
