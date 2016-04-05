## Group:
  * What is the spike? More Visualizations,
                     Regressions ,
                     Clustering ,
                     PCA
  * Bic keeps getting better as we go up right now--look at more clusters!
  * Look at histograms of the x,y bics from last time
  * Sample 100 or 1000 samples and rerun x,y bic curve after sampling (run bic many times, take max for each k)
    because fragile to outliers
  * Look at the two kmeans center of clusters graphs in the z-layer. Better visualizations, which way do they trend?
  * Covariances from last hw as heat maps

## Emily:
  * Plot vector estimates on top of the z-layer cluster center graph to see if estimate makes sense.
  * Visualization of the "spike" (scatter plot, etc)
  * Redo z-layer bics without setting random state (take max at each k) and analyze results
  * Work off of jay's gradient of density estimate (not using uniques), compare the two
  * Visualization of clustering after running the bic curve for higher ks (kmeans)
  * In the spike:
   * Min/Max x-value
   * Min/Max y-value
   * Min/Max z-value
   * Max number of synapses at one point
   * Point at which max number of synpases occurs

## Bijan:
#### 5 solo things hw week 4/4/2016
  * Overlay the scatterplot and vector graphs to find relationships - they seemed to correlate.
  * Find the direction between cluster centers per each z value, plot them all together and compare.
  * Run what I did last week, creating direction of increasing density, using # of partitions as a hyperparameter. Compare data across # of partitions (in x, y, z).
  * From the BIC curves generated last week, analyze the data from the z values that behaved differently (bend at 4 instead of 3). Plot histograms + cluster.
  * Elastic net regression on predicting synapses from xyz data for each z value, especially the ones that behaved differently earlier.

## Akash:
  *Regression in cluster 1 and 4
  *Regression in cluster 1,2,3
  *Scale centroid charts to be equal sizes
  *Compare centroid values in the 3 and 4 cluster groups
  *Figure out how to apply point cloud
  
  

## Jay:
