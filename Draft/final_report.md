## Final Report -- May 5, 2016
**Table of Contents:**
- [Overview](./finals_report.md#overview)
- [Scientific Questioning](./final_report.md#scientific-questioning)
  - [Decriptive Analysis](./final_report.md#descriptive-analysis)
  - [Exploratory Analysis](./final_report.md#exploratory-analysis)
  - [Inferential Analysis](./final_report.md#inferential-analysis)
  - [Predictive Analysis](./final_report.md#predictive-analysis)
  - [Testing Assumptions](./final_report.md#testing-assumptions)
  - [Extended Exploratory Analysis](./final_report.md#extended-exploratory-analysis)
  - [Conclusion(./final_report.md#conclusion)

----------
### Overview
Our dataset is taken from the 2011 *M. musculus* V1 dataset from *Network anatomy and in vivo physiology of visual cortical neurons* (Bock et al)<sup id="r-dbock">[1](f-dbock)</sup>. The raw dataset was over 30 TB and was further processed resulting in an EM volume representation of the data. Our synaptic density data is a result of downsampling the EM data through synapse characterization algorithms and spatial reduction. Our dataset consists of (x,y,z) coordinates, the number of synapses at that point and the unmasked value for that region. 

### Significance
Synapse connectivity is vital to understanding neural circuits in the cerebral cortex. Synaptic density may be an indicator for the network of neurons in the cortex. Specifically, patterns in synaptic density can illuminate features within cortical layers and throughout cortical layers that may be significant to understanding the overall structure of the cortex. Combined with information about neural functioning, an understanding of cortical structure may be useful for studying etiology of mental illnesses with known cortical defects as well as diseases that plague the cerebral cortex.

### Scientific Questioning
We will discuss our analysis of the synapse density data, starting with exploratory and descriptive analysis, through hypothesis testing and regression, and ending with extended exploratory analysis inspired by previous results. The questions posed are followed by their outcomes.

#### Descriptive Analysis 
We began by seeking some basic understanding of this data. To understand the structure of our data, we first asked questions regarding charachteristics of the data such as dataset size and shape, number of total synapses, and number of invalid (i.e. unmasked value = 0) data points were present in our data, what a histogram of the synapse density looks like. Below are the results of these questions. 

|Query|Syn Density Dataset|
|-------|-----------------|
|Dataset Size/Shape|(61776, 5)|
|Total Synapses|7704178| 
|Invalid data points|6595|

<img src="../figs for progress report/histogram.png" data-canonical-src="../figs for progress report/histogram.png" width="400" height="300" />

Another descriptive question asked regarded the meaning of the unmasked variable. After consulting with those familiar with the dataset who have an understanding of how the data was collected, we were able to gain an understanding of the meaning of the variable. The unmaksed value was a way to differentiate between boundary regions and those regions missing data from good-quality regions of data when the data was processed. The mask represents regions which are to be ignored and are not meaningful data. Data points with an unmasked value of zero are regions considered insignificant. More specifically, the unmasked value represents the number of voxels in that row which have meaningful data. 

** Histogram of unmasked ** (lots of data ignored, lots meaningful)

Naturally, we suspected a relationship between the unmasked value and number of synapses at a given coordinate, and as such, tested for the correlation between the two. The correlation  between the unmasked value and number of synapses at a coordinate is 0.89621769. 

** Change to something about 3d distribution of syn density, find plot we made **

The final descriptive question asked regarded clustering of the data. We suspected a natural clustering of synapses to be present, and
thus we produced a scatter plot of the data to get a general idea of how the synapses are clustered and the structure as a whole.

<img src="../figs for progress report/scatter.png" data-canonical-src="../figs for progress report/scatter.png" width="400" height="300" />

** Add histogram of synaptic density **
** Add cutting off edges **


#### Exploratory Analysis
Knowing what the unmasked value is, we could remove invalid data entries where unmasked values were zero. With the remaining data, we sought to gain a general understanding of how the synapses are structured in the sample. Thus we asked how the data could be clustered and which metrics should be used to cluster the synapses. We used k-means, varying k-values. In terms of which metrics to be using, since we're dealing with objects in 3D space, Euclidean distance is the obvious choice. These results are displayed below. 

<img src="../figs for progress report/kmeans_cluster.png" data-canonical-src="../figs for progress report/kmeans_clusters.png" width="400" height="300" />
<img src="../figs for progress report/kmeans_centers.png" data-canonical-src="../figs for progress report/kmeans_centers.png" width="400" height="300" />

We ran k-means clustering with 4, 5, and 10 clusters and found that 4 clusters looked the most well organized and naturally structured
out of those options. Our main goal in running the k-means clustering algorithm at this point was to see if there is any sense of 
natural clustering in the data and whether or not it was visible and apparent. Later, we return to clustering where we find the optimal number of clusters of synapses for the dataset.

We also asked about the values of mean of the probability mass function (f: R^3→[0, 1] where f(x, y, z)=probability that a synapse exists at (x, y, z)). The mean is 1.61875161875e-05.

To gain a better understanding of the limits of our dataset, we asked about the bounds of our (x,y,z) coordinates and the maximum number of synapses that occur at any one coordinate. The results are tabulated below.

|Query| Syn Density Dataset|
|-----|--------------------|
|Min/Max x-value|1369/3358|
|Min/Max y-value|55/1165|
|Min/Max z-value|0/165789|
|Max number of synapses at one point|33450|
|Point at which max number of synpases occurs|(2749.0, 1876.0, 1054.0)|

#### Inferential Analysis

##### Synaptic Density Uniformity
** just use hist of synapses, show non-uniformity **
The histogram of synaptic density clearly shows a non-uniform distribution of synapses in our sample. We see that medium-density areas are more common than low or high density, thus ruling out the hypothesis of uniformity of synaptic density.

#### Predictive Analysis
Now that a relationship between synapses and the unmasked value has been observed, we can attempt to solidify
the relationship between synapses and the unmasked value. Several types of regressions were trained and tested using 10-fold cross-validation, 
and their results are tabulated below.

| Regression | Accuracy | Standard Deviation |
|------------|----------|--------------------|
|K-Nearest Neighbors| 0.25 | +/- 2.54 |
|Linear SVR| 0.57 | +/- 0.18 |
|Linear| 0.62 | +/- 0.40 |
|Random Forest| 0.79 | +/- 0.51 |
|Polynomial Regression| 0.85 | +/- 0.27 |

The regression accuracy on our data based on the five tested regression algorithms is, at best, 
85%, and, at worst, 18%. From the poor results of the K-nearest neighbors and linear SVR regressions, 
We see that the relationship between the variables (x,y,z,synapses) and the unmasked value is most likely
not linear due to the poorer performance of the linear regression compared to the very well-performing
polynomial regression. We believe K-nearest neighbors failed to the 
high dimensionality of our data. Distances become less representative of the data with increasing 
dimensionaltiy. Next, we plan to investigate why the polynomial regression and random forest regression performed relatively well and review our 
assumptions for accuracy and completeness as well as adjust our regression algorithm parameters
to better represent the true data as well as the adjusted assumptions. To gain more understanding of why
the regression algorithms performed the way they did, we reevaluated our procedure thus far and tested our assumptions. 
This is explained further in the Testing Assumptions and Next Steps sections.

#### Testing Assumptions
The prior analyses all made the assumptions that our data was i.i.d (identically and independently distributed). Here we test whether or not such assumptions were actually true.

First we will look at the identical assumption. As mentioned previously, in our exploratory analyses, we did notice some clustering, so it was likely that the data was infact not identically distributed. We more formally investigate this now. We did GMM clustering on the data, and plotted the BIC against the number of clusters.

<img src="../figs for progress report/clusters_bic.png" data-canonical-src="../figs for progress report/clusters_bic.png" width="400" height="400" />

We noticed an elbow at 4 clusters, so we concluded that this was the optimal number of clusters. Thus we concluded that our assumption of identical distributions was false. Also note the spike at 11 clusters: we hypothesize that this is due to the fact that there are 11 possible z-values.

Now we will investigate the independence assumption. To do this we can look at the sample-covariance matrix of our data. Since our data set was so big, doing this for all the data at once is infeasible. Instead we randomly sample from the data many times, taking the sample covariance for each of these random samples. Then we finally average these covariance matrices (element-wise).

<img src="../figs for progress report/covariance_matrix.png" data-canonical-src="../figs for progress report/covariance_matrix.png" width="400" height="400" />

Here we see that the covariance was highly concentrated along the diagonal, indicating that the data was infact independently distributed.

### Extended Exploratory Analysis
#### Constructing a model of our data

We use k-means clusetering on the data, scaling the densities up so that they have a greater effect on the clustering. We calculated the maximum and minimum vvalues for clusters of synaptic density. There was a clean partitioning of the density ranges with little overlap.

|Cluster | Minumum | Maximum |
|--------|---------|---------|
|1| 0.0014 | 0.0033 |
|2| 0.0006 | 0.0011 |
|3| 0 | 0.0006 |
|4| 0.0011 | 0.0014 |

Next, we used four Poissons to model the data based on the results of the clustering above. The table below compares statistical characteristics of the true data to the simulated Poisson data.

|------| Mean | Median | Standard Deviation |
|--------------|------|--------|--------------------|
|True Data|  | 163 | 174 | 69 |
|Simulated Data| 163 | 178 | 64 |

The mean, median and standard deviatio of the simulated data are close to that of the true data. To decide whether the model was an accurate representation of the true data, we compared the models using a K-S test.
A low p-value of 1.7e-73for the Poisson model indicates that the model is a poor representation of the true distribution. 

#### Density variation in x, y, z directions
We see evident signs of cortical layering in the y-direction defined by density local minima. 
** put in mean_xyz.png , total_dens_xyz.png, deriv_across_y.png**
We see local maxima that are steadily decreasing as y increases. This is strong evidence for the regions between local minima across the y-coordinates being cortical layers. The local minima defining the supposed cortical layer boundaries are the y-coordinates: 1837, 2071, 2305, 2539. The magnitude of the changes in synaptic density across y are evident.

We investigated whether the synapse distribution within these possible cortical layers is uniform. In the figures below, we see that the BIC curve defines the optimal number of clusters for synapses within these layers to be greater than one, meaning that synapses are not distributed uniformly throughout the layers.
** add in clusters in 3d space from jay's assignment 11 **
We see trands in clusters across the y-level sets. The maximum density red cluster and the minimum density blue cluster have strong variations in y. The ratio of red-to-blue is highest at smaller values of y and decreases to a minimum at the highest value of y. There is an obvious gradient of high-low density across y, giving more evidence for our suggestion of the cortical layers spanning the y-coordinates.

### Conclusion


### Methods

Code and mathematical theory for all questions is provided in detail for each analysis in the following notebooks.

| Question Type | Code |
|---------------|------|
| Descriptive | [**``../code/descriptive_exploratory_answers.ipynb``**](../code/descriptive_exploratory_answers.ipynb) |
| Exploratory | [**``../code/descriptive_exploratory_answers.ipynb``**](../code/descriptive_exploratory_answers.ipynb) |
| Inferential | [**``../code/inferential_simulation.ipynb``**](../code/inferential_simulation.ipynb) |
| Predictive  | [**``../code/regression_simulation.ipynb``**](../code/regression_simulation.ipynb) |
| Testing Assumptions | [**``../code/test_assumptions.ipynb``**](../code/test_assumptions.ipynb) |
