# Assignment 12 Analysis -- Emily
'''
	-pull out spike and y-layers in image
	-(spike) look at distributions of synapse density in the spike across x,y,z
	-make old plots prettier/writeup this weekend
	-(spike) in old hist graphs, make bin size a function of sample size
	-extract image(s) in dataset of y-layers
		-talk about it, analyze spatial distribution
	-heat maps/hex plots of y-layers, how is density distributed across them?
'''

# Setup
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
#%matplotlib inline 
import numpy as np
import urllib2
import scipy.stats as stats

np.set_printoptions(precision=3, suppress=True)
url = ('https://raw.githubusercontent.com/Upward-Spiral-Science'
       '/data/master/syn-density/output.csv')
data = urllib2.urlopen(url)
csv = np.genfromtxt(data, delimiter=",")[1:] # don't want first row (labels)

# chopping data based on thresholds on x and y coordinates
x_bounds = (409, 3529)
y_bounds = (1564, 3124)

def check_in_bounds(row, x_bounds, y_bounds):
    if row[0] < x_bounds[0] or row[0] > x_bounds[1]:
        return False
    if row[1] < y_bounds[0] or row[1] > y_bounds[1]:
        return False
    if row[3] == 0:
        return False
    
    return True

indices_in_bound, = np.where(np.apply_along_axis(check_in_bounds, 1, csv,
                                                 x_bounds, y_bounds))
data_thresholded = csv[indices_in_bound]
n = data_thresholded.shape[0]

def synapses_over_unmasked(row):
    s = (row[4]/row[3])*(64**3)
    return [row[0], row[1], row[2], s]

syn_unmasked = np.apply_along_axis(synapses_over_unmasked, 1, data_thresholded)
syn_normalized = syn_unmasked


# Extract images in dataset of y-layers
from image_scraping_jay import get_image_url
from PIL import Image
from cStringIO import StringIO
import requests
import urllib
import io

y_bounds = [(1564,1837), (1837,2071), (2071,2305), (2305,2539), (2539,3124)]

'''
for _, bounds in enumerate(y_bounds):
	new_im = Image.new('RGB',(1000,1000))
	temp = data_thresholded[:,1]
	temp = temp[np.logical_and(temp>=bounds[0], temp<bounds[1])]
	ys = np.unique(temp)
	i = 0
'''

def get_image(xrange,yrange,xs,ys):
	spacing = 100
	new_im = Image.new('RGB',(spacing*(10+len(xs[xrange[0]:xrange[1]])),spacing*(10+len(ys[yrange[0]:yrange[1]]))))
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
			#size =  (int(np.floor(1000/len(xs))),int(np.floor(500/len(ys))))
			#size =  (int(4000),int(np.floor(4000/len(ys))))
			size = (spacing,spacing)
			im.thumbnail(size, Image.ANTIALIAS)
			new_im.paste(im,(j,i))
			j += spacing + 10
		i += spacing + 10	
	new_im.save('new_im'+str(i)+'.bmp')
	new_im.show()

xs = np.unique(data_thresholded[:,0])
ys = np.unique(data_thresholded[:,1])
print ys.shape
print xs.shape
get_image((10,20),(15,20),xs,ys)


