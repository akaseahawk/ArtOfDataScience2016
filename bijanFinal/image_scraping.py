# Image scraping (Jay Miller)
import matplotlib.pyplot as plt
import numpy as np
import urllib2
from skimage import io

def bin_to_nparray(cx, cy, cz=55, res=1, overlay=False):
    z = 2917+cz
    cx, cy = int(cx), int(cy)
    bounds = cdata_to_pixels(cx, cy, res)
    size = bounds[:, 1]-bounds[:,0]
    tiles = bounds//512
    # tiles = tiles + [[0, 1],[0, 1]]
    crops = np.empty((2, 2))
    crops = bounds-(tiles*512)
    # crops = crops.T
    tiles = tiles + [[0, 1],[0, 1]]
    xr, yr = [np.arange(*tiles[i, :]) for i in [0, 1]]
    imgs = [[tile_xy_to_nparray(x, y, res, z, overlay) for x in xr]
             for y in yr]
    np_imgs = []
    for y, imgarray in enumerate(imgs):
        for x, img in enumerate(imgarray):
            img = np.array(img)
            if x == 0:
                img = img[:,crops[0,0]:]
            if y == 0:
                img = img[crops[1,0]:, :]
            if x == len(xr)-1:
                img = img[:, :-(512-crops[0, 1])]
            if y == len(yr)-1:
                img = img[:-(512-crops[1, 1]), :]
            if x == 0:
                np_imgs.append(img)
            else:
                np_imgs[-1] = np.hstack((np_imgs[-1], img))

    return np.vstack(tuple(np_imgs))

def bin_and_overlay_to_nparray(cx, cy, cz=55, res=1):
    img = bin_to_nparray(cx, cy, cz, res)
    img_overlay = bin_to_nparray(cx, cy, cz, res, overlay=True)
    return img_overlay[:,:,-1]+img*.5

# make coordinates to bin boundaries mapping
def cdata_to_pixels(cx, cy, res, binwidthx=0, binwidthy=0):
    bounds = [(c-19, c+(39*w)+20) for c,w in [(cx, binwidthx), (cy, binwidthy)]]
    bounds = np.array(bounds)
    power = 5-res
    return bounds*(2**power)

def tile_xy_to_nparray(x, y, res, z=55, overlay=False):
    end = '/'+reduce(lambda x, y: str(x) +'_'+str(y), [y, x, res])
    end += '.png'
    imgurl = 'http://openconnecto.me/ocp/catmaid/bock11/image/xy/'+str(z)+end
    if overlay:
        imgurl = 'http://openconnecto.me/ocp/catmaid/mp4merged/annotation/xy/'+str(z)+end
    image = io.imread(imgurl)
    return image