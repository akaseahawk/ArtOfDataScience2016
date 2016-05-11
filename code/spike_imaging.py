# Spike images
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
#%matplotlib inline 
import numpy as np
import urllib2
import scipy.stats as stats
from image_builder import get_image

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

a = np.apply_along_axis(lambda x:x[4]/x[3], 1, data_thresholded)
spike = a[np.logical_and(a <= 0.0015, a >= 0.0012)]
n, bins, _ = plt.hist(spike, 2000)
bin_max = np.where(n == n.max())
bin_width = bins[1]-bins[0]
syn_normalized[:,3] = syn_normalized[:,3]/(64**3)
spike = syn_normalized[np.logical_and(syn_normalized[:,3] <= 0.00131489435301+bin_width, syn_normalized[:,3] >= 0.00131489435301-bin_width)]
spike_thres = data_thresholded[np.logical_and(syn_normalized[:,3] <= 0.00131489435301+bin_width, syn_normalized[:,3] >= 0.00131489435301-bin_width)]
len_spike = len(spike_thres)

# Compare some of the bins represented the spike
xs = np.unique(spike_thres[:,0])
ys = np.unique(spike_thres[:,1])
get_image((0,10),(0,10),xs,ys,'spike'+str(0)+"_"+str(0))
