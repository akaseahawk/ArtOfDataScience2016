# Image scraping (Jay Miller)

import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import urllib2

plt.style.use('ggplot')
np.random.seed(1)
url = ('https://raw.githubusercontent.com/Upward-Spiral-Science'
       '/data/master/syn-density/output.csv')
data = urllib2.urlopen(url)
csv = np.genfromtxt(data, delimiter=",")[1:] # don't want first row (labels)
data = csv
sizes = [len(np.unique(data[:, i])) for i in range(3)]
ranges = [(np.max(data[:, i]), np.min(data[:,i])) for i in range(3)]
ranges_diff = [np.max(data[:, i])-np.min(data[:,i]) for i in range(3)]

xPix = 135424
yPix = 119808
xPixPerBin = xPix/108.0
yPixPerBin = yPix/86.0

def coords_to_px(xcoord, ycoord):
    c_vec = np.array([xcoord, ycoord], dtype='float')
    c_vec /= 40.0
    return (c_vec[0]*xPixPerBin, c_vec[1]*yPixPerBin)

def get_tilenums_at_res(xcoord, ycoord, res):
    x, y = coords_to_px(xcoord, ycoord)
    if(res == 0):
        x = np.floor(float(x)/512)
        y = np.floor(float(y)/512)
    else:
        x = np.floor(float(x)/(512*(2**res)))
        y = np.floor(float(y)/(512*(2**res)))
    return x,y

def get_image_url(xcoord, ycoord, z, res):
    z += 2917
    z = int(z)
    x, y = get_tilenums_at_res(int(xcoord), int(ycoord), res)
    x = int(x)
    y = int(y)
    end = '/'+reduce(lambda x, y: str(x) +'_'+str(y), [y, x, res])
    end += '.png'
    imgurl = 'http://openconnecto.me/ocp/catmaid/bock11/image/xy/'+str(z) +end
    return imgurl
