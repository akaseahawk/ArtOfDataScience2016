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

def get_image_url(xcoord, ycoord, z, res=1):
    z += 2917
    z = int(z)
    x, y = get_tilenums_at_res(int(xcoord), int(ycoord), res)
    x = int(x)
    y = int(y)
    end = '/'+reduce(lambda x, y: str(x) +'_'+str(y), [y, x, res])
    end += '.png'
    imgurl = 'http://openconnecto.me/ocp/catmaid/bock11/image/xy/'+str(z) +end
    return imgurl

######################################################################
# REVISED IMAGE SCRAPER
from IPython.display import Image, HTML, display

# make coordinates to bin boundaries mapping
def cdata_to_pixels(cx, cy, res, binwidthx=0, binwidthy=0):
    bounds = [(c-19, c+(39*w)+20) for c,w in [(cx, binwidthx), (cy, binwidthy)]]
    bounds = np.array(bounds)
    power = 5-res
    return bounds*(2**power)

# This one combines tile images grabbed from viz.neurodata into a single image
# via javascript onto an HTML canvas, sort of clunky to include in notebooks,
# TODO: convert the HTML canvas into an image and save it as a PNG or something
def get_bin_image(cx, cy, xwidth=0, ywidth=0, cz=55, res=1, imsize=(512,512), disp_text=False):
    """Return the image of the bin corresponding to cx, cy, cz in the data
    params:
        cx, cy, xwidth, ywidth, cz - data coordinates/bin widths
        res - resolution to get image at
        imsize - width/height to output at
    returns:
        HTML for generating image, canvas id
    """
    z = 2917
    cx, cy = int(cx), int(cy)
    bounds = cdata_to_pixels(cx, cy, res, xwidth, ywidth)
    size = bounds[:, 1]-bounds[:,0]
    
    tiles = bounds//512
    # tiles = tiles + [[0, 1],[0, 1]]
    crops = np.empty((2, 2))
    crops = bounds-(tiles*512)
    # crops = crops.T
    tiles = tiles + [[0, 1],[0, 1]]
    imgtags = []
    ids = []
    cargs = {}
    for k, y in enumerate(np.arange(*tiles[1, :])):
        for i, x in enumerate(np.arange(*tiles[0,:])):
                width, height = [512]*2
                sx, sy, dx, dy = [0]*4
                if i==0:
                    # imgtags.append("<div> \n")
                    sx = crops[0, 0]
                    width=512 - crops[0, 0]
                elif i==len(np.arange(*tiles[1, :]))-1:
                    sx = 0
                    width=crops[0,1]
                if k==0:
                    height=512 - crops[1, 0]
                    sy = crops[1, 0]
                elif k==len(np.arange(*tiles[1, :]))-1:
                    sy = 0
                    height = crops[1, 1]
                newargs = {'sx':sx, 'sy':sy, 
                           'swidth':width, 'sheight':height,
                           'dx':0, 'dy':0,
                           'dwidth':width, 'dheight':height}
                end = '/'+reduce(lambda x, y: str(x) +'_'+str(y), [y, x, res])
                end += '.png'
                newid = str(i)+'-'+str(k)
                ids += [newid]
                cargs[newid] = newargs
                imgurl = 'http://openconnecto.me/ocp/catmaid/bock11/image/xy/'+str(z) +end
                imgtags.append("<img crossOrigin='Anonymous' src='%s' id='%s' style='display: none'/>" % (imgurl, newid))
    for xyid in ids:
        x, y = [int(i) for i in xyid.split('-')]
        if x > 0:
            prev = cargs[str(x-1)+'-'+str(y)]
            cargs[xyid]['dx'] += prev['dwidth']+prev['dx']
        if y > 0:
            prev = cargs[str(x)+'-'+str(y-1)]
            cargs[xyid]['dy'] += prev['dheight']+prev['dy']
    canvasID = int(np.random.ranf()*9999999)
    javascript = """
    <script>
        var c = document.getElementById('%s');
        c.width = %s;
        c.height = %s;
        var ctx = c.getContext("2d");
    """ % tuple([canvasID]+ list(size))
    for xyid in ids:
        javascript += "var img = document.getElementById('%s');\n" % xyid
        javascript += """
        ctx.drawImage(img, {sx}, {sy}, {swidth}, {sheight}, {dx}, {dy}, {dwidth}, {dheight} );
        """.format(**cargs[xyid])
            
    javascript += """
    var tempCanvas = document.createElement('canvas');
    tempCanvas.width = c.width;
    tempCanvas.height = c.height;
    tempCanvas.getContext('2d').drawImage(c, 0, 0);
    c.width = %s;
    c.height = %s;
    c.getContext('2d').drawImage(tempCanvas, 0, 0, tempCanvas.width, tempCanvas.height, 0, 0, c.width, c.height);
    """ % imsize

    javascript += '</script>'
    html = "<canvas id='%s'>" % canvasID
    html += "</canvas>"
    html += reduce(lambda x, y: x+'\n'+y, imgtags)+javascript
    html_raw = html
    html = HTML(html)
    display(html)
    return html_raw, canvasID
