import numpy as np
import sklearn.cluster as cluster



def check_condition(row):
    if row[-1] == 0:
        return False
    return True

csv = np.genfromtxt('output.csv', delimiter=",")[1:]

a = np.apply_along_axis(check_condition, 1, csv)
a = np.where(a == True)[0]
nonzero_rows = csv[a, :]
xyz_only = nonzero_rows[:, [0, 1, 2]]

n_clusters = 10
kmeans_algo = cluster.KMeans(n_clusters=n_clusters)
clusters = kmeans_algo.fit_predict(xyz_only)
