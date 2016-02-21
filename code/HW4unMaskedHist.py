# unMaskedHist
"""
Created on Thu Feb 18 15:25:35 2016

@author: akash
"""

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import urllib2

url = ('https://raw.githubusercontent.com/Upward-Spiral-Science'
       '/data/master/syn-density/output.csv')
data = urllib2.urlopen(url)
csv = np.genfromtxt(data, delimiter=",")[1:] # don't want first row (labels)
print csv.shape

def check_condition(row):
    if row[4] == 0:
        return False
    return True

a = np.apply_along_axis(check_condition, 1, csv)
a = np.where(a == True)[0]
csv = csv[a, :]


newcsv = csv[:,3]/np.amax(csv[:,3])
newsyn = csv[:,4]/np.amax(csv[:,4])

print np.amax(csv[:,3])

fig = plt.figure(1)
ax = fig.gca()
plt.hist(csv[:,3],bins=100)
ax.set_title('Hist of Unmasked Values')
ax.set_xlabel('num')
#ax.set_ylabel('Number of (x,y,z) points with synapse density = x')


fig = plt.figure(2)
ax = fig.gca()
plt.hist(csv[:,4], bins = 100)
ax.set_title('Hist of synaps')
ax.set_xlabel('num')
#ax.set_ylabel('Number of (x,y,z) points with synapse density = x')


fig = plt.figure(3)
ax = fig.gca()
plt.hist(newcsv-newsyn,bins=100)
ax.set_title('Hist of Normalized (Unmasked - Synaps)')
ax.set_xlabel('num')
#ax.set_ylabel('Number of (x,y,z) points with synapse density = x')

fig = plt.figure(4)
ax = fig.gca()
plt.hist(csv[:,3]- csv[:,4],bins=100)
ax.set_title('Hist of  Unmasked -  Synaps')
ax.set_xlabel('num')
#ax.set_ylabel('Number of (x,y,z) points with synapse density = x')

a = np.divide(csv[:,4],newcsv)


fig = plt.figure(4)
ax = fig.gca()
plt.hist(csv[:,4]/newcsv,bins=100)
ax.set_title('Hist of  Unmasked / normalized Synaps')
ax.set_xlabel('num')
#ax.set_ylabel('Number of (x,y,z) points with synapse density = x')

unMaskedThresh = np.mean(csv[:,3]) #+ np.std(csv[:,3])

print "unMaskedThresh: " + str(unMaskedThresh)

def check_condition(row):
    if row[3] < unMaskedThresh:
        return False
    return True

a = np.apply_along_axis(check_condition, 1, csv)
a = np.where(a == True)[0]
csv = csv[a, :]

fig = plt.figure(5)
ax = fig.gca()
plt.hist(csv[:,3],bins=25)
ax.set_title('Hist of top half of Unmasked Values')
ax.set_xlabel('num')


plt.show()

