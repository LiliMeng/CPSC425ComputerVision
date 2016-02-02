from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc


def MakePyramid(image,minsize):
    pyramid = []
    im=Image.open(image)
    while(im.size[0]>=minsize and im.size[1]>=minsize):
        pyramid.append(im)
    	im=im.resize((int(im.size[0]*0.75),int(im.size[1]*0.75)), Image.BICUBIC)
    return pyramid
