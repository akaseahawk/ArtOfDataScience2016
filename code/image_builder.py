# Assignment 12 -- Emily

# Extract images in dataset of y-layers
from image_scraping_jay import get_image_url
from PIL import Image
from cStringIO import StringIO
import requests
import io
import numpy as np
import urllib2

def get_image(xrange,yrange,xs,ys,name):
	spacing = 100
	xsize = (spacing*len(xs[xrange[0]:xrange[1]]))
	ysize = (spacing*len(ys[yrange[0]:yrange[1]]))
	new_im = Image.new('RGB',(xsize,ysize))
	i = 0
	for y in ys[yrange[0]:yrange[1]]:
		j = 0
		for x in xs[xrange[0]:xrange[1]]:
			z = 1054
			im_url = get_image_url(x,y,z,1)
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			response = opener.open(im_url)
			img_file = StringIO(response.read())   
			im = Image.open(img_file)
			size = (spacing,spacing)
			im.thumbnail(size, Image.ANTIALIAS)
			new_im.paste(im,(j,i))
			j += spacing
		i += spacing	

	new_im.save(name+'.bmp')




