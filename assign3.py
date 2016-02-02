#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc


def MakePyramid(image,minsize):
    pyramid = []
    #im=Image.open(image)
    while(image.size[0]>=minsize and image.size[1]>=minsize):
        pyramid.append(image)
    	image=image.resize((int(image.size[0]*0.75),int(image.size[1]*0.75)), Image.BICUBIC)
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
    image.save('imagePyramid.png','PNG')
    image.show()
    return 

def FindTemplate(pyramid, template, threshold):

    finalWidth= 15
    downsampleScale=template.size[0]/finalWidth 
    template = template.resize((finalWidth, template.size[1]/downsampleScale), Image.BICUBIC)
    
    points=[]
    
    for image in pyramid:
	normCrossCorr=ncc.normxcorr2D(image, template)
        largerThresh=np.where(normCrossCorr > threshold)
        points.append(zip(largerThresh[1], largerThresh[0]))
 
        img= pyramid[0].convert('RGB')
        
        for i in range(len(points)):
		point=points[i]
                scale=0.75*i
                print scale

                for pt in point:
                    ptx=pt[0]/scale
                    pty=pt[1]/scale

                    ptx1=template.size[0]/(2*scale)
                    pty1=template.size[1]/(2*scale)

                    x1 = ptx-ptx1
                    y1 = pty-pty1
                    x2 = ptx+ptx1
                    y2 = pty+pty1
                    draw=ImageDraw.Draw(img)
                    draw.line((x1,y1,x2,y2),fill="red",width=2)
    		    del draw
	return img


def run():
    
	images=['faces/judybats.jpg','faces/students.jpg','/faces/tree.jpg']
	for image in images:
		img = Image.open(image)
        	img = img.convert('L')

        	pyramid = MakePyramid(img,20)
        	ShowPyramid(pyramid)

                templateName = 'faces/template.jpg'
        	template = Image.open(templateName)
                template = template.convert('L')

      

       	 	threshold =0.532
        	result =FindTemplate(pyramid,template, threshold)
        	result.save('result.png','PNG')
        	result.show()
    	return


run()

   
