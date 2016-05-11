## Progress Report - March 22nd, 2016
**Table of Contents:**
- [Overview](./progress_report.md#overview)
- [Scientific Questioning](./progress_report.md#scientific-questioning)
  - [Decriptive Analysis](./progress_report.md#descriptive-analysis)
  - [Exploratory Analysis](./progress_report.md#exploratory-analysis)
  - [Inferential Analysis](./progress_report.md#inferential-analysis)
  - [Predictive Analysis](./progress_report.md#predictive-analysis)
  - [Testing Assumptions](./progress_report.md#testing-assumptions)
  - [Next Steps](./progress_report.md#next-steps)
- [Methods](./progress_report.md#methods)
  - [Decriptive Analysis](./progress_report.md#descriptive-analysis-1)
  - [Exploratory Analysis](./progress_report.md#exploratory-analysis-1)
  - [Inferential Analysis](./progress_report.md#inferential-analysis-1)
  - [Predictive Analysis](./progress_report.md#predictive-analysis-1)
  - [Testing Assumptions](./progress_report.md#testing-assumptions-1)

----------

### Overview
Mental illness causes huge financial social burdens for those affected by it. Gaining an understanding of brain function brings the research community one step closer to combating this plague on humanity. Brain structure is a good indicator of how the brain behaves. Understanding the structure of the brain may help us model functionality of brain feautres as function of synapse density. We have been analyzing the structure of the brain through synaptic density maps with the goal of understanging the connection between brain structure and brain function.

### Scientific Questioning
We will discuss our analysis of the synapse density data, starting with exploratory and descriptive analysis, through hypothesis testing and regression. The questions posed and their outcomes are described sequentially, with code and methods used to answer them described at the end of this report.

#### Descriptive Analysis
The natural first step when working with any data is to ask exploratory and descriptive questions about it. We have been working with the Kasthuri (2015) synapse densityi dataset (http://neurodata.io/Kasthurietal2014). The dataset consists of (x,y,z) coordinates, the number of synapses at that point and the unmasked value for that region. 

We began by seeking some basic understanding of this data. To understand the structure of our data, we first asked questions regarding charachteristics of the data such as dataset size and shape, number of total synapses, and number of invalid (i.e. unmasked value = 0) data points were present in our data, what a histogram of the synapse density looks like. Below are the results of these questions. 

|Query|Syn Density Dataset|
|-------|-----------------|
|Dataset Size/Shape|(61776, 5)|
|Total Synapses|7704178| 
|Invalid data points|6595|

<img src="../figs/figs for progress report/histogram.png" data-canonical-src="../figs/figs for progress report/histogram.png" width="400" height="300" />

Another descriptive question asked regarded the meaning of the unmasked variable. After consulting with those familiar with the dataset who have an understanding of how the data was collected, we were able to gain an understanding of the meaning of the variable. The unmaksed value was a way to differentiate between boundary regions and those regions missing data from good-quality regions of data when the data was acquired. The mask represents regions which are to be ignored and are not meaningful data. More specifically, the unmasked value represents the number of voxels in that row which have meaningful data. Naturally, we suspected a relationship between the unmasked value and number of synapses at a given coordinate, and as such, tested for the correlation between the two. The correlation  between the unmasked value and number of synapses at a coordinate is 0.89621769. 

The final descriptive question asked regarded clustering of the data. We suspected a natural clustering of synapses to be present, and
thus we produced a scatter plot of the data to get a general idea of how the synapses are clustered and the structure as a whole.

<img src="../figs/figs for progress report/scatter.png" data-canonical-src="../figs/figs for progress report/scatter.png" width="400" height="300" />


#### Exploratory Analysis
Knowing what the unmasked value is, we could remove invalid data entries where unmasked values were zero. With the remaining data, we sought to gain a general understanding of how the synapses are structured in the sample. Thus we asked how the data could be clustered and which metrics should be used to cluster the synapses. We used k-means, varying k-values. In terms of which metrics to be using, since we're dealing with objects in 3D space, Euclidean distance is the obvious choice. These results are displayed below. 

<img src="../figs/figs for progress report/kmeans_cluster.png" data-canonical-src="../figs/figs for progress report/kmeans_clusters.png" width="400" height="300" />
<img src="../figs/figs for progress report/kmeans_centers.png" data-canonical-src="../figs/figs for progress report/kmeans_centers.png" width="400" height="300" />

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
We now try to learn about the distribution of synapses through statistical inference. We chose to examine the distribution by looking at 'slices' of data across specific z-values. There were 11 such z-slices. Our data model was that the synapse density per slice follows a multinomial distribution. The null hypothesis was that the distribution was uniform across each slice (that is, each 'bin' of the multinomial distribution has equal probability). The alternative was that the distribution was not uniform (i.e. each bin does not have the same probability). We ran a chi-squared test to determine whether or not to reject the null. The values for each bin and then the p-value are as follows:

- [ 4.985  4.611  4.755  5.437  5.779  5.449  5.241  6.158  5.035  5.097 4.816]
- p-value: 0.999997409328

So we found that we cannot infact reject the null hypothesis. Looking at values for each bin, we can see that they are actually fairly uniform.

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
|Polynomial Regression| 0.85 | +/- 0.27 |=

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

<img src="../figs/figs for progress report/clusters_bic.png" data-canonical-src="../figs/figs for progress report/clusters_bic.png" width="400" height="400" />

We noticed an elbow at 4 clusters, so we concluded that this was the optimal number of clusters. Thus we concluded that our assumption of identical distributions was false. Also note the spike at 11 clusters: we hypothesize that this is due to the fact that there are 11 possible z-values.

Now we will investigate the independence assumption. To do this we can look at the sample-covariance matrix of our data. Since our data set was so big, doing this for all the data at once is infeasible. Instead we randomly sample from the data many times, taking the sample covariance for each of these random samples. Then we finally average these covariance matrices (element-wise).

<img src="../figs/figs for progress report/covariance_matrix.png" data-canonical-src="../figs/figs for progress report/covariance_matrix.png" width="400" height="400" />

Here we see that the covariance was highly concentrated along the diagonal, indicating that the data was infact independently distributed.

#### Next Steps

One thing that we have found is that the distribution of synapses across each z-slice is fairly uniform. However, we do not know anything about the spatial distribution within each of these z-slices. Therefore an interesting next step would be to examine the distribution of synapses along the xy-plane for each z-slice, and contrast and compare them across the set of all 11 slices. 

Another important next step is to interpret our regression results. While we did find that certain regression algorithms gave fairly good results, we don't know much about how the spatial positioning affected this, since there was obviously a strong relation between unmasked and synapses. Therefore we would like to run more regressions that don't involve this strong relationship, for example we would like to see if we can predict synapse density (synapses/unmasked) given x, y, z, another interesting relationship to examine would be the relationship betweeen position and unmasked (ignoring synapses), as this would give interesting information on the distribution of brain matter and also shed light on results about density.

### Methods

Code and mathematical theory for all questions is provided in detail for each analysis in the following notebooks.

| Question Type | Code |
|---------------|------|
| Descriptive | [**``../code/descriptive_exploratory_answers.ipynb``**](../code/descriptive_exploratory_answers.ipynb) |
| Exploratory | [**``../code/descriptive_exploratory_answers.ipynb``**](../code/descriptive_exploratory_answers.ipynb) |
| Inferential | [**``../code/inferential_simulation.ipynb``**](../code/inferential_simulation.ipynb) |
| Predictive  | [**``../code/regression_simulation.ipynb``**](../code/regression_simulation.ipynb) |
| Testing Assumptions | [**``../code/test_assumptions.ipynb``**](../code/test_assumptions.ipynb) |

#### Descriptive Analysis

Here we were looking for numbers and figures that summarize our dataset well. We looked at total number of synapses, made a histogram of synaptic density, calculated correlation between unmasked and synapses, and made a 3D-scatterplot of the data, in order to gain some intuitive sense of how our data looks in Euclidean space. We could have additionally done these computations accross each z-slice, instead of just for the entire data set, as this might have given us some value information on how the data varies across slices.

#### Exploratory Analysis 

One thing we investigated here was how the data was clustered. We ran the k-means algorithm for several different values of k and then plotted the data, coloring it based on clusters. This gave us some intuitive sense of how the data could/should be clustered, although we did not examine what the optimal number of clusters might've been (although we did do this later). We also looked at the min and max values for the positions, and also where the maximum number of synapses occured. Another interesting thing that we could have done was to look at where this maximum number occurs for each z-slice and then we could see how this position changes across z-slices.

#### Inferential Analysis 

Here we examined spatial distribution of synaptic density for each z-slice. That is, we looked at the total sum of synapses/unmasked for each distinct z-value. We determined using a chi-squared test, that the synapses may be uniformly distributed (that is we failed to reject our null hypothesis that they were uniform). We used a chi-squared test, primarily due to previous familiarity. To prove that the power converges to 1 given sufficient samples under the alternate, we generated similar data to the alternate and then plotted the power increasing.

<img src="../figs/figs for progress report/power.png" data-canonical-src="../figs/figs for progress report/power.png" width="400" height="400" />

Alternatively, we could have looked at the distribution across the entire data set, instead of per slice, but this would be infeasible using a chi-squared test. We could also have investigated further by doing another slicing across say the x-axis, for each of our z-slices, and then checking whether the distribution for the x-slices was uniform. 

#### Predictive Analysis 

Here we ran a regression that tried to predict unmasked given x, y, z, synapses. Unfortunately we realized in retrospect that this was not the most interesting regression to do, given the strong relationship between synapses and unmasked. Our initial train of thought was that it would've been interesting to see how synapses affects the amount of brain region (this is how we were interpreting unmasked). 

We ran Linear Regression, Support Vector Regression (SVR), K-Nearest Neighbor Regression (KNN), Random Forest Regression, and Polynomial Regression, all just with default sklearn parameters. In the future we should tune these parameters to best fit our data. To show that these regressions should infact be fairly effective on our data, we ran them on simulated data similar to ours, and then plotted the coefficient of determination (we used 10-fold cross-validation to determine the std-dev). 

<img src="../figs/figs for progress report/regression.png"  width="400" height="200" />

#### Testing Assumptions

To test independence, we looked at the sample covariance matrix. This means we were just looking at linear independence. So while we said that by looking at the sample covariance matrix, we were concluding that the data was independent, we actually are only determining that it is not linearly independent. That being said, lack of linear independence is still a strong indicator of an overall lack of independence.

To test identical distributions, we ran a GMM for different numbers of clusters and then plotted the BIC (Bayesian Information Criterion) for each. We looked for an elbow in the plot of BIC against # of clusters to determine the optimal one. This turned out to be 4. Interestingly, there is also a high spike at 11 clusters, but we attribute this to the fact that there are 11 z-slices. 
