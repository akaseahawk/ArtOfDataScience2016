import numpy as np

data = np.genfromtxt('output.csv', delimiter=",")[1:]
corr = np.corrcoef(data[:, 3], data[:, 4])
print corr
