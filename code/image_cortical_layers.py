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


# Looking at images across y, and of the layers in the y-direction
#########################################################################################
from image_builder import get_image

xs = np.unique(data_thresholded[:,0])
ys = np.unique(data_thresholded[:,1])

# Layer across y
get_image((0,1),(0,len(ys)-1),xs,ys, "across_y")

# Each y-layer defined by bounds of local minima in total syn density at each y
y_bounds = [(1564,1837), (1837,2071), (2071,2305), (2305,2539), (2539,3124)]

for _, bounds in enumerate(y_bounds):
	y_lower = np.where(ys==bounds[0])[0][0]
	y_upper = np.where(ys==bounds[1])[0][0]
	print y_lower,y_upper
	i = get_image((0,1),(y_lower,y_upper),xs,ys,str(bounds[0])+"_"+str(bounds[1]))