import numpy as np
import matplotlib.pyplot as plt
import random
import urllib2
import sklearn.linear_model as LR
from sklearn.svm import LinearSVR 
from sklearn.neighbors import KNeighborsRegressor as KNN
from sklearn.ensemble import RandomForestRegressor as RF
from sklearn.preprocessing import PolynomialFeatures as PF
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn import cross_validation
from sklearn.cross_validation import LeaveOneOut


#%matplotlib inline
# define number of subjects per class
sample_size = 10000
np.random.seed(1)
url = ('https://raw.githubusercontent.com/Upward-Spiral-Science'
       '/data/master/syn-density/output.csv')
data = urllib2.urlopen(url)
csv = np.genfromtxt(data, delimiter=",")[1:] # don't want first row (labels)

mins = [np.min(csv[:,i]) for i in xrange(5)]
maxs = [np.max(csv[:,i]) for i in xrange(5)]
domains = zip(mins, maxs)
Y_range = domains[3]
del domains[3]

# Null distribution
null_X = np.array([[np.random.randint(*domains[i]) for i in xrange(4)] for k in xrange(sample_size)])
null_Y = np.array([[np.random.randint(*Y_range)] for k in xrange(sample_size)])

# Alternate distribution
alt_X = np.apply_along_axis(lambda row : np.hstack((row[0:3], np.average(row[0:3]))), 1, null_X)
std_dev = np.sqrt(np.average(alt_X[:, 3]))
alt_Y = alt_X[:, 3]/4 + np.random.normal(scale=std_dev, size=(sample_size,))


# Sample sizes from each synthetic data distribution
S = np.array((100, 120, 200, 320,
              400, 800, 1000, 2500, 5000, 7500))

# Regressions
names = ['Linear Regression','SVR','KNN Regression','Random Forest Regression','Polynomial Regression']

# which kernel to use for SVR? which degree polynomial do we want to fit?
regressions_null = [LR.LinearRegression(), 
			   LinearSVR(C=1.0), 
			   KNN(n_neighbors=10, algorithm='auto'),
			   RF(max_depth=5, max_features=1),
			   Pipeline([('poly', PF(degree=2)),('linear', LR.LinearRegression(fit_intercept=False))])]

accuracy = np.zeros((len(S), len(regressions_null), 2), dtype=np.dtype('float64'))
for idx1, N in enumerate(S):
	# Randomly sample from synthetic data with sample size N
	a = np.random.permutation(np.arange(sample_size))[:N]
	X = null_X[a]
	Y = null_Y[a]

	for idx2, reg in enumerate(regressions_null):
		X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size=0.4, random_state=0)
		Y_train = np.ravel(Y_train)

		#Train the model using the training sets for null and alt distributions
		reg.fit(X_train,Y_train)

		loo = LeaveOneOut(len(X))
        scores = cross_validation.cross_val_score(reg, X, Y, cv=loo)
        accuracy[idx1, idx2,] = [scores.mean(), scores.std()]
        print("Accuracy of %s: %0.2f (+/- %0.2f)" % (names[idx2], scores.mean(), scores.std() * 2))

print accuracy













'''
# Plot scores vs N

# Apply technique to data
'''