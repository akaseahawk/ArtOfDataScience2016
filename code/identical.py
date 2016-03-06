import numpy as np
import sklearn.mixture as mixture
import sklearn.preprocessing as preprocess
import matplotlib.pyplot as plt

#%matplotlib inline

np.random.seed(1)
csv = np.load("data.npy")
# csv = preprocess.normalize(csv, axis=0)
max_clusters = 15
bic = np.array([])
i = np.array(range(1, max_clusters))
for idx in range(1, max_clusters):
    print "Fitting and evaluating model with " + str(idx) + " clusters."
    gmm = mixture.GMM(n_components=idx,n_iter=1000,covariance_type='diag')
    gmm.fit(csv)
    bic = np.append(bic, gmm.bic(csv))
print bic
plt.figure(figsize=(7,7))
plt.plot(i, 1.0/bic)
plt.title('BIC')
plt.ylabel('score')
plt.xlabel('number of clusters')
plt.show()


