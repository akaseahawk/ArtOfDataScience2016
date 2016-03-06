import numpy as np
import matplotlib.pyplot as plt
import urllib2

#%matplotlib inline

sample_size = 1000
np.random.seed(1)
url = ('https://raw.githubusercontent.com/Upward-Spiral-Science'
       '/data/master/syn-density/output.csv')
data = urllib2.urlopen(url)
csv = np.genfromtxt(data, delimiter=",")[1:] 

csv_rand = None
for i in range (1, sample_size):
	#Randomly sample from dataset
	a = np.random.permutation(np.arange(csv.shape[0]))[:100]
	csv_rand_sample = csv[a]

	# Normalize
	mean_unmask = np.mean(csv_rand_sample[:,3])
	std_unmask = np.std(csv_rand_sample[:,3])
	csv_rand_sample[:,3] = (csv_rand_sample[:,3]-mean_unmask)/std_unmask

	#Stack matrix
	if i == 1:
		csv_rand = csv_rand_sample
	else:
		csv_rand = np.dstack((csv_rand,csv_rand_sample))

#Average across random samples
csv_rand = np.mean(csv_rand,axis=2)


#Independent Graph Assumption
covar = np.cov(csv_rand_sample)

plt.figure(figsize=(7,7))
plt.imshow(covar)
plt.title('Covariance of Synapse Density dataset')
plt.colorbar()
plt.show()

diag = covar.diagonal()*np.eye(covar.shape[0])
hollow = covar-diag
d_det = np.linalg.slogdet(diag)[1]
h_det = np.linalg.slogdet(hollow)[1]
print d_det
print h_det

plt.figure(figsize=(11,8))
plt.subplot(121)
plt.imshow(diag)
plt.clim([0, np.max(covar)])
plt.title('Determinant of on-diagonal: ' + str(d_det))
plt.subplot(122)
plt.imshow(hollow)
plt.clim([0, np.max(covar)])
plt.title('Determinant of off-diagonal: ' + str(h_det))
plt.show()

print "Ratio of on and off-diagonal determinants: " + str(d_det/h_det)
