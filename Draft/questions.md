#Questions about Project
Emily Marshall, Jay Miller, Akash Ray, Bijan Varjavand

- Our dataset consists of N feature vectors
- The first 3 features of each vector represent x, y, and z coordinates
- The 4th feature is called ‘unmasked’--at the moment, we do not know what this feature represents
- The 5th feature represents the number of synapses at the position defined by features 1-3
- There is a probability mass function f: R^3→[0, 1] where f(x, y, z)=probability that a synapse exists at (x, y, z)

##Descriptive
- What is the unmasking variable?
  > ans
- How clustered are the groups of synapses?
- How are the inhibitory and excitatory classes differentiated?
- *New questions*
- What does a representative slice of our data look like?

#Exploratory
- How can the data be clustered? (which metrics should be used for clustering)?
- Where are the centers of such clusters?
- What is the mean of the probability mass function? What is the covariance?
- What is the set of all possible (x, y, z)?
- Where does the maximum number of synapses occur?
- *New questions*
- How do other clustering algorithms compare to our current k-means clustering representation of the synapse density data?
- What do we consider outliers? What do they represent? How are we going to handle outliers?
- What is the set of (x, y, z) removing outliers? How does removing outliers change our current statistical results regarding the synapse density.
- What is the statistical significance of our PMF model?
- What is the correlation between synapse number and the unmasked value?
  

#Inferential
- Is the clustering location of any significance in relation to other interneuronal groups?

#Predictive
- What is the best classification of groups of inhibitory and excitatory neurons?
- Is there a regression model that can predict the output of f, the density function, given input x, y, z? 

#Causal
- How does density of synapses influence the network of pathways?

#Mechanistic
- How could utilizing inhibitory interneurons affect the structure of the brain?
