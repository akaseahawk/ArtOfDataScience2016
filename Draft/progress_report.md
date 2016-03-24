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
Reword so we're not plagiarizing...
We will discuss our analysis of the synapse density data, starting with exploratory and descriptive analysis, through hypothesis testing and regression. The questions posed and their outcomes are described sequentially, with code and methods used to answer them described at the end of this report.

#### Descriptive Analysis
The natural first step when working with any data is to ask exploratory and descriptive questions about it. We have been working with the Kasthuri (2015) synapse densityi dataset (http://neurodata.io/Kasthurietal2014). The dataset consists of (x,y,z) coordinates, the number of synapses at that point and the unmasked value for that region. 

We began by seeking some basic understanding of this data. To understand the structure of our data, we first asked questions regarding charachteristics of the data such as dataset size and shape, number of total synapses, and number of invalid (i.e. unmasked value = 0) data points were present in our data, what a histogram of the synapse density looks like. Below are the results of these questions. 

|Query|Syn Density Dataset|
|-------|-----------------|
|Dataset Size/Shape|(61776, 5)|
|Total Synapses|7704178| 
|Invalid data points|6595|

<img src="../figs for progress report/histogram.png" data-canonical-src="../figs for progress report/histogram.png" width="400" height="300" />

Another descriptive question asked regarded the meaning of the unmasked variable. After consulting with those familiar with the dataset who have an understanding of how the data was collected, we were able to gain an understanding of the meaning of the variable. The unmaksed value was a way to differentiate between boundary regions and those regions missing data from good-quality regions of data when the data was acquired. The mask represents regions which are to be ignored and are not meaningful data. More specifically, the unmasked value represents the number of voxels in that row which have meaningful data. Naturally, we suspected a relationship between the unmasked value and number of synapses at a given coordinate, and as such, tested for the correlation between the two. The correlation  between the unmasked value and number of synapses at a coordinate is 0.89621769. 

The final descriptive question asked regarded clustering of the data. We suspected a natural clustering of synapses to be present, and
thus we produced a scatter plot of the data to get a general idea of how the synapses are clustered and the structure as a whole.

<img src="../figs for progress report/scatter.png" data-canonical-src="../figs for progress report/scatter.png" width="400" height="300" />


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


#### Predictive Analysis
Now that a relationship between synapses and the unmasked value has been observed, we can attempt to solidify
the relationship between synapses and the unmasked value. Several types of regressions were trained and tested using LOO cross-validation, 
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

### Methods

Code and mathematical theory for all questions is provided in detail for each analysis in the following notebooks.
| Question Type | Code |
|---------------|------|
| Descriptive | [**``../code/descriptive_and_exploratory_answers.ipynb``**](../code/descriptive_and_exploratory_answers.ipynb) |
| Exploratory | [**``../code/descriptive_and_exploratory_answers.ipynb``**](../code/descriptive_and_exploratory_answers.ipynb) |
| Inferential | [**``../code/inferential_simulation.ipynb``**](../code/inferential_simulation.ipynb) |
| Predictive  | [**``../code/classification_simulation.ipynb``**](../code/classification_simulation.ipynb) |
| Testing Assumptions | [**``../code/test_assumptions.ipynb``**](../code/test_assumptions.ipynb) |

#### Descriptive Analysis

#### Exploratory Analysis 

#### Inferential Analysis 

#### Predictive Analysis 

#### Testing Assumptions
