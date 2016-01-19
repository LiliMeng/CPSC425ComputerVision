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


print gauss1d(0.3)
print gauss1d(0.5)
print gauss1d(1)
print gauss1d(2)
