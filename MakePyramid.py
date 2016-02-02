from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc


def MakePyramid(image,minsize):
    im=Image.open(image)
    s=im.size
    x=s[0]
    y=s[1]
    print x
    print y
    image_size=x*y
    while(x>minsize[0] and y>minsize[1]):
    	x=x*0.75
    	y=y*0.75
    	im1=im.resize((int(x),int(y)), Image.BICUBIC)
        im1.show()
    print im1.size
    return im1

minsize=[64,64]
pyramid=MakePyramid('lena.jpg',minsize)
