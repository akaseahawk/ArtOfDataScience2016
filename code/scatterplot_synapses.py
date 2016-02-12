"""make a 3d scatterplot of the synapses
currently the program only looks at data points
with synapses > mean synapses
and then randomly samples from that data set
since if there are too many data points the 3d grapher
runs very slowly
-Jay Miller """

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np


def check_condition(row):
    if row[-1] == 0:
        return False
    return True


def synapse_filt(row, avg):
    if row[-1] > avg:
        return True
    return False

csv = np.genfromtxt('output.csv', delimiter=",")
samples = 5000

# only look at data points where the number of synapses is greater than avg
a = np.apply_along_axis(check_condition, 1, csv)
a = np.where(a == True)[0]
nonzero_rows = csv[a, :]
avg_synapse = np.mean(nonzero_rows[1:, -1])
print avg_synapse
filter_avg_synapse = np.apply_along_axis(synapse_filt, 1,
                                         nonzero_rows, avg_synapse)
a = np.where(filter_avg_synapse == True)[0]
nonzero_filtered = nonzero_rows[a, :]
xyz_only = nonzero_filtered[:, [1, 2, 3]]

# randomly sample
perm = np.random.permutation(xrange(1, len(xyz_only[:])))
xyz_only = xyz_only[perm[:samples]]
# get range for graphing
x_min = np.amin(xyz_only[:, 0])
x_max = np.amax(xyz_only[:, 0])
y_max = np.amax(xyz_only[:, 1])
y_min = np.amin(xyz_only[:, 1])
z_min = np.amin(xyz_only[:, 2])
z_max = np.amax(xyz_only[:, 2])

# following code adopted from
# https://www.getdatajoy.com/examples/python-plots/3d-scatter-plot
fig = plt.figure()
ax = fig.gca(projection='3d')

ax.set_title('3D Scatter Plot')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_zlim(z_min, z_max)

ax.view_init()
ax.dist = 12  # distance

ax.scatter(
           xyz_only[:, 0], xyz_only[:, 1], xyz_only[:, 2],  # data
           color='purple',  # marker colour
           marker='o',  # marker shape
           s=30  # marker size
)

plt.show()  # render the plot
