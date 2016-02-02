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

def ShowPyramid(pyramid1):
    width =0
    height = 0
    for img in pyramid1:
	width = width +img.size[0]
        height = max(height, img.size[1])
  
    image = Image.new("L", (width,height), 256)

    offset_x = 0
    offset_y = 0
   
    for img in pyramid1:
	image.paste(img, (offset_x, offset_y))
        offset_x = offset_x +img.size[0]
        offset_y = 0
    image.save('lenaPyramid.png','PNG')
    image.show()
    return 


minsize=64
pyramid=MakePyramid('lena.jpg',minsize)
ShowPyramid(pyramid)
