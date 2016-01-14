from PIL import Image
import numpy as np
import math
from scipy import signal

def gauss1d(sigma):
    PI=3.1415926
    x=[-3, -2, -1, 0, 1, 2, 3]
    results=[]
    print "the result for sigma value %f is the following:" %sigma
    for index in range(len(x)):
    	result= 1/(math.sqrt(2*PI)*math.pow(sigma, 2))*math.exp(-math.pow(x[index],2)/(2*math.pow(sigma,2))) 
    	results.append(result)
    print results
    return 


gauss1d(0.3)
gauss1d(0.5)
gauss1d(1)
gauss1d(2)
