###Questions about Project
Team: Emily Marshall, Jay Miller, Akash Ray, Bijan Varjavand

- Our dataset consists of N feature vectors
- The first 3 features of each vector represent x, y, and z coordinates
- The 4th feature is called ‘unmasked’--at the moment, we do not know what this feature represents
- The 5th feature represents the number of synapses at the position defined by features 1-3
- There is a probability density function f: R^3→[0, 1] where f(x, y, z)=probability that a synapse exists at (x, y, z)

**Descriptive**<br/>
- *What is the unmasking variable?*

  > ans 

- *How clustered are the groups of synapses?*

  > ans 


- How are the inhibitory and excitatory classes differentiated?

#Exploratory
- How can the data be clustered? (which metrics should be used for clustering)?
- Where are the centers of such clusters?
- What is the mean of the density function? What is the covariance?
- What is the set of all possible (x, y, z)?
- Where does the maximum number of synapses occur?

#Inferential
- Is the clustering location of any significance in relation to other interneuronal groups?

#Predictive
- What is the best classification of groups of inhibitory and excitatory neurons?
- Is there a regression model that can predict the output of f, the density function, given input x, y, z? 

#Causal
- How does density of synapses influence the network of pathways?

#Mechanistic
- How could utilizing inhibitory interneurons affect the structure of the brain?
